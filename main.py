from fastapi import FastAPI
from routes import upload, generate, compare, ask

app = FastAPI(
    title="Ancient DNA Analysis API",
    description="API for uploading, analyzing and comparing ancient DNA sequences.",
    version="1.0.0"
)

app.include_router(upload.router)
app.include_router(generate.router)
app.include_router(compare.router)
app.include_router(ask.router)
