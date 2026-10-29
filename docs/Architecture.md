# PhishAware — System Architecture

## 1. Introduction

This document describes the proposed system architecture of PhishAware, an accessibility-first and privacy-conscious phishing detection application.

It defines the main application components, their responsibilities, communication methods, data flow, and security considerations.

The architecture is based on the initial project specification and is intended to guide implementation.

The initial system will support two primary analysis capabilities:

* URL analysis.
* Suspicious message analysis.

Voice-message analysis is planned for a future version and is not part of the initial implementation.

## 2. Architectural Overview

PhishAware will use a layered architecture consisting of three primary layers:

1. Frontend Layer.
2. Backend API Layer.
3. Detection and Explanation Layer.

Each layer will have clearly defined responsibilities.

### 2.1 Frontend Layer

**Technology:** React, JavaScript, Vite, CSS.

The frontend provides the user interface through which users interact with PhishAware.

Responsibilities:

* Accept URLs and suspicious messages.
* Provide input validation and helpful instructions.
* Send analysis requests to the backend API.
* Display loading and error states.
* Present analysis results.
* Display detected indicators and their explanations.
* Provide practical safety recommendations.
* Support accessible interaction and responsive layouts.

### 2.2 Backend API Layer

**Technology:** Python and FastAPI.

The backend acts as the communication layer between the frontend and detection engine.

Responsibilities:

* Receive requests from the frontend.
* Validate submitted information.
* Apply input-size and format restrictions.
* Route requests to the appropriate detection service.
* Collect and organize analysis findings.
* Generate consistent API responses.
* Handle errors safely.

### 2.3 Detection and Explanation Layer

**Technology:** Python.

This layer performs the actual analysis and prepares understandable results.

It will contain:

**URL Detector**

* Examines URL characteristics.
* Identifies suspicious domain patterns.
* Checks for possible impersonation and deceptive structures.
* Returns structured findings.

**Message Detector**

* Examines pasted message content.
* Identifies suspicious language patterns.
* Detects possible urgency, impersonation, threats, and sensitive-information requests.
* Returns structured findings.

**Explanation Component**

* Converts technical findings into plain-language explanations.
* Explains why each indicator may be suspicious.
* Provides relevant safety recommendations.
* Generates short contextual reminders.

The explanation component must use actual detection findings rather than inventing evidence.

## 3. High-Level Architecture

The initial architecture follows this communication structure:

```text
             USER
               |
               v
      REACT FRONTEND
               |
               | HTTP Requests
               v
       FASTAPI BACKEND
               |
               v
       REQUEST VALIDATION
               |
               v
       ANALYSIS ROUTER
          /        \
         /          \
        v            v
   URL DETECTOR   MESSAGE DETECTOR
        |            |
        v            v
   URL FINDINGS   MESSAGE FINDINGS
         \          /
          \        /
           v      v
       EXPLANATION COMPONENT
               |
               v
       STRUCTURED RESULTS
               |
               v
        FASTAPI RESPONSE
               |
               v
         REACT FRONTEND
               |
               v
        DISPLAY RESULTS
               |
               v
             USER
```

The frontend will not implement the detection rules itself. Analysis will be performed by the backend.

## 4. Frontend Architecture

The frontend will use React components to separate interface responsibilities.

### 4.1 Proposed Frontend Structure

```text
frontend/
├── public/
├── src/
│   ├── components/
│   │   ├── Header.jsx
│   │   ├── Navigation.jsx
│   │   ├── InputForm.jsx
│   │   ├── ResultCard.jsx
│   │   ├── FindingList.jsx
│   │   ├── SafetyRecommendations.jsx
│   │   └── LoadingState.jsx
│   │
│   ├── features/
│   │   ├── url-analysis/
│   │   └── message-analysis/
│   │
│   ├── services/
│   │   └── api.js
│   │
│   ├── hooks/
│   ├── utils/
│   ├── styles/
│   ├── App.jsx
│   └── main.jsx
│
├── tests/
├── package.json
└── vite.config.js
```

This is a proposed structure. Files and folders will be created as their functionality is implemented.

### 4.2 Component Responsibilities

| Component             | Responsibility                                |
| --------------------- | --------------------------------------------- |
| Header                | Display application branding and navigation.  |
| Navigation            | Support navigation between application views. |
| InputForm             | Accept user-submitted URLs or messages.       |
| ResultCard            | Display the overall assessment.               |
| FindingList           | Present detected indicators and explanations. |
| SafetyRecommendations | Display recommended actions.                  |
| LoadingState          | Communicate when analysis is processing.      |

The frontend will use a shared result presentation structure for both URL and message analysis.

This avoids duplicating interface functionality.

## 5. Backend Architecture

The backend will use FastAPI to expose endpoints and coordinate analysis.

### 5.1 Proposed Backend Structure

```text
backend/
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── url.py
│   │       └── message.py
│   │
│   ├── schemas/
│   │   ├── requests.py
│   │   └── responses.py
│   │
│   ├── detectors/
│   │   ├── url_detector.py
│   │   └── message_detector.py
│   │
│   ├── services/
│   │   ├── analysis_service.py
│   │   └── explanation_service.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   └── main.py
│
├── tests/
├── requirements.txt
└── README.md
```

