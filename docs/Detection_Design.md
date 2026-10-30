# PhishAware Detection Design

## 1. Introduction

This document describes how PhishAware identifies and analyzes potentially suspicious URLs and messages.

The purpose of the detection system is to identify warning signs, explain the evidence in understandable language, and recommend appropriate safety actions.

PhishAware does not automatically declare content malicious based on a single indicator. Instead, it evaluates available evidence and communicates uncertainty clearly.

## 2. Detection Approach

PhishAware will initially use a rule-based detection approach.

The system examines submitted URLs and messages using predefined indicators. Each detected indicator produces a finding containing:

* **Category:** The type of suspicious behavior identified.
* **Description:** A plain-language explanation.
* **Evidence:** The specific feature that triggered the finding.
* **Severity:** The relative importance of the finding.

Multiple findings may contribute to an overall assessment.

The initial version will not depend on machine learning or automatically visit submitted URLs.

## 3. URL Detection

The URL detector analyzes the structure and characteristics of a submitted URL without opening the destination.

### 3.1 URL Indicators

The initial detection rules include:

| Indicator                   | Description                                                                               |
| --------------------------- | ----------------------------------------------------------------------------------------- |
| IP address as host          | The URL uses an IP address instead of a recognizable domain name.                         |
| Misleading domain structure | The domain contains another organization's name in a way that could mislead users.        |
| Suspicious subdomain        | The URL uses an unusually structured or misleading subdomain.                             |
| Unusual URL structure       | The URL contains unusual patterns that may require additional attention.                  |
| Non-HTTPS connection        | The URL uses HTTP instead of HTTPS.                                                       |
| URL shortener               | The URL uses a shortening service that hides the destination.                             |
| Suspicious characters       | The URL contains potentially deceptive encoding or character patterns.                    |
| Sensitive keyword in path   | The URL contains terms associated with login, verification, payment, or account recovery. |

These indicators are warning signs, not proof of phishing. For example, HTTP websites and URL shorteners can have legitimate uses.

### 3.2 URL Analysis Process

1. Receive the submitted URL.
2. Validate the input format.
3. Parse the URL into its components.
4. Examine the hostname, scheme, path, query parameters, and other relevant characteristics.
5. Apply the detection rules.
6. Collect findings and supporting evidence.
7. Generate an overall assessment.
8. Provide an explanation and safety recommendations.

The system must not automatically open or follow the submitted URL during the initial analysis.

## 4. Message Detection

The message detector analyzes pasted SMS messages, emails, and chat messages.

It examines the language and content for patterns commonly associated with phishing and social engineering.

### 4.1 Message Indicators

| Indicator                     | Description                                                                                       |
| ----------------------------- | ------------------------------------------------------------------------------------------------- |
| Urgency                       | The message pressures the recipient to act immediately.                                           |
| Threats                       | The message threatens account suspension, financial loss, or other consequences.                  |
| Sensitive information request | The message requests passwords, PINs, verification codes, or other sensitive information.         |
| Impersonation                 | The sender claims to represent a bank, government office, company, or other trusted organization. |
| Suspicious links              | The message contains URLs that may require further examination.                                   |
| Unexpected rewards            | The message promises prizes, money, or benefits unexpectedly.                                     |
| Payment pressure              | The message requests urgent payments or transfers.                                                |
| Unusual communication         | The message contains unexpected requests or instructions that may indicate social engineering.    |

These indicators must be interpreted in context. A message containing urgent language or a payment request is not automatically malicious.

### 4.2 Message Analysis Process

1. Receive the submitted message.
2. Validate the input.
3. Examine its wording and structure.
4. Identify suspicious language and requests.
5. Extract URLs, email addresses, or other relevant indicators where appropriate.
6. Apply the detection rules.
7. Collect findings and supporting evidence.
8. Generate an overall assessment.
9. Provide an explanation and safety recommendations.

## 5. Severity Classification

Each finding will have one of three severity levels:

| Severity | Meaning                                                                          |
| -------- | -------------------------------------------------------------------------------- |
| Low      | A weak warning sign that requires attention but may be legitimate.               |
| Medium   | A concerning indicator that deserves further verification.                       |
| High     | A strong warning sign that may indicate a significant phishing or security risk. |

