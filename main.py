
from fastapi import FastAPI, File, UploadFile, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from schemas import HTTPError409, HTTPError410, OcrResult, ZerSchema, responseSchema
from ocr import ocr_image, ocr_ZER

from PIL import Image
from io import BytesIO

app = FastAPI(title='OCR PeopleContact')

# Configure CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

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

@app.post("/InfoPagoZer/",response_model=responseSchema,responses={
                                                            200:{"model":responseSchema},
                                                            #409:{"model":HTTPError409, "description":"Imagen Ya registrada"},
                                                            #410:{"model":HTTPError410, "description":"Formato de imágen incorrecto"}
                                                            },# Este responses es para las excepciones en la documentación. Si se hace así queda la documentación.   
          tags=["ZERocr"])

async def upload_image(file: UploadFile = File(...)):
    image_data = await file.read()
    
    """# Intenta abrir los datos de la imagen con Pillow
    try:
        Image.open(BytesIO(image_data))
    except IOError:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Formato de imágen incorrecto")
    """
    dictionary = await ocr_ZER(image_data)

    if dictionary != -1:

        if dictionary:

            response_struct = responseSchema(succes=True, 
                                            message="Imagen procesada exitosamente",
                                            statusCode=200,
                                            data = dictionary
                                            )

            return response_struct
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Imágen Ya registrada")
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Datos insuficientes detectados")