
from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from schemas import HTTPError, OcrResult, ZerSchema
from ocr import ocr_image, ocr_ZER

app = FastAPI(title='OCR PeopleContact')
app.mount("/static", StaticFiles(directory="static/"), name="static")

@app.get("/", response_class=HTMLResponse,tags=["WebInterface"])
async def get_root(request: Request):
    with open("static/index.html", "r") as f:
        html_content = f.read()
    return html_content

@app.post("/img2text/",response_model=OcrResult,tags=["OCR4all"])
async def upload_image(file: UploadFile = File(...)):
    image_data = await file.read()
    text = await ocr_image(image_data)

    return OcrResult(texto=text)

@app.post("/InfoPagoZer/",response_model=ZerSchema,responses={
                                                            200:{"model":ZerSchema},
                                                            409:{"model":HTTPError, "description":"Error Saving Image in SharedFolder"}
                                                            },# Este responses es para las excepciones en la documentación. Si se hace así queda la documentación.   
          tags=["ZERocr"])

async def upload_image(file: UploadFile = File(...)):
    image_data = await file.read()
    dictionary = await ocr_ZER(image_data)
    if dictionary:
        return dictionary
    else:
        raise HTTPException(status_code=409)