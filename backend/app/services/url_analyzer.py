from urllib.parse import urlparse
import ipaddress
import re

from app.schemas.detection import (
    AnalysisType,
    DetectionStatus,
    DetectionResponse,
    Finding,
    Recommendation,
    Severity,
)


def check_ip_address(hostname: str) -> Finding | None:
    """Check whether the URL uses an IP address instead of a domain."""

    try:
        ipaddress.ip_address(hostname)

        return Finding(
            id="URL001",
            category="IP address",
            title="Website uses an IP address",
            description=(
                "This link uses a numerical address instead of a "
                "normal website domain. Some legitimate websites do "
                "this, but it can also be used to hide a website's identity."
            ),
            evidence=f"The website address is {hostname}.",
            severity=Severity.MEDIUM,
        )

    except ValueError:
        return None
def check_http_scheme(scheme: str) -> Finding | None:
    """Check whether the URL uses unencrypted HTTP."""

    if scheme.lower() == "http":
        return Finding(
            id="URL002",
            category="Unencrypted connection",
            title="This link does not use HTTPS",
            description=(
                "This website uses HTTP instead of HTTPS. "
                "Information sent through this connection may not "
                "be protected from interception."
            ),
            evidence=f"The link starts with '{scheme}://'.",
            severity=Severity.MEDIUM,
        )

    return None
SHORTENER_DOMAINS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "is.gd",
    "cutt.ly",
    "rebrand.ly",
}


def check_url_shortener(hostname: str) -> Finding | None:
    """Check whether the URL uses a known URL-shortening service."""

    if hostname.lower().rstrip(".") in SHORTENER_DOMAINS:
        return Finding(
            id="URL003",
            category="Hidden destination",
            title="This link hides its final destination",
            description=(
                "This link uses a URL-shortening service. "
                "Its final destination is not visible from the shortened link."
            ),
            evidence=f"The link uses the shortening service {hostname}.",
            severity=Severity.LOW,
        )

    return None
SENSITIVE_KEYWORDS = {
    "login",
    "verify",
    "verification",
    "password",
    "secure",
    "account",
    "banking",
    "payment",
    "signin",
}


def check_sensitive_keywords(url: str) -> Finding | None:
    """Check whether the URL contains sensitive or commonly abused keywords."""

    parsed_url = urlparse(url)
    url_content = f"{parsed_url.hostname or ''}{parsed_url.path}".lower()

    matched_keywords = [
        keyword
        for keyword in SENSITIVE_KEYWORDS
        if re.search(rf"(?<![a-z0-9]){re.escape(keyword)}(?![a-z0-9])", url_content)
    ]

    if matched_keywords:
        return Finding(
            id="URL004",
            category="Sensitive keywords",
            title="The link contains sensitive account-related words",
            description=(
                "This link contains words commonly used on account "
                "verification, login, or payment pages. These words "
                "can also appear on legitimate websites, so they are "
                "not proof of phishing."
            ),
            evidence=(
                "Words found in the link: "
                + ", ".join(matched_keywords)
                + "."
            ),
            severity=Severity.LOW,
        )

    return None
def analyze_url(url: str) -> DetectionResponse:
    """Analyze a URL and return a complete detection response."""

    # Step 1: Parse the submitted URL
    try:
        parsed_url = urlparse(url.strip())

        if (
           parsed_url.scheme.lower() not in {"http", "https"}
           or not parsed_url.hostname
           or any(char.isspace() for char in url.strip())
        ):
           raise ValueError("Invalid URL")

        # Validate the port if one is provided
        _ = parsed_url.port

        # Reject hostnames with invalid IP address syntax
        hostname = parsed_url.hostname

        if not hostname:
            raise ValueError("Invalid hostname")

        hostname = parsed_url.hostname

    except (ValueError, AttributeError):
        return DetectionResponse(
            analysis_type=AnalysisType.URL,
            status=DetectionStatus.UNABLE_TO_DETERMINE,
            summary="We could not analyze this link because its format is invalid.",
            findings=[],
            recommendations=[
                Recommendation(
                    title="Check the link",
                    description="Make sure you enter a complete website address beginning with http:// or https://.",
                    priority=Severity.MEDIUM,
                )
            ],
            limitations=[
                "The submitted text could not be recognized as a valid HTTP or HTTPS URL."
            ],
        )

    # Step 2: Run all four detection checks
    

    checks = [
        check_ip_address(hostname),
        check_http_scheme(parsed_url.scheme),
        check_url_shortener(hostname),
        check_sensitive_keywords(url),
    ]

    # Step 3: Collect findings
    findings = [finding for finding in checks if finding is not None]

    # Step 4: Determine the overall detection status
    if any(finding.severity == Severity.HIGH for finding in findings):
        status = DetectionStatus.POTENTIALLY_MALICIOUS

    elif findings:
        status = DetectionStatus.SUSPICIOUS

    else:
        status = DetectionStatus.NO_OBVIOUS_THREAT

    # Step 5: Create a simple explanation
    if status == DetectionStatus.SUSPICIOUS:
        summary = (
            f"We found {len(findings)} characteristic(s) that deserve attention. "
            "This does not prove the link is malicious."
        )
    else:
        summary = (
            "We did not find any of the suspicious characteristics "
            "checked by our current URL detection rules. "
            "This does not guarantee that the link is safe."
        )

    # Step 6: Provide recommendations
    recommendations = [
        Recommendation(
            title="Verify the website",
            description=(
                "Check that the domain belongs to the organization "
                "you intended to visit."
            ),
            priority=Severity.MEDIUM,
        ),
        Recommendation(
            title="Protect your personal information",
            description=(
                "Do not enter passwords, banking details, or other "
                "sensitive information unless you trust the website."
            ),
            priority=Severity.HIGH,
        ),
    ]

    # Step 7: Return the complete response
    return DetectionResponse(
        analysis_type=AnalysisType.URL,
        status=status,
        summary=summary,
        findings=findings,
        recommendations=recommendations,
        limitations=[
            "The analyzer examines the URL text only and does not visit the website.",
            "It does not verify the website's ownership or reputation.",
            "A suspicious characteristic does not automatically mean a link is malicious.",
            "A link with no detected issues may still be dangerous."
        ],
    )