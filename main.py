from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
import yt_dlp
import os
from urllib.parse import urlparse, parse_qs
import re

app = FastAPI()
DOWNLOAD_DIR = "downloads"  # Directory to save files

def extract_video_id(url: str) -> str:
    """Extracts YouTube video ID from any URL format."""
    if "youtube.com/watch" in url:
        parsed = urlparse(url)
        video_id = parse_qs(parsed.query).get("v", [None])[0]
        if video_id:
            return video_id
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("&")[0].split("?")[0]
    else:
        regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
        match = re.search(regex, url)
        if match:
            return match.group(1)
    raise HTTPException(status_code=400, detail="Invalid YouTube URL")

def download_with_ytdlp(url: str, format: str = "mp4") -> str:
    """Downloads the video/audio using yt-dlp and returns the file path."""
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    ydl_opts = {
        "quiet": True,
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" if format == "mp4" else "bestaudio/best",
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}] if format == "mp3" else [],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename

@app.get("/download")
async def download_video(
    url: str = Query(..., description="YouTube URL"),
    format: str = Query("mp4", description="Format (mp4/mp3)"),
):
    """Downloads the video/audio and sends the file."""
    try:
        video_id = extract_video_id(url)
        youtube_url = f"https://youtube.com/watch?v={video_id}"
        file_path = download_with_ytdlp(youtube_url, format)
        
        return FileResponse(
            file_path,
            media_type="video/mp4" if format == "mp4" else "audio/mpeg",
            filename=os.path.basename(file_path),
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)