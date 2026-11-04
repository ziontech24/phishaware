from app.services.url_analyzer import (
    check_ip_address,
    check_http_scheme,
    check_url_shortener,
    check_sensitive_keywords,
    analyze_url,
)

from app.schemas.detection import (
    Severity,
    AnalysisType,
    DetectionStatus,
)

def test_detect_ip_address():
    result = check_ip_address("192.168.1.10")

    assert result is not None
    assert result.severity == Severity.MEDIUM
    assert "192.168.1.10" in result.evidence


def test_normal_domain_is_not_flagged_as_ip():
    result = check_ip_address("example.com")

    assert result is None


def test_detect_http():
    result = check_http_scheme("http")

    assert result is not None
    assert result.severity == Severity.MEDIUM


def test_https_is_not_flagged():
    result = check_http_scheme("https")

    assert result is None


def test_detect_url_shortener():
    result = check_url_shortener("bit.ly")

    assert result is not None
    assert result.severity == Severity.LOW


def test_normal_domain_is_not_flagged_as_shortener():
    result = check_url_shortener("example.com")

    assert result is None


def test_detect_sensitive_keyword():
    result = check_sensitive_keywords(
        "https://example.com/account/verify"
    )

    assert result is not None
    assert "account" in result.evidence
    assert "verify" in result.evidence


def test_normal_url_is_not_flagged_for_sensitive_keywords():
    result = check_sensitive_keywords("https://example.com/about")

    assert result is None
def test_analyze_url_with_multiple_suspicious_characteristics():
    result = analyze_url(
        "http://192.168.1.10/account/verify"
    )

    assert result.analysis_type == AnalysisType.URL
    assert result.status == DetectionStatus.SUSPICIOUS
    assert len(result.findings) == 3
    assert len(result.recommendations) > 0
    assert len(result.limitations) > 0


def test_analyze_url_with_normal_url():
    result = analyze_url("https://example.com/about")

    assert result.analysis_type == AnalysisType.URL
    assert result.status == DetectionStatus.NO_OBVIOUS_THREAT
    assert result.findings == []


def test_analyze_url_with_invalid_url():
    result = analyze_url("not-a-valid-url")

    assert result.status == DetectionStatus.UNABLE_TO_DETERMINE
    assert result.findings == []


def test_analyze_url_does_not_visit_website():
    result = analyze_url("https://example.com")

    assert result.status == DetectionStatus.NO_OBVIOUS_THREAT
    assert "does not visit the website" in result.limitations[0]
def test_analyze_url_without_hostname():
    result = analyze_url("https://")

    assert result.status == DetectionStatus.UNABLE_TO_DETERMINE
    assert result.findings == []


def test_analyze_url_with_unsupported_scheme():
    result = analyze_url("ftp://example.com")

    assert result.status == DetectionStatus.UNABLE_TO_DETERMINE
    assert result.findings == []


def test_analyze_url_with_invalid_port():
    result = analyze_url("https://example.com:99999")

    assert result.status == DetectionStatus.UNABLE_TO_DETERMINE
    assert result.findings == []