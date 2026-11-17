
from uuid import UUID

from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):

    document_id: UUID

    question: str = Field(
        min_length=1,
        max_length=2000,
        description="Question about the uploaded PDF"
    )
