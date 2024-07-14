from __future__ import unicode_literals
import yt_dlp
import subprocess
import shutil
import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Download audio from youtube video')
    parser.add_argument('-u', '--url', required=True, help='URL of the YouTube video')
    return parser.parse_args()

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'output.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
    }],
}

def download_from_url(url):
    if not os.path.exists("./process"):
        os.mkdir("./process")
    
    # Download audio using yt_dlp
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    ydl.download([url])
    
    # Find the downloaded file
    downloaded_file = None
    for file in os.listdir():
        if file.endswith('.wav'):
            downloaded_file = file
            break
    
    if downloaded_file:
        output_file = 'output.wav'
        
        # If ffmpeg conversion is needed
        if downloaded_file != output_file:
            try:
                subprocess.run(['ffmpeg', '-i', downloaded_file, output_file], check=True)
                os.remove(downloaded_file)
            except subprocess.CalledProcessError as e:
                print(f"Error occurred while running ffmpeg: {e}")
                return
        
        # Move the output file to the process directory
        if os.path.exists(f"./process/{output_file}"):
            os.remove(f"./process/{output_file}")
        shutil.move(output_file, f"./process/{output_file}")

if __name__ == "__main__":
    args = parse_args()
    download_from_url(args.url)
