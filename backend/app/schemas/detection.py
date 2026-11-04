from enum import Enum
from pydantic import BaseModel, Field

class AnalysisType(str, Enum):
    URL = "url"
    MESSAGE = "message"
class DetectionStatus(str, Enum):
    POTENTIALLY_MALICIOUS = "potentially_malicious"
    SUSPICIOUS = "suspicious"
    NO_OBVIOUS_THREAT = "no_obvious_threat_detected"
    UNABLE_TO_DETERMINE = "unable_to_determine"
class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
class Finding(BaseModel):
    id: str
    category: str
    title: str
    description: str
    evidence: str
    severity: Severity
class Recommendation(BaseModel):
    title: str
    description: str
    priority: Severity
class DetectionResponse(BaseModel):
    analysis_type: AnalysisType
    status: DetectionStatus
    summary: str = Field(
        description="A short, easy-to-understand explanation of the overall result."
    )
    findings: list[Finding]
    recommendations: list[Recommendation]
    limitations: list[str] = Field(
        description="Important things the analysis could not verify."
    )
