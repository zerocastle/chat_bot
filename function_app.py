from typing import Union
from fastapi import FastAPI

from fastapi.encoders import jsonable_encoder

from dto.Question import QuestionRequest
from azure.messaging.webpubsubservice.aio import WebPubSubServiceClient
from azure.core.credentials import AzureKeyCredential
from fastapi.middleware.cors import CORSMiddleware

import os
import uuid as uuid

import azure.functions as func

END_POINT = "https://gptlecturepubsubkys.webpubsub.azure.com"
HUB = "dev_hub"
KEY = "DZJRixJasBSZtdXR48GMkCILRkCyUo1rxx8Qtrl0TeF91m9Lj0ehJQQJ99AKACNns7RXJ3w3AAAAAWPSHJxV"

# load_env()
fastApp = FastAPI()
fastApp.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
    
)
#azure function 이용 
app = func.AsgiFunctionApp(app = fastApp,http_auth_level=func.AuthLevel.ANONYMOUS) 

# service = WebPubSubServiceClient(endpoint=os.environ["END_POINT_URL"], hub=os.environ["HUB"], credential=AzureKeyCredential(os.environ["KEY"]))

service = WebPubSubServiceClient(endpoint=END_POINT, hub=HUB, credential=AzureKeyCredential(KEY))


@fastApp.post("/question")
async def send_question(question : QuestionRequest):
    
    return await question


@fastApp.get("/channel_id")
def get_channel_id():
    return {"channel_id" : str(uuid.uuid4())} 
    

@fastApp.get("/pubsub/token")
async def read_root(channel_id: str):
    return await service.get_client_access_token(groups=[channel_id] , minutes_to_expire=5 , roles=['webpubsub.joinLeaveGroup.' + channel_id])


@fastApp.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return await{"item_id": item_id, "q": q}


