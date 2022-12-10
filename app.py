import os
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware
import motor.motor_asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


MONGODB_URL = 'mongodb+srv://grupo3:6MFW60Nn4K69ZHsc@cluster0.80bqakk.mongodb.net/test'

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.misiontic


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class DocumentModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    Nombre: str = Field(...)
    Tipo: str = Field(...)
    Area: str = Field(...)
    Fecha: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "Nombre": "Nomina Noviembre",
                "Tipo": "PDF",
                "Area": "Contabilidad",
                "Fecha": "6/12/2022"
            }
        }


class UpdateDocumentModel(BaseModel):
    Nombre: Optional[str]
    Tipo: Optional[str]
    Area: Optional[str]
    Fecha: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "Nombre": "Nomina Noviembre",
                "Tipo": "PDF",
                "Area": "Contabilidad",
                "Fecha": "6/12/2022"
            }
        }


@app.post("/", response_description="Agregar nuevo Documento", response_model=DocumentModel)
async def agregar_documento(document: DocumentModel = Body(...)):
    document = jsonable_encoder(document)
    new_document = await db["misiontic"].insert_one(document)
    created_document = await db["misiontic"].find_one({"_id": new_document.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_document)


@app.get("/", response_description="Lista de Documentos", response_model=List[DocumentModel])
async def listar_documentos():
    documents = await db["misiontic"].find().to_list(1000)
    return documents


@app.get("/{id}", response_description="Obtener documento por ID", response_model=DocumentModel)
async def mostrar_documento_id(id: str):
    if (document := await db["misiontic"].find_one({"_id": id})) is not None:
        return document

    raise HTTPException(
        status_code=404, detail=f"Documento {id} no encontrado")


@app.put("/{id}", response_description="Actualizar documento", response_model=DocumentModel)
async def actualizar_documento_id(id: str, document: UpdateDocumentModel = Body(...)):
    document = {k: v for k, v in document.dict().items() if v is not None}

    if len(document) >= 1:
        update_result = await db["misiontic"].update_one({"_id": id}, {"$set": document})

        if update_result.modified_count == 1:
            if (
                updated_document := await db["misiontic"].find_one({"_id": id})
            ) is not None:
                return updated_document

    if (existing_document := await db["misiontic"].find_one({"_id": id})) is not None:
        return existing_document

    raise HTTPException(
        status_code=404, detail=f"Documento {id} no encontrado")


@app.delete("/{id}", response_description="Eliminar Documento")
async def eliminar_documento_id(id: str):
    delete_result = await db["misiontic"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=404, detail=f"Documento {id} no encontrado")
