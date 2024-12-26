from typing import Optional
from openai_redis_vectorstore.schemas import Document as DocumentBase


class Document(DocumentBase):
    id: Optional[int] = None
    app_label: Optional[str] = None
    model_name: Optional[str] = None
