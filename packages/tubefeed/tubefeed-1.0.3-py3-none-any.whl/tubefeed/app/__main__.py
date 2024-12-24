import asyncio
import logging
import os
import re
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile

import aiofiles
from fastapi import FastAPI, HTTPException
from starlette.responses import Response, RedirectResponse, StreamingResponse
from yt_dlp import DownloadError

from .. import APP_VERSION, DB_VERSION
from ..database import Database, Channel, Playlist
from ..feed import Feed
from ..ytapi import YouTube, Error as YTError, Playlist as YTPlaylist
from ..ytdlp import get_audio_url, store_audio, m4a_header

###########################################################
# configuration                                           #
# mostly read from environment variables                  #
###########################################################
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:8000')
DATA_DIR = Path(os.environ.get('DATA_DIR', './data/'))
YT_API_KEY = os.environ.get('YT_API_KEY')

RDS = int(os.environ.get('RELEASE_DELAY_STATIC', '600'))
RDDF = float(os.environ.get('RELEASE_DELAY_DURATION_FACTOR', '0.0'))

FSL = os.environ.get('FEED_SIZE_LIMIT', None)
FSL = int(FSL) if FSL is not None else FSL

UNSAFE_DOWNLOAD_METHOD = os.environ.get('UNSAFE_DOWNLOAD_METHOD', '').lower() in ('true', 'yes', '1')
MAX_DOWNLOAD_RATE = os.environ.get('MAX_DOWNLOAD_RATE', None)
YT_DLP_FORMAT = os.environ.get('YT_DLP_FORMAT', 'bestaudio[ext=m4a]')
FFMPEG_BITRATE = os.environ.get('FFMPEG_BITRATE', None)

VERSION_PATH = DATA_DIR / 'version.txt'
DATABASE_PATH = DATA_DIR / 'cache.db'


###########################################################
# FastAPI configuration                                   #
# includes creating and initializing the cache database   #
###########################################################
@asynccontextmanager
async def lifespan(_: FastAPI):
    # create data directory
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True)

    # get database version from file
    if VERSION_PATH.exists():
        with open(VERSION_PATH, 'r') as f:
            current_version = f.read().strip()
    else:
        current_version = None

    # recreate database if outdated
    if current_version != DB_VERSION:
        logging.warning(f'database schema is outdated, recreating')

        DATABASE_PATH.unlink(missing_ok=True)
        with open(VERSION_PATH, 'w') as f:
            f.write(DB_VERSION)

    # create database tables
    async with Database(DATABASE_PATH) as db:
        await db.create_tables()

    yield


app = FastAPI(lifespan=lifespan)


###########################################################
# API functions                                           #
###########################################################
@app.get('/')
async def root():
    """
    This function is just included for convenience. It returns a couple of
    notices on how to use the API. However, this is neither a real API
    description, nor does it contain all the usable parameters.

    :return: json
    """
    return {
        'title': 'Tubefeed',
        'version': APP_VERSION,
        'refs': {
            '/channel/{handle}': 'rss feed from channel handle',
            '/playlist/{id}': 'rss feed from playlist id',
            '/video/{id}': 'url to m4a audio stream for video id'
        }
    }


@app.get('/channel/{handle}')
async def get_channel(handle: str,
                      include: str = None,
                      limit: int | None = None,
                      format: str = None, bitrate: str = None):
    if not include:
        include = ['videos', 'livestreams']
    else:
        include = include.split(' ')

    # convert handle to lowercase
    handle = handle.lower()

    # ensure channel is in database and build feed
    async with Database(DATABASE_PATH) as db:
        # load channel from database
        channel = await ensure_channel_in_db(db, handle)

        # run get_playlist to update playlist items
        uploads = await channel.uploads()
        children = [
            c
            for c in await uploads.children()
            if c.child_name in include
        ]

        await asyncio.gather(*(
            ensure_playlist_in_db(db, c)
            for c in children
        ))

        # build feed
        feed = Feed(BASE_URL, limit or FSL, UNSAFE_DOWNLOAD_METHOD, format=format, bitrate=bitrate)
        await feed.add_channel(channel, *children)

    # return response
    return Response(status_code=200, content=str(feed), media_type='application/xml')


@app.get('/channel/{handle}/avatar.jpg')
async def get_channel(handle: str):
    # convert handle to lowercase
    handle = handle.lower()

    # get channel and avatars from database
    async with Database(DATABASE_PATH) as db:
        channel = await ensure_channel_in_db(db, handle)
        avatars = await channel.avatars()

    # return error if no avatar is found
    if len(avatars) == 0:
        raise HTTPException(status_code=404, detail=f'no avatar found for {handle}')

    # select avatar with max size
    avatar_url = max(avatars, key=lambda a: a.width).url

    # send redirect to client
    return RedirectResponse(url=avatar_url, status_code=302)


