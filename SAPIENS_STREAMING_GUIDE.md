# Stream Sapiens from Any Page - Using Kokoro TTS Built-in Streaming

This solution leverages the **existing kokoro-tts `--stream` functionality** instead of reinventing it.

## ✅ What I Built

### **Simple Architecture:**
```
extract_pages.py → pipe → kokoro-tts --stream
     ↓                        ↓
  [Page Text]              [Audio Stream]
```

## 🚀 **Quick Usage**

### **Stream from page 50:**
```bash
./stream_sapiens_from_page.sh 50
```

### **Stream pages 50-100:**
```bash
./stream_sapiens_from_page.sh 50 100
```

### **Stream with specific voice:**
```bash
./stream_sapiens_from_page.sh 50 100 af_sarah
```

### **Stream with voice and speed:**
```bash
./stream_sapiens_from_page.sh 50 100 af_sarah 1.3
```

## 📋 **Available Voices**

Just run the script without arguments to see all available voices:
```bash
./stream_sapiens_from_page.sh
```

## 🔧 **How It Works**

### **1. Page Extraction (`extract_pages.py`):**
- Extracts text from specific page ranges
- Outputs to stdout for piping
- Simple, focused functionality

### **2. Kokoro TTS Streaming (`kokoro-tts --stream`):**
- Uses the **existing** streaming functionality
- All the advanced features (voice blending, error handling, etc.)
- No reinventing the wheel

### **3. Shell Script Wrapper (`stream_sapiens_from_page.sh`):**
- Combines extraction + streaming
- Simple parameter handling
- User-friendly interface

## 🎯 **Advantages of This Approach**

✅ **Leverages existing kokoro-tts streaming infrastructure**  
✅ **Much simpler codebase (50 lines vs 400+ lines)**  
✅ **Uses proven streaming functionality**  
✅ **All existing kokoro-tts features available**  
✅ **Easy to maintain and extend**  

## 🛠️ **Files Created**

1. **`extract_pages.py`** - Simple page extractor (50 lines)
2. **`stream_sapiens_from_page.sh`** - Wrapper script (40 lines) 
3. **This guide** - Usage documentation

## 🎵 **Features Inherited from Kokoro TTS**

- ✅ **Real-time streaming**
- ✅ **50+ voice options**  
- ✅ **Voice blending support**
- ✅ **Speed control**
- ✅ **Error handling**
- ✅ **Progress indicators**
- ✅ **Interruption support (Ctrl+C)**

## 📖 **Example Usage**

```bash
# Start reading Sapiens from Chapter 4 (page 50)
./stream_sapiens_from_page.sh 50

# Read just one page with a specific voice
./stream_sapiens_from_page.sh 50 50 af_sarah

# Speed reading with 1.5x speed
./stream_sapiens_from_page.sh 100 150 am_adam 1.5
```

This approach is **much cleaner** and leverages the existing, well-tested streaming functionality rather than building everything from scratch! 