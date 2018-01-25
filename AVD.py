from __future__ import unicode_literals
import pip
try:
	import youtube_dl
except:
	pip.main(['install','youtube_dl'])
	import youtube_dl

try:
	import requests
except:
	pip.main(['install','requests'])
	import requests

try:
	from bs4 import BeautifulSoup
except:
	pip.main(['install','bs4'])
	from bs4 import BeautifulSoup

import sys
import argparse

#search=sys.argv[2]
#mode=sys.argv[1]
parser=argparse.ArgumentParser()
parser.add_argument("-m","--mode",help="mode -a for audio. -v for video",type=str)
parser.add_argument("-s","--song",help="Name of song",type=str)
parser.add_argument("-f","--folder",help="Folder to save",type=str)
args=parser.parse_args()
html=requests.get("https://www.youtube.com/results?search_query="+args.song).content
soup=BeautifulSoup(html,"html.parser")
#for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
print("https://www.youtube.com"+soup.findAll(attrs={'class':'yt-uix-tile-link'})[0]["href"])
link="https://www.youtube.com"+soup.findAll(attrs={'class':'yt-uix-tile-link'})[0]["href"]
if args.mode == 'audio':
	ydl_opts = {
	    'format': 'bestaudio/best',
	    'postprocessors': [{
	        'key': 'FFmpegExtractAudio',
	        'preferredcodec': 'mp3',
	        'preferredquality': '192',
	    }],
	    'outtmpl':args.folder+'/%(title)s.%(ext)s'
	}
elif args.mode=='video':
	ydl_opts={'outtmpl':args.folder+'/%(title)s.%(ext)s'}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([link])
    