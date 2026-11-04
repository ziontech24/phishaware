from pydantic import BaseModel, Field


class URLAnalysisRequest(BaseModel):
    url: str = Field(
        min_length=1,
        max_length=2048,
        description="The complete HTTP or HTTPS URL to analyze."
    )