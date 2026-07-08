from datetime import datetime, timezone
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .base_exception import BaseAPIException


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(BaseAPIException)
    async def handle_api_exception(request: Request, exc: BaseAPIException):

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "status": exc.status_code,
                "error": exc.__class__.__name__,
                "message": exc.message,
                "path": request.url.path,
                "request_id": request.state.request_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

    @app.exception_handler(Exception)
    async def handle_unknown_exception(
        request: Request,
        exc: Exception,
    ):

        print(f"[{request.state.request_id}] {exc}")

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "status": 500,
                "error": "InternalServerException",
                "message": "Unexpected server error",
                "path": request.url.path,
                "request_id": request.state.request_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )
