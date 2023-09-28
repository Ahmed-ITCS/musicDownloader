import os
import re
import requests
import yt_dlp


def get_video_title(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.text
        title_match = re.search(r'<title>(.*?) - YouTube</title>', content, re.IGNORECASE)
        if title_match:
            return title_match.group(1)
        else:
            return "Untitled"
    except Exception as e:
        print(f"Unable to fetch video title: {str(e)}")
        return "Untitled"
def download_youtube_audio(url, output_dir="."):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        video_title = get_video_title(url)
        ydl_opts['outtmpl'] = os.path.join(output_dir, f"{video_title}.%(ext)s")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print(f"Audio from {url} downloaded successfully as '{video_title}.mp3'.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
def process_youtube_links_from_file(file_path, output_dir="."):
    with open(file_path, "r") as file:
        for line in file:
            youtube_url = line.strip()
            if youtube_url:
                download_youtube_audio(youtube_url, output_dir)

if __name__ == "__main__":
    input_file_path = input("Enter the path to the text file containing YouTube links: ")
    output_directory = input("Enter the output directory (press Enter for the current directory): ").strip()
    if not output_directory:
        output_directory = "."
    
    process_youtube_links_from_file(input_file_path, output_directory)
