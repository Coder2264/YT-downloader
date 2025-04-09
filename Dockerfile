# Use Python image
FROM python:3.13.3-slim-bullseye

# Install system dependencies (ffmpeg + cleanup)
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir fastapi uvicorn yt-dlp

# Create and set working directory
WORKDIR /app
COPY . .

# Create downloads directory
RUN mkdir -p /app/downloads

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]