The structure separates API handling, validation, detection, and explanation responsibilities.

### 5.2 Backend Responsibilities

**API Routes**

Receive frontend requests and return analysis results.

**Schemas**

Define the expected request and response structures using Pydantic.

**Detectors**

Implement URL and message detection rules.

**Analysis Service**

Coordinate the appropriate detector and organize the findings.

**Explanation Service**

Generate understandable explanations and relevant safety recommendations.

**Main Application**

Initialize FastAPI and register the API routes.

## 6. Detection Engine Design

The detection engine will initially use locally implemented, rule-based analysis.

This approach allows the project to begin without depending on external threat-intelligence services or machine-learning models.

### 6.1 URL Detection

The URL detector will examine characteristics such as:

* Domain structure.
* Suspicious subdomains.
* Lookalike domain patterns.
* Misleading use of trusted organization names.
* Unusual URL encoding.
* Suspicious URL structures.
* Other indicators supported by implemented rules.

The detector will return structured findings describing the observed characteristics.

The initial version will not automatically visit submitted URLs or retrieve their webpage content.

### 6.2 Message Detection

The message detector will examine submitted text for indicators such as:

* Urgency and pressure.
* Threats involving account suspension or financial consequences.
* Requests for passwords or verification codes.
* Unexpected requests for payments.
* Possible impersonation.
* Suspicious links.
* Other social-engineering patterns.

The detector will identify relevant text patterns and provide supporting evidence.

It must avoid treating individual words or phrases as automatic proof of phishing.

### 6.3 Detection Findings

Both detectors should return findings using a consistent internal structure.

A finding may contain:

| Field         | Description                                     |
| ------------- | ----------------------------------------------- |
| `id`          | Unique identifier for the finding.              |
| `category`    | Type of suspicious indicator.                   |
| `description` | Description of the observed evidence.           |
| `evidence`    | Relevant URL characteristic or message excerpt. |
| `severity`    | Relative importance of the indicator.           |

The exact schema will be finalized during implementation.

## 7. Explanation and Recommendation Design

The explanation component will transform technical findings into understandable information.

It will be responsible for:

1. Summarizing the analysis.
2. Explaining identified indicators.
3. Describing why the evidence may be concerning.
4. Providing practical safety recommendations.
5. Including a short reminder about similar warning signs.

For example:

**Detected indicator:** Urgent account suspension threat.

**Technical finding:** The message pressures the recipient to take immediate action to avoid an alleged account suspension.

**Plain-language explanation:** Scammers sometimes create fear by threatening to close accounts so people act without checking whether the message is genuine.

**Recommended action:** Do not click the provided link. Contact the organization through its official website or another trusted communication channel.

**Remember for next time:** Unexpected threats that demand immediate action deserve extra caution.

The explanation component must distinguish between observed evidence and possible interpretations.

It must not claim that a message is malicious solely because one suspicious indicator is present.

## 8. API Communication Design

The frontend and backend will communicate through HTTP requests using JSON.

The initial API will expose the following endpoints.

| Method | Endpoint               | Purpose                      |
| ------ | ---------------------- | ---------------------------- |
| GET    | `/api/v1/health`       | Check backend availability.  |
| POST   | `/api/v1/scan/url`     | Analyze a submitted URL.     |
| POST   | `/api/v1/scan/message` | Analyze a submitted message. |

### 8.1 URL Analysis Request

Example:

```json
{
  "url": "https://example.com"
}
```

### 8.2 Message Analysis Request

Example:

```json
{
  "message": "Your account will be suspended. Click this link immediately."
}
```

These are illustrative requests. The final validation rules and schemas will be established during implementation.

### 8.3 Standard Analysis Response

Both analysis endpoints should return a consistent response structure.

Example:

```json
{
  "analysis_type": "message",
  "status": "suspicious",
  "summary": "This message contains potential phishing indicators.",
  "findings": [
    {
      "id": "finding-001",
      "category": "urgency",
      "severity": "medium",
      "description": "The message pressures the recipient to act immediately.",
      "evidence": "Click this link immediately."
    }
  ],
  "recommendations": [
    "Do not click unexpected links.",
    "Verify the request through an official communication channel."
  ],
  "reminder": "Be cautious of messages that pressure you to act without checking their authenticity."
}
```

The response structure is a proposed contract and will be refined as the detection functionality develops.

Possible assessment statuses include:

* `potentially_malicious`
* `suspicious`
* `no_obvious_threat_detected`
* `unable_to_determine`

The API must also support appropriate validation and error responses.

## 9. Data Flow

### 9.1 URL Analysis Flow

1. The user enters a URL into the frontend.
2. The frontend submits the URL to the backend.
3. The backend validates the request.
4. The analysis service calls the URL detector.
5. The URL detector examines available characteristics.
6. Findings are passed to the explanation component.
7. The backend organizes the results.
8. The API returns a structured response.
9. The frontend displays the assessment, evidence, explanations, and recommendations.

