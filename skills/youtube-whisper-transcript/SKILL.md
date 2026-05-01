---
name: youtube-whisper-transcript
description: Download a YouTube video's audio track and transcribe it with Whisper, then save a transcript file for summarization or study. Use when the user shares a YouTube URL and asks for transcription, notes, a text brief, or a transcript-based analysis.
---

# YouTube Whisper Transcript

Convert a YouTube video into text in a repeatable way.

## What this skill does

1. Download audio from a YouTube URL
2. Save the audio into a working folder
3. Transcribe the audio with Whisper via OpenAI-compatible API
4. Save the transcript as a text file
5. Return file paths and a short status summary

## Requirements

Before using this skill, confirm:
- the YouTube URL
- whether audio-only download is enough (default: yes)
- whether the user wants only the transcript or also a summary

## Default workflow

Run the bundled script:

```bash
{baseDir}/scripts/youtube_whisper_transcript.sh "<youtube_url>"
```

Optional output directory:

```bash
{baseDir}/scripts/youtube_whisper_transcript.sh "<youtube_url>" "./video-analysis"
```

## Output contract

After the script finishes, report:
- audio file path
- transcript file path
- whether the transcript succeeded
- any known limitation (missing subtitles, Whisper API failure, yt-dlp failure)

## When to use references

Read `references/troubleshooting.md` when:
- yt-dlp fails
- subtitles are missing and you need fallback logic
- Whisper returns auth or API errors
- the user asks why a transcript could not be produced

## Notes

- Prefer transcript production before summarization.
- If the transcript fails, do not pretend the video was fully understood.
- If the user wants a detailed brief, first generate the transcript, then analyze the text.
