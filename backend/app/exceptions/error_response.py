from datetime import datetime

from pydantic import BaseModel


class ErrorResponse(BaseModel):

    success: bool

    status: int

    error: str

    message: str

    path: str

    request_id: str

    timestamp: datetime