### 9.2 Message Analysis Flow

1. The user pastes a suspicious message.
2. The frontend submits the message to the backend.
3. The backend validates the request.
4. The analysis service calls the message detector.
5. The message detector examines the text.
6. Findings are passed to the explanation component.
7. The backend organizes the results.
8. The API returns a structured response.
9. The frontend displays the assessment, evidence, explanations, and recommendations.

Both workflows will use the same overall result presentation approach.

## 10. Security and Privacy Architecture

Security and privacy will be considered throughout the application.

### 10.1 Input Validation

* Validate all incoming requests on the backend.
* Apply reasonable input-size restrictions.
* Reject malformed or unsupported input.
* Avoid processing unexpected data formats.

### 10.2 URL Safety

* Do not automatically navigate to submitted URLs.
* Analyze URL characteristics without contacting the destination.
* Treat submitted URLs as untrusted input.
* Introduce SSRF protections before implementing any future server-side URL retrieval.

### 10.3 Data Privacy

* Do not introduce a database in the initial release.
* Process submitted content in memory where practical.
* Avoid unnecessary retention of submitted information.
* Avoid logging raw URLs and messages.
* Document any external service that receives user-submitted information.

### 10.4 Application Security

* Keep API keys and configuration secrets outside source control.
* Use environment variables for sensitive configuration.
* Configure CORS for the intended frontend origin.
* Return safe error messages.
* Avoid exposing internal implementation details.
* Test security-related behavior during development.

### 10.5 Accessibility

* Use semantic HTML.
* Support keyboard navigation.
* Provide screen-reader-compatible labels and announcements.
* Ensure sufficient contrast.
* Communicate important results through text rather than color alone.

## 11. Database and Data Storage Decisions

The initial version will not require a database.

This decision is based on the initial application scope:

* No user registration.
* No authentication.
* No permanent analysis history.
* No user profile management.
* No requirement to permanently store submitted URLs or messages.

Analysis requests will be processed without intentionally retaining submitted content after processing.

Future database integration will only be considered if a clearly justified feature requires persistent storage and its privacy and security implications have been evaluated.

## 12. Future Voice-Message Integration

Voice-message phishing analysis is planned for a future major version.

It will extend the existing architecture rather than replace the current URL and message analysis workflows.

The proposed future workflow is:

```text
       AUDIO UPLOAD
             |
             v
       FILE VALIDATION
             |
             v
       SPEECH-TO-TEXT
             |
             v
       TRANSCRIPT REVIEW
             |
             v
       MESSAGE DETECTOR
             |
             v
       OPTIONAL CONTEXT
       (PHONE, URL, EMAIL)
             |
             v
       EVIDENCE COMBINATION
             |
             v
       EXPLANATION COMPONENT
             |
             v
       STRUCTURED RESULTS
```

The feature will require additional components for:

* Secure audio upload.
* Audio format and size validation.
* Speech-to-text processing.
* Transcript review and correction.
* Optional contact-information analysis.
* Additional privacy controls.

Voice characteristics, accents, emotions, and speaking styles will not be treated as reliable indicators of dishonesty.

The existing explanation and recommendation approach will be reused so that voice analysis provides the same understandable result experience.

## 13. Testing Strategy

Testing will cover the individual components and their integration.

### Frontend Testing

* Input validation.
* Component behavior.
* Result presentation.
* Loading and error states.
* Keyboard interaction.
* Accessibility checks.

### Backend Testing

* API request validation.
* URL detection rules.
* Message detection rules.
* Explanation generation.
* Response structure.
* Error handling.

### Integration Testing

* Frontend-to-backend communication.
* URL analysis workflow.
* Message analysis workflow.
* Correct presentation of returned findings.
* Privacy-related processing behavior.

Automated testing will be implemented throughout development, with GitHub Actions introduced in a later milestone.

## 14. Architecture Decisions and Future Considerations

The following decisions will guide the initial implementation:

| Area                  | Initial Decision                   |
| --------------------- | ---------------------------------- |
| Frontend              | React with JavaScript and Vite     |
| Backend               | Python with FastAPI                |
| Detection             | Local rule-based analysis          |
| Communication         | HTTP and JSON                      |
| Validation            | Pydantic                           |
| Testing               | Pytest and frontend testing tools  |
| Database              | Not required initially             |
| URL retrieval         | Not included initially             |
| External intelligence | Future consideration               |
| Machine learning      | Future consideration               |
| Voice analysis        | Future major version               |
| Language              | English initially; Amharic planned |

The architecture may evolve as implementation reveals additional requirements. Significant changes should be documented and evaluated against the original project specification.

## 15. Conclusion

The proposed PhishAware architecture separates user interaction, API communication, detection, and explanation responsibilities.

This separation will make the application easier to develop, test, maintain, and extend.

The initial implementation will prioritize URL analysis, message analysis, understandable results, accessibility, and privacy.

Future capabilities, including voice-message analysis and additional detection methods, will be introduced progressively after the core system is functioning reliably.
