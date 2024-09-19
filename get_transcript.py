import json
import sys
from yt_dlp import YoutubeDL
import re
import time


def get_video_transcript(transcript):
    # Initialize an empty string to hold the output text
    output_text = ""

    # Split the transcript into lines
    lines = transcript.splitlines()

    # Variable to store the previous line for comparison
    previous_line = ""

    # Loop through each line in the transcript
    for line_number, line in enumerate(lines, start=1):
        # Skip the first 4 lines
        if line_number <= 4:
            continue

        # Skip empty lines or lines containing only whitespace
        if not line.strip():
            continue

        # Skip lines that contain patterns such as timestamps, brackets, or HTML tags
        if re.search(r"^$|-->|[\[\]]|<", line):
            continue

        # Skip duplicate lines (if the current line matches the previous one)
        if line == previous_line:
            continue

        # Add the line to output text
        output_text += line + "\n"

        # Update the previous line tracker
        previous_line = line

    # Return the cleaned transcript as a string (optional, for additional use)
    return output_text


def load_problems(file_path):
    with open(file_path, "r") as file:
        problems = json.load(file)
    return problems


if __name__ == "__main__":
    file_path = "problems.json"
    problems = load_problems(file_path)

    options = {
        "extract_flat": "discard_in_playlist",
        "fragment_retries": 10,
        "ignoreerrors": "only_download",
        "noprogress": True,
        "outtmpl": {"default": "%(id)s.%(ext)s"},
        "postprocessors": [
            {"key": "FFmpegConcat", "only_multi_video": True, "when": "playlist"}
        ],
        "quiet": True,
        "retries": 10,
        "simulate": False,
        "skip_download": True,
        "subtitlesformat": "vtt",
        "subtitleslangs": ["en"],
        "writeautomaticsub": True,
        "writesubtitles": True,
    }

    with YoutubeDL(options) as ydl:
        for problem in problems:
            url = "https://www.youtube.com/watch?v=" + problem["Video"]
            # check if the transcript is already downloaded to the local directory
            try:
                with open(problem["Video"] + ".en.vtt", "r") as file:
                    print(f"Transcript already downloaded for {problem['Name']}")
            except FileNotFoundError:
                print(f"Starting to download the transcript for {problem['Name']}")
                ydl.download([url])
                print("Transcript downloaded successfully")
                # Add a delay to avoid getting blocked by YouTube
                time.sleep(2)
            
            # Get the transcript from the downloaded file
            print(f"Cleaning the transcript for {problem['Name']}")
            cleaned_transcript = ""
            try:
                with open(problem["Video"] + ".en.vtt", "r") as file:
                    transcript = file.read()
                    cleaned_transcript = get_video_transcript(transcript)
                    print(f"Transcript cleaned successfully for {problem['Name']}")
            except FileNotFoundError:
                print(f"Transcript not found for {problem['Name']}")
                continue
            
            # Check if the cleaned transcript already exists
            try:
                with open(problem["Video"] + ".en.txt", "r") as file:
                    print(f"Cleaned transcript already exists for {problem['Name']}")
            except FileNotFoundError:
                print(f"Writing the cleaned transcript for {problem['Name']}")
                with open(problem["Video"] + ".en.txt", "w") as file:
                    file.write(cleaned_transcript)
    
    with open("problems_with_transcript.json", "w") as file:
        json.dump(problems, file, indent=4)
        print("Problems updated successfully")