@app.get('/playlist/{id}')
async def get_playlist(id: str,
                       limit: int | None = None,
                       format: str = None, bitrate: str = None):
    # ensure playlist is in database and build feed
    async with Database(DATABASE_PATH) as db:
        # get playlist from database
        playlist = await ensure_playlist_in_db(db, id)

        # build feed
        feed = Feed(BASE_URL, limit or FSL, UNSAFE_DOWNLOAD_METHOD, format=format, bitrate=bitrate)
        await feed.add_playlist(playlist)

    # return response
    return Response(status_code=200, content=str(feed), media_type='application/xml')


@app.get('/playlist/{id}/thumbnail.jpg')
async def get_playlist_thumbnail(id: str):
    # get playlist and thumbnails from database
    async with Database(DATABASE_PATH) as db:
        playlist = await ensure_playlist_in_db(db, id)
        thumbnails = await playlist.thumbnails()

    # return error if no thumbnail is found
    if len(thumbnails) == 0:
        raise HTTPException(status_code=404, detail=f'no thumbnail found for {id}')

    # select thumbnail with max size
    thumbnail_url = max(thumbnails, key=lambda a: a.width).url

    # send redirect to client
    return RedirectResponse(url=thumbnail_url, status_code=302)


@app.get('/video/{id}/thumbnail.jpg')
async def get_video_thumbnail(id: str):
    # get video and thumbnails from database
    async with Database(DATABASE_PATH) as db:
        video = await db.get_video(id)
        if video is None:
            raise HTTPException(status_code=404, detail=f'video {id} not found')

        thumbnails = await video.thumbnails()

    # return error if no thumbnail is found
    if len(thumbnails) == 0:
        raise HTTPException(status_code=404, detail=f'no thumbnail found for {id}')

    # select thumbnail with max size
    thumbnail_url = max(thumbnails, key=lambda a: a.width).url

    # send redirect to client
    return RedirectResponse(url=thumbnail_url, status_code=302)


@app.get('/video/{id}/audio.m4a')
async def get_video_audio_m4a(id: str, format: str = None):
    """
    The old download method uses yt-dlp to receive a file url from YouTube
    and redirects Audiobookshelf to this url. This is a very simple approach
    and should work even with outdated versions of yt-dlp. The downside is
    that YouTube often limits the download speed to twice the bitrate of the
    file, which means that a one-hour video will take 30 minutes to download.
    This also means that we cannot change anything about the video file.


    :param id: YouTube id of the video
    :param format: value for yt-dlp -f
    :return: redirect to an url to download the audio directly from YouTube
    """
    try:
        audio_url = await get_audio_url(f'https://www.youtube.com/watch?v={id}', format or YT_DLP_FORMAT)
        return RedirectResponse(url=audio_url, status_code=302)

    # error from yt-dlp
    except DownloadError as e:
        raise HTTPException(status_code=500, detail=e.msg)


@app.get('/video/{id}/audio_remuxed.m4a')
async def get_video_audio_m4a_remuxed(id: str, format: str = None, bitrate: str = None):
    """
    The new download version uses yt-dlp in conjunction with ffmpeg. This
    should make downloads much faster, rewrites metadata and allows chapter
    marks to be added to the file.

    :param id: YouTube id of the video
    :param format: value for yt-dlp -f
    :param bitrate: value for ffmpeg -b:a
    :return: stream containing the downloaded and remuxed file
    """
    format = format or YT_DLP_FORMAT
    bitrate = bitrate or FFMPEG_BITRATE

    # receive video info from database
    async with Database(DATABASE_PATH) as db:
        video = await db.get_video(id)
        if video is None:
            raise HTTPException(status_code=404, detail=f'video {id} not found')

    # extract chapters from video description
    chapters_iter = re.finditer(r'^\s*((\d+):)?(\d+):(\d+)\s.*?(\w.*?)$', video.description, re.MULTILINE)
    chapters: list[tuple[int, str | None]] = []

    for chapter in chapters_iter:
        hours = int(chapter.group(2)) if chapter.group(2) is not None else 0
        minutes = int(chapter.group(3)) if chapter.group(3) is not None else 0
        seconds = int(chapter.group(4)) if chapter.group(4) is not None else 0
        title = chapter.group(5).strip()

        chapters.append(((hours * 60 + minutes) * 60 + seconds, title))

    chapters.append((video.duration, None))

    # store chapters to temporary file if there are any
    if len(chapters) > 1:
        with NamedTemporaryFile(suffix='_chapters.metadata', mode='w', encoding='utf-8', delete=False) as metadata_file:
            metadata_file.write(';FFMETADATA1\n')

            for (start, title), (end, _) in zip(chapters, chapters[1:]):
                metadata_file.write('[CHAPTER]\n')
                metadata_file.write('TIMEBASE=1/1\n')
                metadata_file.write(f'START={start}\n')
                metadata_file.write(f'END={end}\n')
                metadata_file.write(f'title={title}\n')

            metadata_path = Path(metadata_file.name)
    else:
        metadata_path = None

    # create a temporary file to store the audio
    with NamedTemporaryFile(suffix='_audio.m4a', delete=False) as m4a_file:
        m4a_path = Path(m4a_file.name)

    # send the file
    async def generate_stream():
        # start download function in background
        yt_dlp_options = {
            'f': format,
            'r': MAX_DOWNLOAD_RATE
        }

        if bitrate is None:
            ffmpeg_options = {
                'c': 'copy'
            }
        else:
            ffmpeg_options = {
                'c:a': 'aac',
                'b:a': bitrate
            }

        store_job = store_audio(video.url, yt_dlp_options, metadata_path, m4a_path, ffmpeg_options)
        store_task = asyncio.create_task(store_job)

        # wait up to 20 seconds before sending the first byte
        for _ in range(20):
            if not store_task.done():
                await asyncio.sleep(1)

        # Send a byte of the header every 28 seconds while the download is running.
        # This should prevent Audiobookshelf from closing the connection.
        for i in range(len(m4a_header)):
            yield m4a_header[i:i + 1]

            for _ in range(28):
                if not store_task.done():
                    await asyncio.sleep(1)

        # finally read the file
        await store_task

        async with aiofiles.open(m4a_path, 'rb') as m4a_input:
            # skip header
            await m4a_input.read(len(m4a_header))

            # send data in chunks
            while chunk := await m4a_input.read(8192):
                yield chunk

        # remove temporary files
        for path in (metadata_path, m4a_path):
            if path is None:
                continue

            try:
                path.unlink()
            except FileNotFoundError:
                pass

    return StreamingResponse(generate_stream(), media_type='audio/m4a')


