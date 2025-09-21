import pytesseract
from PIL import Image
import io
import cv2
import numpy as np
import re

def preprocess_image(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    img = cv2.medianBlur(img, 5)
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    _, buffer = cv2.imencode('.jpg', img)
    return buffer.tobytes()

def extract_text(image_bytes):
    preprocessed = preprocess_image(image_bytes)
    image = Image.open(io.BytesIO(preprocessed))
    text = pytesseract.image_to_string(image)
    # Simple parsing logic (improve with regex/ML for prod)
    lines = text.split('\n')
    date_match = re.search(r'\d{1,2}/\d{1,2}/\d{2,4}', text)  # Example date format
    amount_match = re.search(r'\$\d+\.?\d*', text)
    vendor = lines[0].strip() if lines else "Unknown"  # First line as vendor placeholder
    return {
        "date": date_match.group(0) if date_match else "Unknown",
        "vendor": vendor,
        "amount": float(amount_match.group(0)[1:]) if amount_match else 0.0,
        "raw_text": text
    }