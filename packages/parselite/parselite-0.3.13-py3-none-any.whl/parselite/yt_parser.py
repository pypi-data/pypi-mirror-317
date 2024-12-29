import time
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter




class YoutubeExtractor:

    @staticmethod
    def get_video_id(url):
        return url.split("?v=")[-1]

    @staticmethod
    def extract(urls: list):
        urls = [YoutubeExtractor.get_video_id(url) for url in urls]
        results = []
        formatter = TextFormatter()
        for url in urls:
            # try:
            transcript = YouTubeTranscriptApi.get_transcript(url)
            transcript = formatter.format_transcript(transcript)
            results.append(transcript)
            # except:
            #     pass
        return results
