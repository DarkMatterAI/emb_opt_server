from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from .config import CONFIG

if CONFIG.MONGO_URI:
    client = AsyncIOMotorClient(CONFIG.MONGO_URI)
else:
    client = None

from .schemas.schemas_crud import EndpointDocument
from .schemas.schemas_search import SearchDocument

document_models = [EndpointDocument, SearchDocument]

async def init_mongodb():
    await init_beanie(database=client[CONFIG.MONGO_DB_NAME], 
                      document_models=document_models)