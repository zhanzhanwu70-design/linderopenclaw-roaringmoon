#!/usr/bin/env bash
set -euo pipefail

URL="${1:-}"
OUTDIR="${2:-./video-analysis}"

if [ -z "$URL" ]; then
  echo "Usage: $0 <youtube_url> [output_dir]" >&2
  exit 1
fi

mkdir -p "$OUTDIR"

if ! command -v yt-dlp >/dev/null 2>&1; then
  echo "yt-dlp not found in PATH" >&2
  exit 2
fi

AUDIO_TEMPLATE="$OUTDIR/%(id)s.%(ext)s"
yt-dlp -x --audio-format mp3 -o "$AUDIO_TEMPLATE" "$URL" >/tmp/youtube_whisper_download.log 2>&1 || {
  cat /tmp/youtube_whisper_download.log >&2
  exit 3
}

VIDEO_ID="$(yt-dlp --get-id "$URL" 2>/dev/null | head -n 1)"
if [ -z "$VIDEO_ID" ]; then
  echo "Could not determine YouTube video id" >&2
  exit 4
fi

AUDIO_FILE="$OUTDIR/$VIDEO_ID.mp3"
if [ ! -f "$AUDIO_FILE" ]; then
  echo "Expected audio file not found: $AUDIO_FILE" >&2
  exit 5
fi

TRANSCRIPT_FILE="$OUTDIR/$VIDEO_ID.txt"

if [ ! -f /app/skills/openai-whisper-api/scripts/transcribe.sh ]; then
  echo "Whisper transcribe helper not found" >&2
  exit 6
fi

bash /app/skills/openai-whisper-api/scripts/transcribe.sh "$AUDIO_FILE" --out "$TRANSCRIPT_FILE" >/tmp/youtube_whisper_transcribe.log 2>&1 || {
  cat /tmp/youtube_whisper_transcribe.log >&2
  exit 7
}

echo "AUDIO_FILE=$AUDIO_FILE"
echo "TRANSCRIPT_FILE=$TRANSCRIPT_FILE"
