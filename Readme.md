# YouTube Video Downloader API

A FastAPI backend service for downloading YouTube videos, packaged in Docker.

## Prerequisites

- Docker installed
- 500MB+ free disk space

## Quick Start

### 1. Build the Docker Image
```bash
docker build -t yt-downloader .
```

### 2. Run the Container
```bash
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/downloads:/app/downloads \
  --name yt-dl-server \
  yt-downloader
```
### 3. Using the API
```bash
curl -L "http://localhost:8000/download?url=YOUTUBE_URL&format=mp4" --output video.mp4
curl -L "http://localhost:8000/download?url=YOUTUBE_URL&format=mp3" --output audio.mp3
```

### Important Notes
Downloaded files are saved to ./downloads on your host machine

The service runs on port 8000 by default

First run may take longer as dependencies are installed
