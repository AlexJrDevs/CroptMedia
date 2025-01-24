# CroptMedia

A Python program that allows users to create TikTok-style videos by combining two video sources: one for gameplay (bottom) and one for a talking person (top). Customize with features like tracking the speaker, clip selection, transcription, and text editing.

---

## Features

- **Combine Two Videos**: Merge a gameplay video at the bottom and another video at the top for a TikTok-style video.
- **Talking Head Tracking**: Optionally track the person in the top video or keep the view static.
- **Clip Selection**: Choose specific sections of each video to include in the final edit.
- **Multiple Clips**: Add multiple clips for a dynamic final video.
- **Transcription and Text Editing**: Automatically generate a transcript with options to edit and style text for subtitles or annotations.

## Requirements

- **Python 3.7+**
- **FFmpeg** (for video processing)
- **OpenCV** (for face tracking)
- **Speech Recognition API** (optional, for transcription)
- **PyDub** (for audio manipulation)

Install dependencies with:

```bash
pip install -r requirements.txt
