#!/bin/bash

# Stream Sapiens PDF from specific page using existing kokoro-tts --stream functionality
# Usage: ./stream_sapiens_from_page.sh <start_page> [end_page] [voice] [speed]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PDF_PATH="$SCRIPT_DIR/Books/sapiens.pdf"
EXTRACT_SCRIPT="$SCRIPT_DIR/extract_pages.py"
KOKORO_DIR="$SCRIPT_DIR/kokoro-tts"

# Check if start page is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <start_page> [end_page] [voice] [speed]"
    echo ""
    echo "Examples:"
    echo "  $0 50                    # Stream from page 50 to end"
    echo "  $0 50 100               # Stream from page 50 to 100"
    echo "  $0 50 100 af_sarah      # Stream with specific voice"
    echo "  $0 50 100 af_sarah 1.2  # Stream with voice and speed"
    echo ""
    echo "Available voices:"
    cd "$KOKORO_DIR" && ./kokoro-tts --help-voices
    exit 1
fi

START_PAGE=$1
END_PAGE=${2:-""}
VOICE=${3:-""}
SPEED=${4:-"1.0"}

# Build kokoro-tts command
KOKORO_CMD="./kokoro-tts /dev/stdin --stream --speed $SPEED"

if [ -n "$VOICE" ]; then
    KOKORO_CMD="$KOKORO_CMD --voice $VOICE"
fi

echo "📖 Streaming Sapiens from page $START_PAGE${END_PAGE:+ to page $END_PAGE}"
echo "🎵 Using kokoro-tts streaming with speed: $SPEED${VOICE:+, voice: $VOICE}"
echo "⏯️  Press Ctrl+C to stop streaming"
echo ""

# Execute: extract pages and pipe to kokoro-tts streaming
if [ -n "$END_PAGE" ]; then
    python "$EXTRACT_SCRIPT" "$PDF_PATH" "$START_PAGE" --end-page "$END_PAGE" | (cd "$KOKORO_DIR" && eval "$KOKORO_CMD")
else
    python "$EXTRACT_SCRIPT" "$PDF_PATH" "$START_PAGE" | (cd "$KOKORO_DIR" && eval "$KOKORO_CMD")
fi 