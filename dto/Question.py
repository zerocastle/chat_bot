from pydantic import BaseModel
from typing import Optional

class QuestionRequest(BaseModel):
    channel_id : str
    content : str
    