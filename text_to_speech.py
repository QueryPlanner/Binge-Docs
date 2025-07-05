from kokoro import KPipeline
from IPython.display import display, Audio
import soundfile as sf
import torch
import numpy as np

pipeline = KPipeline(lang_code='a')
text = '''
# Path Parameters and Numeric Validations

In the same way that you can declare more validations and metadata for query parameters with `Query`, you can declare the same type of validations and metadata for path parameters with `Path`.

## Import Path

First, import `Path` from `fastapi`, and import `Annotated`:

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[1,3] *}

/// info

FastAPI added support for `Annotated` (and started recommending it) in version 0.95.0.

If you have an older version, you would get errors when trying to use `Annotated`.

Make sure you [Upgrade the FastAPI version](../deployment/versions.md#upgrading-the-fastapi-versions){.internal-link target=_blank} to at least 0.95.1 before using `Annotated`.
'''
generator = pipeline(text, voice='af_heart')

# Collect all audio chunks
audio_chunks = []
for i, (gs, ps, audio) in enumerate(generator):
    print(f"Processing chunk {i}: {gs}, {ps}")
    audio_chunks.append(audio)

# Concatenate all audio chunks into one single array
if audio_chunks:
    full_audio = np.concatenate(audio_chunks, axis=0)
    
    # Display the full audio
    display(Audio(data=full_audio, rate=24000, autoplay=True))
    
    # Save as single file
    sf.write('full_audio.wav', full_audio, 24000)
    print(f"Generated single audio file: full_audio.wav with {len(full_audio)} samples")
else:
    print("No audio chunks generated")