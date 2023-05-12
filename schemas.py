from pydantic import BaseModel

# Esta clase es para el manejo de los codigos de respuesta de la app
# Este es el esquema base de un error cualquiera.
class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "Imagen Ya registrada"},
        }

class ImageSchema(BaseModel):
    data: bytes

class OcrResult(BaseModel):
    texto: str


class ZerSchema(BaseModel):
    referencia: str
    nombre: str
    placa: str
    pago: float
    fecha: str
    path: str
