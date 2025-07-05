#!/bin/bash

# Markdown to Speech Converter
# Usage: ./convert_md_to_speech.sh <markdown_file> [output_file] [voice] [lang_code]

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to display usage
show_usage() {
    echo -e "${BLUE}Markdown to Speech Converter${NC}"
    echo ""
    echo "Usage: $0 <markdown_file> [output_file] [voice] [lang_code]"
    echo ""
    echo "Arguments:"
    echo "  markdown_file    Path to the markdown file to convert (required)"
    echo "  output_file      Output audio file path (optional, auto-generated if not provided)"
    echo "  voice           Voice to use for TTS (optional, default: af_heart)"
    echo "  lang_code       Language code for TTS (optional, default: a)"
    echo ""
    echo "Environment Variables:"
    echo "  USE_GPU=1        Force enable GPU acceleration (may be slower for small models)"
    echo ""
    echo "Examples:"
    echo "  $0 fastapi/docs/en/docs/tutorial/path-params-numeric-validations.md"
    echo "  $0 docs/tutorial.md tutorial_speech.wav"
    echo "  $0 docs/tutorial.md tutorial_speech.wav af_heart a"
    echo "  USE_GPU=1 $0 docs/tutorial.md  # Force GPU acceleration"
    echo ""
    echo "Available voices: af_heart, af_sky, af_bella, af_sarah, etc."
    echo "Language codes: a (auto), en (English), etc."
    echo ""
    echo "Note: GPU acceleration is disabled by default as CPU is often faster for small models."
}

# Check if help is requested
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    show_usage
    exit 0
fi

# Check if at least one argument is provided
if [ $# -lt 1 ]; then
    echo -e "${RED}Error: Missing required argument${NC}"
    echo ""
    show_usage
    exit 1
fi

# Get arguments
MARKDOWN_FILE="$1"
OUTPUT_FILE="$2"
VOICE="${3:-af_heart}"
LANG_CODE="${4:-a}"

# Check if markdown file exists
if [ ! -f "$MARKDOWN_FILE" ]; then
    echo -e "${RED}Error: Markdown file '$MARKDOWN_FILE' not found${NC}"
    exit 1
fi

# Check if Python script exists
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/md_to_speech.py"

if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo -e "${RED}Error: Python script 'md_to_speech.py' not found in $SCRIPT_DIR${NC}"
    echo "Make sure md_to_speech.py is in the same directory as this script."
    exit 1
fi

# Display conversion info
echo -e "${BLUE}=== Markdown to Speech Converter ===${NC}"
echo "Input file: $MARKDOWN_FILE"
echo "Voice: $VOICE"
echo "Language: $LANG_CODE"
if [ -n "$OUTPUT_FILE" ]; then
    echo "Output file: $OUTPUT_FILE"
else
    echo "Output file: Auto-generated"
fi
echo ""

# Check if GPU acceleration is requested
GPU_ACCELERATION=""
if [[ "$USE_GPU" == "1" ]]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # Check if it's Apple Silicon (M1/M2/M3/M4)
        ARCH=$(uname -m)
        if [[ "$ARCH" == "arm64" ]]; then
            echo -e "${BLUE}GPU acceleration enabled (Apple Silicon detected)${NC}"
            GPU_ACCELERATION="PYTORCH_ENABLE_MPS_FALLBACK=1"
        else
            echo -e "${BLUE}GPU acceleration requested but not supported on Intel Mac${NC}"
        fi
    else
        echo -e "${BLUE}GPU acceleration requested but not implemented for this OS${NC}"
    fi
else
    echo -e "${BLUE}Using CPU for inference (faster for small models like Kokoro-82M)${NC}"
fi

# Run the Python script
echo -e "${BLUE}Starting conversion...${NC}"
if [ -n "$OUTPUT_FILE" ]; then
    if [ -n "$GPU_ACCELERATION" ]; then
        env $GPU_ACCELERATION python "$PYTHON_SCRIPT" "$MARKDOWN_FILE" "$OUTPUT_FILE" "$VOICE" "$LANG_CODE"
    else
        python "$PYTHON_SCRIPT" "$MARKDOWN_FILE" "$OUTPUT_FILE" "$VOICE" "$LANG_CODE"
    fi
else
    if [ -n "$GPU_ACCELERATION" ]; then
        env $GPU_ACCELERATION python "$PYTHON_SCRIPT" "$MARKDOWN_FILE" "" "$VOICE" "$LANG_CODE"
    else
        python "$PYTHON_SCRIPT" "$MARKDOWN_FILE" "" "$VOICE" "$LANG_CODE"
    fi
fi

# Check if conversion was successful
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Conversion completed successfully!${NC}"
else
    echo -e "${RED}✗ Conversion failed!${NC}"
    exit 1
fi 