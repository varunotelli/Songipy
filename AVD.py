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

from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

import sys
import argparse
from pydub import AudioSegment
import os
#search=sys.argv[2]
#mode=sys.argv[1]
parser=argparse.ArgumentParser()
parser.add_argument("-m","--mode",help="mode audio for audio. video for video",type=str)
parser.add_argument("-s","--song",help="Name of song",type=str)
parser.add_argument("-f","--folder",help="Folder to save",default=".",type=str)
parser.add_argument("-n","--name", help="Provide a name for the file", nargs='?' ,default=None,type=str)
parser.add_argument("-t","--trim", help="Trim audio file y or n?",nargs='?' ,default="n",type=str)
parser.add_argument("-st","--start",help="Enter start time",nargs='?' ,default=None,type=str)
parser.add_argument("-fin","--finish",help="Enter finish time",nargs='?' ,default=None,type=str)


args=parser.parse_args()
html=requests.get("https://www.youtube.com/results?search_query="+args.song).content
soup=BeautifulSoup(html,"html.parser")
#for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
#print(soup.findAll(attrs={'class':'yt-uix-tile-link'})[0]['title'])
title=soup.findAll(attrs={'class':'yt-uix-tile-link'})[0]['title']
#title=""
print("https://www.youtube.com"+soup.findAll(attrs={'class':'yt-uix-tile-link'})[0]["href"])
link="https://www.youtube.com"+soup.findAll(attrs={'class':'yt-uix-tile-link'})[0]["href"]
#print("name="+args.name)
if args.mode == 'audio':
	if args.name:
		title=args.name
		ydl_opts = {
		    'format': 'bestaudio/best',
		    'postprocessors': [{
		        'key': 'FFmpegExtractAudio',
		        'preferredcodec': 'mp3',
		        'preferredquality': '192',
		    }],
		    'outtmpl':args.folder+'/'+args.name+'.%(ext)s'
	}
	else:
		#title='%(title)s'
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

	if not args.name:
		#title='%(title)s'
		ydl_opts={'outtmpl':args.folder+'/%(title)s.%(ext)s'}

	else:
		title=args.name
		#title=soup.findAll(attrs={'class':'yt-uix-tile-link'})[0]['title']
		ydl_opts={'outtmpl':args.folder+'/'+title+'.%(ext)s'}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    title=ydl.extract_info(link,download=True).get('title',None)

print(title)

if args.trim=="y":
	if args.mode=="audio":
		st_minute=int(args.start.split(':')[0])
		st_sec=int(args.start.split(':')[1])
		st_time=(st_minute*60*1000)+(st_sec*1000)
		f_minute=int(args.finish.split(':')[0])
		f_sec=int(args.finish.split(':')[1])
		f_time=(f_minute*60*1000)+(f_sec*1000)+1000

		song = AudioSegment.from_mp3(args.folder+'/'+title.replace("|","_")+".mp3")    
		song=song[st_time:f_time]
		song.export(title.replace("|","_")+".mp3",format="mp3")
	elif args.mode=="video":
		st_minute=int(args.start.split(':')[0])
		st_sec=int(args.start.split(':')[1])
		st_time=(st_minute*60)+(st_sec)
		f_minute=int(args.finish.split(':')[0])
		f_sec=int(args.finish.split(':')[1])
		f_time=(f_minute*60)+(f_sec)
		#clip=VideoFileClip(title.replace("|","_")+".webm").subclip(st_time,f_time)
		#clip.write_videofile(title.replace("|","_")+".webm")
		ffmpeg_extract_subclip(args.folder+"/"+title.replace("|","_")+".webm",st_time,f_time, targetname="test1.webm")

