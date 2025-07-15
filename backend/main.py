from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path
from backend.services.transcriber import transcribe_audio
from backend.services.ocr import extract_text_and_figures

app = FastAPI()

# Allow frontend (from any origin for now)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Lecture AI backend is running!"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    upload_path = Path("../data") / file.filename
    with open(upload_path, "wb") as buffer:
        buffer.write(await file.read())
        
    transcript = transcribe_audio(str(upload_path))  # 👈 Call transcriber
    output_path = Path("../outputs") / f"{file.filename}_transcript.txt"
    output_path.write_text(transcript, encoding='utf-8')
    
    return {"filename": file.filename, "status": "transcribed", "transcript_preview": transcript[:300]}

@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    upload_path = Path("data") / file.filename
    with open(upload_path, "wb") as buf:
        buf.write(await file.read())

    results = extract_text_and_figures(str(upload_path), frame_interval=60, output_dir="outputs/figures")

    txt_path = Path("outputs") / f"{file.filename}_ocr.txt"
    txt_path.write_text(results["text"], encoding="utf-8")

    return {
        "filename": file.filename,
        "status": "ocr_complete",
        "ocr_preview": results["text"][:300]
    }
