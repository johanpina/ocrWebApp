import io
import pytesseract
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pytesseract import Output
from PIL import Image

# Configurar Tesseract
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Asegúrate de que la ruta sea la correcta en tu sistema

app = FastAPI()
app.mount("/static", StaticFiles(directory="."), name="static")


class ImageSchema:
    data: bytes

async def ocr_image(image_data: bytes) -> str:
    image = Image.open(io.BytesIO(image_data))
    text = pytesseract.image_to_string(image, lang="spa", config="--psm 6")  # Ajusta el idioma y la configuración según tus necesidades
    return text

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    image_data = await file.read()
    text = await ocr_image(image_data)
    return {"text": text}

@app.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    with open("index.html", "r") as f:
        html_content = f.read()
    return html_content


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
