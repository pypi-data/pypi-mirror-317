from typing import Optional
from typing import Dict
from typing import Any

import pydantic
from openai_redis_vectorstore.schemas import Document as DocumentBase


class VectorStoreIndexSegment(pydantic.BaseModel):
    index_name: str
    content: str
    meta: Optional[Dict[str, Any]] = None


class Document(DocumentBase):
    id: Optional[int] = None
    app_label: Optional[str] = None
    model_name: Optional[str] = None
