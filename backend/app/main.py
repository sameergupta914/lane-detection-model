from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from .config import settings
from .model_loader import get_model
from .routes.predict import router as predict_router
from .schemas import ErrorResponse, HealthResponse


app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/outputs", StaticFiles(directory=settings.output_dir), name="outputs")
app.include_router(predict_router, prefix=settings.api_prefix)


@app.on_event("startup")
def startup():
    get_model()


@app.get("/health", response_model=HealthResponse)
def health():
    try:
        get_model()
        loaded = True
    except Exception:
        loaded = False

    return HealthResponse(
        status="ok",
        model_loaded=loaded,
        model_path=str(settings.model_path),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(error=f"Unhandled server error: {exc}").model_dump(),
    )
