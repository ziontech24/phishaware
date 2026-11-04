from fastapi import FastAPI

from app.api.routes import health, url


app = FastAPI(
    title="PhishAware API",
    description="An accessible phishing detection API.",
    version="1.0.0"
)


app.include_router(
    health.router,
    prefix="/api/v1",
    tags=["Health"]
)

app.include_router(
    url.router,
    prefix="/api/v1",
    tags=["URL Analysis"]
)