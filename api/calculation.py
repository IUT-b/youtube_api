import os

import ffmpeg
import requests
import youtube_dl
from flask import jsonify


def classification(request):
    #音楽を取得するYouTubeのURL
    url = request.json["url"]
    #音楽を保存するファイル名
    music_path = "ytmusic.mp3"

    #YouTubeから音楽を抽出して保存
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": "./" + music_path,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    #Lolipopのサーバーへ保存した音楽ファイルを転送
    url = "https://iut-b.main.jp/up2"
    files = {"file": open(music_path, "rb")}
    res = requests.post(url, files=files)

    return jsonify({"new_video_path": res.status_code}), 201
