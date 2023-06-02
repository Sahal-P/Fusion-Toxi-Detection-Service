from fastapi import APIRouter, Depends, Body, Request
from models.message import Message
from fastapi.responses import JSONResponse
from bson import ObjectId
from schemas.message import MessageEntity
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_204_NO_CONTENT
from typing import Optional
from fastapi import Query
from services.service import TextClassification
import json
# from config.db import collection

Validate_Text = TextClassification()

message = APIRouter()

@message.post("/validate")
async def ToxicTextDetectAPIView(message: Message, prefix: str = Query(...)) -> JSONResponse:
    if prefix != "7898474748":
        print(prefix, type(prefix))
        result= None
        return JSONResponse(status_code=HTTP_401_UNAUTHORIZED, content=result)
    msg = Validate_Text.toxic_values(message.message)
    result = json.dumps({"result":msg})
    return JSONResponse(status_code=HTTP_200_OK, content=result)

@message.get("/search")  
async def UserLoginAPIView(prefix: str = Query(...)) -> JSONResponse:
    
    return JSONResponse(status_code=HTTP_200_OK, content='')
