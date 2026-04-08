"""FastAPI backend for formal-to-informal text translation."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.translate import router as translate_router

app = FastAPI(title="Formalator API", version="1.0.0")

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(translate_router, prefix="/api")


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "service": "formalator-api"}
