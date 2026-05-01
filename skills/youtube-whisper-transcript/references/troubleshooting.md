# Troubleshooting

## 1. `yt-dlp not found in PATH`
Install `yt-dlp` first or make sure it is available in the runtime PATH.

## 2. No subtitles available
This skill does not depend on YouTube subtitles. It downloads audio and transcribes the audio with Whisper.

## 3. Whisper API returns 401 / invalid key
The OpenAI-compatible transcription endpoint is not authenticated correctly.
Check:
- `OPENAI_API_KEY`
- OpenClaw config entries for Whisper / OpenAI
- any custom `OPENAI_BASE_URL`

## 4. Download succeeds but transcript file is missing
Likely causes:
- the transcription helper failed
- API auth failed
- output path permissions are wrong

## 5. Transcript quality is poor
Possible fixes:
- provide `--language` in the Whisper helper if the language is known
- use cleaner audio when possible
- post-process the transcript in a separate summarization step instead of forcing one-pass interpretation

## 6. Why not summarize directly from the video?
Because transcript-first is more reliable, auditable, and reusable. Once text exists, it can be reviewed, indexed, and summarized repeatedly.
