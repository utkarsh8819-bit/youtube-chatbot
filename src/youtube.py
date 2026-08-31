from urllib.parse import urlparse, parse_qs

from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str) -> str:
    """Extract the YouTube video ID from a YouTube URL."""

    parsed_url = urlparse(url)

    # Normal YouTube URL:
    # https://www.youtube.com/watch?v=VIDEO_ID
    if parsed_url.hostname in {"www.youtube.com", "youtube.com", "m.youtube.com"}:
        video_id = parse_qs(parsed_url.query).get("v", [None])[0]

        if video_id:
            return video_id

    # Short YouTube URL:
    # https://youtu.be/VIDEO_ID
    if parsed_url.hostname == "youtu.be":
        video_id = parsed_url.path.strip("/")

        if video_id:
            return video_id

    raise ValueError("Invalid YouTube URL")


def get_transcript(url: str):
    """Fetch the best available transcript while preserving timestamps."""

    video_id = extract_video_id(url)

    api = YouTubeTranscriptApi()

    # Get all available transcripts
    transcript_list = api.list(video_id)

    # First preference: manually created English transcript
    for transcript in transcript_list:
        if transcript.language_code == "en" and not transcript.is_generated:
            return transcript.fetch().to_raw_data()

    # Second preference: generated English transcript
    for transcript in transcript_list:
        if transcript.language_code == "en":
            return transcript.fetch().to_raw_data()

    # Final fallback: use the first available transcript
    for transcript in transcript_list:
        return transcript.fetch().to_raw_data()

    raise ValueError("No transcript is available for this video.")