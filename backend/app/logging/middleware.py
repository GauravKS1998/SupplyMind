import time

from starlette.middleware.base import BaseHTTPMiddleware

from .logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start = time.time()

        response = await call_next(request)

        end = time.time()

        duration = round((end - start) * 1000, 2)

        logger.info(f"""
Request ID : {request.state.request_id}
Method     : {request.method}
Path       : {request.url.path}
Status     : {response.status_code}
Duration   : {duration} ms
""")

        return response
