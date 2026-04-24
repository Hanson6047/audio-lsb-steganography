# CLAUDE.md

## Project Name

Audio LSB Steganography

## Project Goal

This project is a Python-based audio steganography system.

The main goal is to hide secret information inside WAV audio files using the LSB, Least Significant Bit, technique.

This project is designed for learning and presentation purposes.  
The code should be easy to understand, easy to explain, and suitable for a beginner/intermediate Python learner.

---

## Current Scope

Only implement the following features for now:

1. Convert text messages into binary data.
2. Hide a text message inside a WAV audio file using LSB.
3. Extract a hidden text message from a WAV audio file.
4. Support basic encoding and decoding through command-line interface.
5. Hide a short WAV audio file inside another longer WAV audio file.
6. Extract the hidden WAV audio file from the stego WAV file.

---

## Out of Scope for Now

Do NOT implement these features unless explicitly requested:

1. AES encryption.
2. Randomized embedding positions.
3. GUI application.
4. MP3 support.
5. FFT / DCT frequency-domain steganography.
6. Web application.
7. Database.
8. Overly complex class-based architecture.
9. Machine learning or AI-based detection.
10. Multi-layer steganography beyond the basic audio-in-audio feature.

The current focus is to make the basic LSB system correct, understandable, and testable.

---

## Development Principles

Please follow these principles:

1. Do not generate a full large project all at once.
2. Work stage by stage.
3. Explain the goal before writing code.
4. Explain each new or modified file before editing it.
5. Keep the code simple and readable.
6. Prefer functions over classes in the early version.
7. Add docstrings to all important functions.
8. Add comments near important logic.
9. Avoid unnecessary abstraction.
10. Avoid adding features that are not in the current stage.

The priority is:

1. Correctness
2. Understandability
3. Testability
4. Maintainability
5. Feature richness

---

## Expected Project Structure

```text
audio_lsb_steganography/
├── main.py
├── requirements.txt
├── README.md
├── CLAUDE.md
├── data/
│   ├── cover/
│   ├── secret/
│   └── output/
└── src/
    ├── __init__.py
    ├── bit_utils.py
    ├── wav_utils.py
    ├── text_steg.py
    └── audio_steg.py

    --

    ## File Responsibilities

### main.py

The command-line entry point of the project.

It should parse user commands and call functions from the `src/` modules.

Example commands:

```bash
python main.py encode-text --input data/cover/cover.wav --output data/output/stego.wav --message "Hello"
python main.py decode-text --input data/output/stego.wav
python main.py encode-audio --cover data/cover/song.wav --secret data/secret/secret.wav --output data/output/stego_audio.wav
python main.py decode-audio --input data/output/stego_audio.wav --output data/output/extracted_secret.wav
```

---

### requirements.txt

Lists required Python packages.

At the beginning, keep it minimal:

```text
numpy
```

---

### README.md

Explains the project for humans.

It should include:

1. Project purpose.
    
2. LSB principle.
    
3. Project structure.
    
4. Installation steps.
    
5. Usage examples.
    
6. Current limitations.
    
7. Future improvements.
    

---

### data/cover/

Stores cover audio files.

A cover audio file is the audio used to hide secret data.

Example:

```text
cover.wav
song.wav
```

---

### data/secret/

Stores secret files.

Example:

```text
secret.wav
message.txt
```

---

### data/output/

Stores generated files.

Example:

```text
stego.wav
extracted_secret.wav
```

---

### src/bit_utils.py

Handles binary conversion.

Responsibilities:

1. Convert bytes to bits.
    
2. Convert bits to bytes.
    
3. Convert text to bits.
    
4. Convert bits to text.
    
5. Convert integer length to 32-bit header.
    
6. Convert 32-bit header back to integer.
    

Recommended functions:

```python
def bytes_to_bits(data: bytes) -> list[int]:
    pass

def bits_to_bytes(bits: list[int]) -> bytes:
    pass

