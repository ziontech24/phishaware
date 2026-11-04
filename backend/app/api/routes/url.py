from fastapi import APIRouter

from app.schemas.url import URLAnalysisRequest
from app.schemas.detection import DetectionResponse
from app.services.url_analyzer import analyze_url


router = APIRouter()


@router.post("/analyze/url", response_model=DetectionResponse)
def analyze_url_endpoint(request: URLAnalysisRequest):
    return analyze_url(request.url)