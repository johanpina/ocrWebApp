from pydantic import BaseModel

# Esta clase es para el manejo de los codigos de respuesta de la app
# Este es el esquema base de un error cualquiera.

class ZerSchema(BaseModel):
    referencia: str = None
    nombre: str = None
    placa: str = None
    pago: int = None
    fecha: str = None
    path: str = None

class responseSchema(BaseModel):
    succes: bool
    message: str
    statusCode: int
    data: ZerSchema = {}


class HTTPError409(responseSchema):
    statusCode = 409
    
    class Config:
        schema_extra = {
            "example": {"succes":False, "message": "Imagen Ya registrada", "statusCode": 409, "data": {}},
        }

class HTTPError410(responseSchema):
    statusCode = 410
    class Config:
        schema_extra = {
            "example": {"succes":False, "message": "Formato de imágen incorrecto", "statusCode": 410, "data": {}},
        }

class ImageSchema(BaseModel):
    data: bytes

class OcrResult(BaseModel):
    texto: str


