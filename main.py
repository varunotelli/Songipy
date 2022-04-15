from __future__ import unicode_literals
import os
import youtube_dl
import requests
from bs4 import BeautifulSoup
from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.io.VideoFileClip import VideoFileClip
import sys
import argparse
from pydub import AudioSegment

def audio_trim(folder,title,start="00:00",fin=None):

	st_minute=int(start.split(':')[0])
	st_sec=int(start.split(':')[1])
	st_time=(st_minute*60*1000)+(st_sec*1000)
	f_minute=int(fin.split(':')[0])
	f_sec=int(fin.split(':')[1])
	f_time=(f_minute*60*1000)+(f_sec*1000)

	song = AudioSegment.from_mp3(folder+'/'+title.replace("|","_")+".mp3")    
	song=song[st_time:f_time]
	song.export(folder+'/'+title.replace("|","_")+"[trimmed].mp3",format="mp3")

def video_trim(folder,title,start="0:00",fin=None):
	st_minute=int(start.split(':')[0])
	st_sec=int(start.split(':')[1])
	st_time=(st_minute*60)+(st_sec)
	f_minute=int(fin.split(':')[0])
	f_sec=int(fin.split(':')[1])
	f_time=(f_minute*60)+(f_sec)
	ffmpeg_extract_subclip(folder+"/"+title.replace("|","_")+".mp4",st_time,f_time, 
		targetname=folder+"/"+title.replace("|","_")+"[trimmed].mp4")


def main():
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
	#print(html)
	soup=BeautifulSoup(html,"html.parser")
	#title=soup.findAll(attrs={'class':'yt-uix-tile-link'})[0]['title']
	from youtubesearchpython import VideosSearch
	videosSearch = VideosSearch(args.song, limit = 5)
	for i in range(0,5):
		print(str(i+1)+"."+ videosSearch.result()['result'][i]['title'])
	ch=int(input("Enter choice "))
	#print("https://www.youtube.com"+soup.findAll(attrs={'class':'yt-uix-tile-link'})[ch-1]["href"])
	link=videosSearch.result()['result'][ch-1]['link']
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
			ydl_opts={'format':'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
			'outtmpl':args.folder+'/%(title)s.%(ext)s'}

		else:
			title=args.name
			ydl_opts={'format':'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
			'outtmpl':args.folder+'/'+title+'.%(ext)s'}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	    title=ydl.extract_info(link,download=True).get('title',None)

	print(title)

	ch2=input("Would you like to trim the "+args.mode+"?(y/n) ")
	if ch2=="y":
		start=input("Enter start time of trim ")
		if not start:
			start="0:00"

		fin=input("Enter finish time of trim ")
		if args.mode=="audio":

			
			if not fin:
				song=AudioSegment.from_mp3(args.folder+'/'+title.replace("|","_")+".mp3")
				minutes=int(song.duration_seconds/60)
				secs=int(song.duration_seconds%60)
				fin=str(minutes)+":"+str(secs)
			print("Trimming....")
			audio_trim(args.folder,title,start,fin)
		elif args.mode=="video":
			if not fin:
				minutes=int(VideoFileClip(args.folder+"/"+title+".mp4").duration/60)
				secs=int(VideoFileClip(args.folder+"/"+title+".mp4").duration%60)
				print(str(minutes)+":"+str(secs))
				fin=str(minutes)+":"+str(secs)
			print("Trimming....")
			video_trim(args.folder,title,start,fin)

		print("Trim Successful!")	

if __name__=='__main__':
	os.environ["PATH"]+=os.pathsep+"./packages"
	main()