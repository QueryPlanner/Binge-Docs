#!/usr/bin/env python3
import re
import sys
import os
from kokoro_onnx import Kokoro
import soundfile as sf
import numpy as np

def clean_markdown(text):
    """
    Clean markdown text to make it suitable for TTS.
    Removes problematic characters and formatting.
    """
    # Remove FastAPI-specific embedded code references
    text = re.sub(r'\{\*[^*]*\*\}', '', text)
    
    # Remove markdown headers (# ## ###, etc.) but keep the text
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    
    # Remove code blocks (```...```)
    text = re.sub(r'```[\s\S]*?```', '', text)
    
    # Remove inline code backticks but keep the content (`...` -> ...)
    text = re.sub(r'`([^`]*)`', r'\1', text)
    
    # Remove HTML-like tags and abbreviations
    text = re.sub(r'<[^>]*>', '', text)
    
    # Remove markdown links but keep the text [text](url) -> text
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    
    # Remove markdown emphasis (* ** _ __)
    text = re.sub(r'[*_]{1,2}([^*_]*)[*_]{1,2}', r'\1', text)
    
    # Replace problematic characters
    text = text.replace('\\', ' ')
    text = text.replace('/', ' ')
    text = text.replace('|', ' ')
    text = text.replace('+', ' plus ')
    text = text.replace('&', ' and ')
    
    # Remove comment blocks (/// ... ///)
    text = re.sub(r'///[\s\S]*?///', '', text)
    
    # Remove markdown tables (lines with |)
    lines = text.split('\n')
    filtered_lines = []
    for line in lines:
        if '|' not in line or not line.strip().startswith('|'):
            filtered_lines.append(line)
    text = '\n'.join(filtered_lines)
    
    # Remove excessive whitespace and empty lines
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
    text = re.sub(r'\s+', ' ', text)
    
    # Remove remaining special characters that might cause issues
    text = re.sub(r'[{}()\[\]<>]', '', text)
    
    return text.strip()

def chunk_text(text, max_length=1000):
    """Split text into smaller chunks for TTS processing."""
    sentences = text.replace('\n', ' ').split('.')
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        sentence_length = len(sentence)
        
        if current_length + sentence_length > max_length and current_chunk:
            chunks.append('. '.join(current_chunk) + '.')
            current_chunk = [sentence]
            current_length = sentence_length
        else:
            current_chunk.append(sentence)
            current_length += sentence_length
    
    if current_chunk:
        chunks.append('. '.join(current_chunk) + '.')
    
    return chunks

def markdown_to_speech(file_path, output_path=None, voice='af_heart', lang_code='a'):
    """
    Convert a markdown file to speech.
    
    Args:
        file_path: Path to the markdown file
        output_path: Output audio file path (optional)
        voice: Voice to use for TTS
        lang_code: Language code for TTS (not used in kokoro-onnx)
    """
    # Read the markdown file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return False
    except Exception as e:
        print(f"Error reading file: {e}")
        return False
    
    # Clean the markdown
    cleaned_text = clean_markdown(text)
    
    if not cleaned_text.strip():
        print("Warning: No text content found after cleaning.")
        return False
    
    print(f"Original text length: {len(text)} characters")
    print(f"Cleaned text length: {len(cleaned_text)} characters")
    print("\nFirst 200 characters of cleaned text:")
    print(cleaned_text[:200] + "..." if len(cleaned_text) > 200 else cleaned_text)
    print("\n" + "="*50)
    
    # Initialize the TTS model
    try:
        # Look for model files in kokoro-tts directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        kokoro_dir = os.path.join(script_dir, 'kokoro-tts')
        model_path = os.path.join(kokoro_dir, 'kokoro-v1.0.onnx')
        voices_path = os.path.join(kokoro_dir, 'voices-v1.0.bin')
        
        if not os.path.exists(model_path):
            print(f"Error: Model file not found at {model_path}")
            return False
        if not os.path.exists(voices_path):
            print(f"Error: Voices file not found at {voices_path}")
            return False
            
        kokoro = Kokoro(model_path, voices_path)
        print(f"Initialized Kokoro TTS with voice: {voice}")
        
    except Exception as e:
        print(f"Error initializing TTS model: {e}")
        return False
    
    # Generate speech
    try:
        # Split text into chunks for better processing
        chunks = chunk_text(cleaned_text, max_length=800)
        print(f"Processing {len(chunks)} text chunks...")
        
        audio_chunks = []
        
        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i+1}/{len(chunks)}")
            try:
                # Generate audio for this chunk
                audio = kokoro.create(chunk, voice=voice, speed=1.0)
                audio_chunks.append(audio)
            except Exception as e:
                print(f"Error processing chunk {i+1}: {e}")
                continue
        
        if not audio_chunks:
            print("No audio chunks generated")
            return False
        
        # Concatenate all audio chunks
        full_audio = np.concatenate(audio_chunks, axis=0)
        
        # Determine output path
        if output_path is None or output_path.strip() == "":
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            output_path = f"{base_name}_speech.wav"
        
        # Save the audio file
        sf.write(output_path, full_audio, 24000)
        print(f"\nGenerated audio file: {output_path}")
        print(f"Total chunks processed: {len(audio_chunks)}")
        print(f"Audio duration: {len(full_audio) / 24000:.2f} seconds")
        return True
        
    except Exception as e:
        print(f"Error during TTS generation: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python md_to_speech.py <markdown_file> [output_file] [voice] [lang_code]")
        print("Example: python md_to_speech.py docs/tutorial.md tutorial_speech.wav af_heart a")
        sys.exit(1)
    
    file_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2].strip() else None
    voice = sys.argv[3] if len(sys.argv) > 3 else 'af_heart'
    lang_code = sys.argv[4] if len(sys.argv) > 4 else 'a'
    
    print(f"Converting '{file_path}' to speech...")
    print(f"Voice: {voice}, Language: {lang_code}")
    
    success = markdown_to_speech(file_path, output_path, voice, lang_code)
    
    if success:
        print("Conversion completed successfully!")
    else:
        print("Conversion failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 