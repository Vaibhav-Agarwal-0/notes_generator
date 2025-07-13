import cv2
import pytesseract
from pathlib import Path
import os

def extract_text_from_video(video_path: str, frame_interval: int = 30) -> str:
    text_blocks = []
    vidcap = cv2.VideoCapture(video_path)

    success, image = vidcap.read()
    count = 0
    frame_idx = 0

    while success:
        if frame_idx % frame_interval == 0:
            # Save frame temporarily
            temp_img_path = f"../../data/frame_{count}.jpg"
            cv2.imwrite(temp_img_path, image)

            # Extract text
            text = pytesseract.image_to_string(image)
            if text.strip():
                text_blocks.append(f"[Frame {frame_idx}]\n{text.strip()}")

            # Clean up temp frame
            os.remove(temp_img_path)
            count += 1

        success, image = vidcap.read()
        frame_idx += 1

    vidcap.release()
    return "\n\n".join(text_blocks)
