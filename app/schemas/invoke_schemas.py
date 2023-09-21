from typing import Optional, List
from pydantic import BaseModel

class InvokeItem(BaseModel):
    item: Optional[str]
    embedding: Optional[List[float]]
    data: Optional[dict]