def text_to_bits(text: str) -> list[int]:
    pass

def bits_to_text(bits: list[int]) -> str:
    pass

def int_to_32_bits(value: int) -> list[int]:
    pass

def bits_to_int(bits: list[int]) -> int:
    pass
```

---

### src/wav_utils.py

Handles WAV file reading and writing.

Responsibilities:

1. Read WAV parameters.
    
2. Read WAV frames.
    
3. Convert frames into NumPy sample array.
    
4. Write NumPy sample array back to WAV.
    
5. Check embedding capacity.
    

Recommended functions:

```python
def read_wav(path: str):
    pass

def write_wav(path: str, params, audio_samples) -> None:
    pass

def calculate_capacity_bits(audio_samples, lsb_count: int = 1) -> int:
    pass

def check_capacity(payload_bits_count: int, audio_samples, lsb_count: int = 1) -> None:
    pass
```

Use WAV format first.  
Do not implement MP3 support now.

---

### src/text_steg.py

Handles text steganography.

Responsibilities:

1. Hide text inside a WAV file.
    
2. Extract text from a WAV file.
    
3. Add a 32-bit length header before the payload.
    
4. Use LSB to embed and extract data.
    

Recommended functions:

```python
def hide_text_in_wav(input_wav: str, output_wav: str, message: str, lsb_count: int = 1) -> None:
    pass

def extract_text_from_wav(stego_wav: str, lsb_count: int = 1) -> str:
    pass
```

Payload format:

```text
[32-bit payload length][payload bits]
```

The 32-bit length means the number of payload bits.

---

### src/audio_steg.py

Handles audio-in-audio steganography.

Responsibilities:

1. Hide a short WAV audio file inside another WAV audio file.
    
2. Extract the hidden WAV audio file.
    
3. Preserve enough metadata to reconstruct the secret WAV file.
    

Recommended basic approach:

```text
secret_wav_file
↓
read all bytes
↓
convert bytes to bits
↓
add 32-bit payload length
↓
embed into cover wav LSB
```

Recommended functions:

```python
def hide_audio_in_wav(cover_wav: str, secret_wav: str, output_wav: str, lsb_count: int = 1) -> None:
    pass

def extract_audio_from_wav(stego_wav: str, output_secret_wav: str, lsb_count: int = 1) -> None:
    pass
```

For the first version, the secret audio should be:

1. WAV format.
    
2. Short duration.
    
3. Smaller than the cover audio capacity.
    

---

## Development Stages

Follow these stages in order.

### Stage 1: Project Setup

Goal:

1. Create project folders.
    
2. Create empty Python files.
    
3. Create `requirements.txt`.
    
4. Create initial `README.md`.
    

Do not implement core LSB logic yet.

---

### Stage 2: Bit Utilities

Goal:

1. Implement `bit_utils.py`.
    
2. Test text-to-bits and bits-to-text.
    
3. Test bytes-to-bits and bits-to-bytes.
    
4. Test 32-bit length header conversion.
    

---

### Stage 3: WAV Utilities

Goal:

1. Implement `wav_utils.py`.
    
2. Read a WAV file.
    
3. Write a copied WAV file.
    
4. Confirm the copied audio can be played.
    
5. Calculate capacity.
    

---

### Stage 4: Text Steganography

Goal:

1. Implement `text_steg.py`.
    
2. Hide a text message in a WAV file.
    
3. Extract the text message.
    
4. Confirm the extracted message matches the original message.
    

---

### Stage 5: CLI

Goal:

1. Implement `main.py`.
    
2. Add `encode-text`.
    
3. Add `decode-text`.
    
4. Test from command line.
    

---

### Stage 6: Audio-in-Audio Steganography

Goal:

1. Implement `audio_steg.py`.
    
2. Hide a short WAV file inside a longer WAV file.
    
3. Extract the hidden WAV file.
    
4. Confirm the extracted WAV can be played.
    

---

### Stage 7: Documentation

Goal:

1. Update `README.md`.
    
2. Explain the project.
    
3. Explain how LSB works.
    
4. Explain each file.
    
5. Add command examples.
    
6. Add limitations.
    

---

## Required Response Format

When helping with this project, please use the following format:

```text
【本階段目標】
Explain what this stage will accomplish.

