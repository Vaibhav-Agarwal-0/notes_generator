from faster_whisper import WhisperModel

# Load once at module level
model = WhisperModel("base", compute_type="float32")  # "int8" is faster

def transcribe_audio(filepath: str) -> str:
    segments, _ = model.transcribe(filepath)
    transcript = "\n".join([seg.text for seg in segments])
    return transcript
