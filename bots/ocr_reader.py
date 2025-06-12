import pytesseract
from PIL import Image, ImageOps

def preprocess_image(image_path: str) -> Image.Image:
    img = Image.open(image_path)
    img = img.convert("L")
    img = ImageOps.autocontrast(img) 
    return img

def extract_text_from_image(image_path: str) -> str:
    try:
        image = preprocess_image(image_path)

        config = "--psm 6"
        text = pytesseract.image_to_string(image, lang="spa", config=config)
        return text.strip()
    except Exception as e:
        return f"Ocurrió un error durante el OCR: {e}"
