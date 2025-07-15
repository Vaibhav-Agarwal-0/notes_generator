import cv2
import pytesseract
import layoutparser as lp
from pathlib import Path

# Load layout model once
layout_model = lp.Detectron2LayoutModel(
    'lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config',
    label_map={0:"Text",1:"Title",2:"List",3:"Table",4:"Figure"}
)

def extract_text_and_figures(video_path: str, frame_interval: int = 30, output_dir: str = "outputs/figures") -> dict:
    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()
    frame_idx = 0
    all_text = []

    while success:
        if frame_idx % frame_interval == 0:
            layout = layout_model.detect(frame)
            for block in layout:
                x1,y1,x2,y2 = map(int, block.coordinates)
                crop = frame[y1:y2, x1:x2]

                if block.type in ("Text","Title","List"):
                    text = pytesseract.image_to_string(crop).strip()
                    if text:
                        all_text.append(f"[Frame {frame_idx}][{block.type}]\n{text}\n")
                else:  # Figure block
                    fname = output_dir_path / f"frame{frame_idx}_{block.type}_{x1}_{y1}.png"
                    cv2.imwrite(str(fname), crop)

        success, frame = cap.read()
        frame_idx += 1

    cap.release()
    return {"text": "\n".join(all_text)}
