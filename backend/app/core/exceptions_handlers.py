from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.exceptions import ProcureFlowException
from app.core.logging import get_logger

logger = get_logger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ProcureFlowException)
    async def procureflow_exception_handler(
        request: Request, exc: ProcureFlowException
    ) -> JSONResponse:
        logger.warning(
            f"Application error: {exc.message}",
            extra={
                "status_code": exc.status_code,
                "path": request.url.path,
                "details": exc.details,
            },
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.message,
                "data": None,
                "errors": [exc.message],
                "request_id": getattr(request.state, "request_id", None),
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.error(
            f"Unhandled error: {str(exc)}",
            exc_info=True,
            extra={"path": request.url.path},
        )
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "An unexpected error occurred" if not app.debug else str(exc),
                "data": None,
                "errors": None,
                "request_id": getattr(request.state, "request_id", None),
            },
        )
