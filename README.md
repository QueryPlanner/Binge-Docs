# 🎧 Binge docs

Turn your favorite documentation into your personal podcast! 📚➡️🎵

This magical tool converts markdown files to speech using the Kokoro TTS engine. It's like having a personal narrator for all your docs - perfect for learning on the go, during commutes, or when you just want to give your eyes a break! 

The tool automatically cleans markdown content to remove all the techy bits that would make your TTS sound like a robot having a syntax error. 🤖✨

## 🎥 See It In Action

https://x.com/VectorQl/status/1941400473552183762

*Watch the magic happen - from boring markdown to beautiful audio!*

> **🌟 Sneak Peek**: The demo video shows the complete workflow of converting FastAPI documentation to speech, including the cleaning process and audio generation. It's like watching a documentary about documentation transformation!

## 📁 The Cast & Crew

- `md_to_speech.py` - The star of the show! Python script that handles markdown cleaning and TTS conversion
- `.sh` - Your friendly shell script wrapper for easy one-liner magic

## 🚀 Ready to Binge?

### Quick Start (Because who has time to read?)
```bash
# Convert any markdown file (we'll name it for you!)
./.sh path/to/file.md

# Want to name your masterpiece?
./.sh path/to/file.md my_awesome_podcast.wav

# Feeling fancy with different voices?
./.sh path/to/file.md output_audio.wav af_sky en
```

### Real Examples (From the wild!)
```bash
# Turn FastAPI docs into your commute companion
./.sh fastapi/docs/en/docs/tutorial/path-params-numeric-validations.md

# Create your own tutorial series
./.sh fastapi/docs/en/docs/tutorial/path-params-numeric-validations.md tutorial.wav

# Switch up the voice for variety
./.sh docs/tutorial.md tutorial.wav af_bella a
```

### 🎛️ Command Line Options (Your controls)

1. `markdown_file` (required) - Path to your markdown treasure to convert
2. `output_file` (optional) - Name your audio masterpiece (we'll auto-generate if you're feeling lazy)
3. `voice` (optional) - Pick your narrator (default: af_heart - they're lovely!)
4. `lang_code` (optional) - Language code for TTS (default: a for auto-magic detection)

### 🎭 Voice Cast (Pick your narrator!)
- `af_heart` (default) - The reliable friend
- `af_sky` - Dreamy and smooth
- `af_bella` - Elegant and clear
- `af_sarah` - Warm and friendly
- And many more voices waiting to tell your story...

## 🧹 The Magic Cleanup (What we sweep under the rug)

Our intelligent script automatically declutters your markdown so your ears don't have to suffer through:

- 🔢 Markdown headers (`#`, `##`, etc.) - keeps the juicy text, ditches the hashtags
- 💻 Code blocks (` ``` `) - because nobody wants to hear "backtick backtick backtick"
- 🔤 Inline code (`` ` ``) - saves you from robotic spelling sessions
- ⚡ FastAPI-specific embedded code references (`{* ... *}`) - no more cryptic curly braces
- 🏷️ HTML tags and abbreviations - clean, readable content only
- 🔗 Markdown links - keeps the text, loses the messy URLs
- ✨ Markdown emphasis (`*`, `**`, `_`, `__`) - the meaning stays, the asterisks go bye-bye
- 🚫 Problematic characters (`\`, `/`, `|`, etc.) - no more TTS hiccups
- 💬 Comment blocks (`/// ... ///`) - internal notes stay internal
- 📊 Markdown tables - because tables sound terrible when read aloud
- 🎵 Special characters that make TTS sound like a confused robot

## 🎬 What to Expect (The behind-the-scenes show)

When you run the script, you'll get a front-row seat to the magic:
- 📏 Original vs cleaned text lengths (see the transformation!)
- 👀 Preview of your cleaned text (sneak peek of what gets narrated)
- 🎵 Processing progress for each audio chunk (watch the magic happen)
- 📋 Final audio file stats (duration, file size, and all the good stuff)

## 🛠️ What You Need (The usual suspects)

- Python 3.x (the brain of the operation)
- Kokoro TTS library (the voice actor)
- soundfile library (the recording engineer)
- numpy library (the math wizard)

## 🎯 Battle-Tested Results

Successfully converted FastAPI documentation into a smooth 251-second audio journey! From dense technical docs to an engaging audio experience - that's the power of binge-worthy documentation! 🎧✨ 
