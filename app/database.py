import os 
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .schemas import DOCUMENT_MODELS

client = AsyncIOMotorClient(os.environ.get("MONGO_URI", None))

async def init_mongodb():
    await init_beanie(database=client[os.environ.get("MONGO_DB_NAME", None)], 
                      document_models=DOCUMENT_MODELS)