###########################################################
# data transport functions                                #
# These ensure the required data is in the database.      #
###########################################################
async def ensure_channel_in_db(db: Database, handle: str) -> Channel:
    # get channel object from database
    channel = await db.get_channel_by_handle(handle)

    # fetch from YouTube if missing in database
    if channel is None:
        async with YouTube(YT_API_KEY) as yt:
            try:
                # search for handle
                for yt_c in await yt.find_channels(handle=handle):
                    # get uploads playlist
                    yt_u = await yt_c.uploads()

                    # store in database
                    channel = await db.add_channel(yt_c, yt_u)

                    # break so no 404 is raised
                    break

                # handle not found
                else:
                    raise HTTPException(status_code=404, detail=f'channel {handle} not found')

            # error from YouTube
            except YTError as e:
                raise HTTPException(status_code=e.code, detail=e.message)

    await db.commit()
    return channel


async def ensure_playlist_in_db(db: Database, playlist: str | Playlist) -> Playlist:
    now = datetime.now().timestamp()

    async with YouTube(YT_API_KEY) as yt:
        # If the given playlist is a Playlist object from the database
        # package, we just need to create a yt_pl object to use later.
        if isinstance(playlist, Playlist):
            yt_pl = YTPlaylist.from_id(yt, playlist.id)

        # If the given playlist is a string / id, we need to get the
        # object from the database or create it with data from YouTube
        # before updating the videos.
        else:
            id = playlist

            # get playlist object from database
            playlist = await db.get_playlist(id)

            if playlist is not None:
                yt_pl = YTPlaylist.from_id(yt, id)

            # fetch playlist from YouTube if missing in database
            else:
                try:
                    # fetch playlist
                    yt_pl = await yt.get_playlist(id)
                    if yt_pl is None:
                        raise HTTPException(status_code=404, detail=f'playlist {id} not found')

                    # check if channel is not already in database
                    channel = await db.get_channel_by_id(yt_pl.channel_id)

                    if channel is None:
                        # fetch channel and store in database
                        yt_ch = await yt_pl.channel()
                        yt_ch_u = await yt_ch.uploads()

                        channel = await db.add_channel(yt_ch, yt_ch_u)

                    # store playlist in database
                    playlist = await channel.add_playlist(yt_pl)

                # error from YouTube
                except YTError as e:
                    raise HTTPException(status_code=e.code, detail=e.message)

        # We request the playlist items from YouTube and store the missing
        # ones in the database.
        try:
            async for yt_videos in yt_pl.videos():
                # fetch video objects from database
                db_videos = await asyncio.gather(*(playlist.get_video(v.id) for v in yt_videos))

                # find missing videos
                yt_v_missing = [yt_v for db_v, yt_v in zip(db_videos, yt_videos) if db_v is None]

                # receive details for missing videos
                yt_v_details = await yt.get_videos(yt_v_missing)

                # store in database
                yt_v_insert = ((v, int(v.published.timestamp()) + max(RDDF * v.duration, RDS)) for v in yt_v_details)

                await asyncio.gather(*(
                    playlist.add_video(v, sk)
                    for v, sk in yt_v_insert
                    if not v.is_live and sk <= now
                ))

                # break if oldest fetched video is already in db
                if db_videos[-1] is not None:
                    break

        except YTError as e:
            # Under some circumstances we do not want to raise an error here.
            # If a channel did not upload a single short for example, the
            # playlist does not exist. This is expected behaviour though.
            if not playlist.child_name or e.code != 404:
                raise e

    await db.commit()
    return playlist
