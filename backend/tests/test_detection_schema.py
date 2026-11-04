import pytest

from app.schemas.detection import (
    AnalysisType,
    DetectionStatus,
    Severity,
    Finding,
    Recommendation,
    DetectionResponse,
)


def test_analysis_type():
    assert AnalysisType.URL == "url"
    assert AnalysisType.MESSAGE == "message"


def test_detection_status():
    assert DetectionStatus.SUSPICIOUS == "suspicious"
    assert DetectionStatus.UNABLE_TO_DETERMINE == "unable_to_determine"


def test_finding_model():
    finding = Finding(
        id="F001",
        category="Suspicious link",
        title="Unusual website address",
        description="The link uses an address different from the organization it claims to represent.",
        evidence="The website address does not match the claimed organization.",
        severity=Severity.HIGH,
    )

    assert finding.severity == Severity.HIGH


def test_recommendation_model():
    recommendation = Recommendation(
        title="Do not open the link",
        description="Visit the organization's official website instead.",
        priority=Severity.HIGH,
    )

    assert recommendation.priority == Severity.HIGH


def test_complete_detection_response():
    response = DetectionResponse(
        analysis_type=AnalysisType.MESSAGE,
        status=DetectionStatus.SUSPICIOUS,
        summary="This message contains signs commonly associated with phishing.",
        findings=[
            Finding(
                id="F001",
                category="Urgency",
                title="Pressure to act quickly",
                description="The message pressures you to act immediately.",
                evidence="It says your account will be blocked unless you act now.",
                severity=Severity.MEDIUM,
            )
        ],
        recommendations=[
            Recommendation(
                title="Do not follow the link",
                description="Visit the organization's official website directly.",
                priority=Severity.HIGH,
            )
        ],
        limitations=[
            "We cannot confirm who sent this message."
        ],
    )

    assert response.analysis_type == AnalysisType.MESSAGE
    assert response.status == DetectionStatus.SUSPICIOUS
    assert len(response.findings) == 1
    assert len(response.recommendations) == 1

    # Verify that the response can be converted into JSON.
    result = response.model_dump(mode="json")

    assert result["status"] == "suspicious"
    assert result["findings"][0]["severity"] == "medium"


def test_invalid_severity():
    with pytest.raises(ValueError):
        Finding(
            id="F002",
            category="Test",
            title="Invalid severity test",
            description="Testing invalid severity.",
            evidence="Test evidence.",
            severity="critical",
        )