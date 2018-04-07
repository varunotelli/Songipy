import requests, zipfile, io, os
ffmpeg_url = "https://github.com/vot/ffbinaries-prebuilt/releases/download/v3.2/ffmpeg-3.2-win-32.zip"
ffprobe_url = "https://github.com/vot/ffbinaries-prebuilt/releases/download/v3.2/ffprobe-3.2-win-32.zip"

file1 = requests.get(ffmpeg_url)
zipfile1 = zipfile.ZipFile(io.BytesIO(file1.content))
zipfile1.extractall()

file2 = requests.get(ffprobe_url)
zipfile2 = zipfile.ZipFile(io.BytesIO(file2.content))
zipfile2.extractall()
