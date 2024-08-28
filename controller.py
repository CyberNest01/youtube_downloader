from pytube import Playlist
import yt_dlp as youtube_dl
from fastapi import HTTPException

from Http import UrlType

from dataclasses import dataclass
import zipfile
import os
import datetime


@dataclass
class FuncRes:
    status: bool
    message: str = None
    file_path: str = None


async def download_youtube_video(url: str, resolution: str) -> FuncRes:
    try:
        ydl_opts = {
            'format': f'bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]',
            'outtmpl': 'Download/%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'restrictfilenames': True,
            'cookiefile': 'cookies.txt'
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info_dict)
        return FuncRes(status=True, message="Download Complete !!!", file_path=file_path)
    except Exception as e:
        return FuncRes(status=False, message=e.__str__())


async def youtube_downloader(url: str, url_type: int, resolution: str):
    urls = []
    error_urls = []
    path_list = []
    message = "NotFound !!!"
    status = True
    if url_type == UrlType.solo:
        urls.append(url)
    else:
        playlist = Playlist(url)
        for video_url in playlist.video_urls:
            urls.append(video_url)
    for url in urls:
        print(f"Processing URL: {url}")
        res = await download_youtube_video(url, resolution)
        print("response: " + res.message)
        if res.status == False:
            error_urls.append(url)
        else:
            path_list.append(res.file_path)
    if error_urls:
        url_txt = [' [ ' + g_url + ' ] ' for g_url in error_urls]
        url_txt = ''.join(url_txt)
        message = "Cant Download Some Videos: " + url_txt
        status = False
    if status:
        zip_filename = "Download/" + datetime.datetime.now().isoformat() + '.zip'
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for file in path_list:
                zipf.write(file, os.path.basename(file))
                os.remove(file)
        return zip_filename
    raise HTTPException(status_code=400, detail=message)