Severity describes the importance of an individual finding. It does not independently establish whether the submitted content is malicious.

## 6. Overall Analysis Results

Every analysis must return one of four assessment categories:

| Category                     | Meaning                                                                                |
| ---------------------------- | -------------------------------------------------------------------------------------- |
| `potentially_malicious`      | Available evidence indicates a significant possibility of malicious activity.          |
| `suspicious`                 | One or more concerning indicators were identified, but the evidence is not conclusive. |
| `no_obvious_threat_detected` | The analysis did not identify obvious warning signs. This does not guarantee safety.   |
| `unable_to_determine`        | The system could not analyze the submission reliably.                                  |

The overall assessment must consider the available findings, their context, and the limitations of the detection process.

## 7. Finding and Response Structure

Each finding should contain:

```json
{
  "id": "finding-001",
  "category": "urgency",
  "description": "The message pressures the recipient to act immediately.",
  "evidence": "Your account will be suspended within 24 hours.",
  "severity": "medium"
}
```

The overall analysis response should follow a consistent structure:

```json
{
  "analysis_type": "message",
  "status": "suspicious",
  "summary": "The message contains signs commonly associated with phishing.",
  "findings": [],
  "recommendations": [
    "Do not click links until the message is verified.",
    "Contact the organization through its official communication channels."
  ],
  "limitations": [
    "The sender's identity has not been independently verified."
  ]
}
```

Both URL and message analysis should use the same overall response structure wherever possible.

## 8. Recommendations and User Guidance

Recommendations should be practical, clear, and related to the detected findings.

Examples include:

* Avoid clicking suspicious links.
* Do not share passwords, PINs, or verification codes.
* Verify unexpected requests through an organization's official website or phone number.
* Do not send money in response to unverified messages.
* Report suspected phishing messages to the relevant organization or service provider.

The system should explain why each recommendation is relevant.

## 9. False Positives and Limitations

PhishAware must recognize that legitimate content can contain suspicious-looking characteristics.

Examples include:

* A legitimate website may use HTTP.
* A genuine message may contain urgent language.
* A URL shortener may be used for ordinary communication.
* A legitimate organization may request users to verify account information through official channels.

Therefore:

1. A single indicator must not automatically establish that content is malicious.
2. Findings must include understandable supporting evidence.
3. The system must communicate uncertainty.
4. Users must not be encouraged to trust content simply because no warning signs were found.
5. Detection limitations must be disclosed.

## 10. Privacy and Security Considerations

* Submitted URLs must not be automatically opened during initial analysis.
* Raw messages and URLs should not be unnecessarily stored.
* Sensitive information should not appear in application logs.
* Input length and format must be validated.
* External threat-intelligence services, if introduced later, must be evaluated for privacy and security.
* User submissions must be handled securely.

## 11. Testing Strategy

Each detection rule must have test cases covering:

* A suspicious example that should trigger the rule.
* A legitimate example that should not trigger the rule.
* An edge case that tests the rule's limitations.
* Invalid or incomplete input where relevant.

Testing must also verify that:

* Findings contain the required fields.
* Severity values are valid.
* Overall assessment categories are valid.
* Recommendations are understandable.
* The system handles uncertain results appropriately.

## 12. Future Improvements

Potential future improvements include:

* Integration with trusted threat-intelligence services.
* More advanced domain and URL reputation checks.
* Improved multilingual message analysis, including Amharic.
* Voice-message transcription and analysis.
* Improved detection methods based on carefully evaluated datasets.

These improvements will be considered after the initial rule-based system is implemented and tested.

## 13. Design Principles

PhishAware detection must follow these principles:

1. **Explainability:** Every finding should have understandable supporting evidence.
2. **Transparency:** Communicate uncertainty and limitations honestly.
3. **Accessibility:** Present results in language that users with different abilities and technical backgrounds can understand.
4. **Privacy:** Avoid unnecessary collection and retention of user data.
5. **Safety:** Provide practical recommendations that help users avoid harm.
6. **Consistency:** Use a common response structure for URL and message analysis.