【會新增/修改的檔案】
List files and explain their purpose.

【程式碼】
Provide the code.

【程式碼解釋】
Explain the logic in beginner-friendly language.

【測試方式】
Provide exact commands to run.

【預期結果】
Explain what should happen if successful.

【下一步】
Explain what the next stage will be.
```

---

## Explanation Requirements

The user wants to understand the project, not only finish it.

Whenever code is added or modified, explain:

1. What this file is responsible for.
    
2. What each function does.
    
3. How data flows through the system.
    
4. Why this design is used.
    
5. How to test it.
    
6. What common errors may happen.
    

Use Traditional Chinese explanations.

Use simple English only when naming functions, commands, or technical terms.

---

## Coding Style

Use beginner-friendly Python.

Rules:

1. Use clear function names.
    
2. Use type hints where helpful.
    
3. Use docstrings.
    
4. Use comments for important logic.
    
5. Avoid advanced Python tricks.
    
6. Avoid unnecessary classes.
    
7. Avoid global variables unless clearly needed.
    
8. Raise clear error messages.
    
9. Keep each function focused on one task.
    

---

## LSB Embedding Rule

For the first version, use 1-bit LSB by default.

Basic rule:

```text
new_sample = (old_sample & ~1) | secret_bit
```

This means:

1. Clear the last bit of the audio sample.
    
2. Put the secret bit into that last position.
    

Example:

```text
old sample: 10010110
secret bit: 1
new sample: 10010111
```

---

## Payload Format

Use this format for both text and audio payloads:

```text
[32-bit payload length][payload bits]
```

The first 32 bits store how many payload bits need to be extracted.

This allows the decoder to know when to stop reading.

---

## Testing Requirements

Every stage must include at least one test.

Examples:

### Test bit conversion

```bash
python -m src.bit_utils
```

Expected result:

```text
Original text: Hello
Recovered text: Hello
```

### Test text encoding

```bash
python main.py encode-text --input data/cover/cover.wav --output data/output/stego.wav --message "Hello LSB"
```

### Test text decoding

```bash
python main.py decode-text --input data/output/stego.wav
```

Expected result:

```text
Hello LSB
```

### Test audio encoding

```bash
python main.py encode-audio --cover data/cover/song.wav --secret data/secret/secret.wav --output data/output/stego_audio.wav
```

### Test audio decoding

```bash
python main.py decode-audio --input data/output/stego_audio.wav --output data/output/extracted_secret.wav
```

Expected result:

```text
The hidden audio file was extracted successfully.
```

---

## Current Limitations

The first version has these limitations:

1. Only WAV files are supported.
    
2. MP3 files are not supported.
    
3. No encryption yet.
    
4. No randomized embedding position yet.
    
5. No GUI yet.
    
6. Large secret audio files may not fit inside the cover audio.
    
7. If the stego WAV is converted to MP3, the hidden data may be destroyed.
    

---

## Future Improvements

Possible future features:

1. AES encryption before embedding.
    
2. Password-based randomized embedding positions.
    
3. 2-bit or 3-bit LSB mode.
    
4. GUI interface.
    
5. Audio quality analysis such as MSE and SNR.
    
6. Waveform comparison.
    
7. Frequency-domain steganography using FFT or DCT.
    
8. Support for hiding images, PDFs, or ZIP files.
    

---

## Important Instruction

Do not skip stages.

Do not add advanced features before the basic LSB text and audio hiding features are working.

The user should be able to explain every file and every important function after each stage.