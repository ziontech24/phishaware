# PhishAware — Project Specification

## 1. Project Overview

PhishAware is an accessibility-first, privacy-conscious phishing detection and security awareness web application.

It helps users analyze suspicious URLs and messages, understand potential phishing indicators, and learn how to respond safely.

The project aims to make cybersecurity awareness more accessible to people with different abilities, technical backgrounds, and levels of digital literacy.

## 2. Problem Statement

Phishing attacks often use deceptive links, impersonation, urgency, and requests for sensitive information to trick people into taking unsafe actions.

Many detection tools focus primarily on identifying threats without sufficiently explaining their results or considering accessibility, privacy, and differences in users' technical knowledge.

PhishAware aims to address these concerns by combining understandable phishing analysis, accessible interaction, privacy-conscious design, and educational guidance.

## 3. Project Objectives

The objectives are to:

1. Analyze suspicious URLs and identify potentially dangerous characteristics.
2. Analyze pasted SMS messages, emails, and chat messages for phishing indicators.
3. Explain the evidence supporting each analysis result.
4. Provide clear and practical safety recommendations.
5. Design an interface that supports keyboard navigation and assistive technologies.
6. Minimize the collection and retention of submitted information.
7. Make security explanations understandable to users with different levels of technical knowledge.
8. Establish a foundation for English and Amharic language support.

## 4. Target Users

PhishAware is intended for:

* General internet users.
* Students and educators.
* People with limited cybersecurity knowledge.
* Blind and visually impaired users.
* Deaf and hard-of-hearing users.
* People who benefit from simplified language and clear instructions.
* Anyone who wants to assess suspicious links or messages.

The application should not assume that users have advanced technical knowledge.

## 5. Core Features

### 5.1 URL Analysis

Users can submit a URL for analysis.

The system will examine available URL characteristics and identify suspicious indicators without automatically navigating to the submitted destination.

### 5.2 Message Analysis

Users can paste suspicious SMS messages, emails, or chat messages.

The system will examine the text for possible phishing indicators, such as urgency, impersonation, suspicious link patterns, and requests for sensitive information.

### 5.3 Explainable Results

The application will present a result category, supporting evidence, and recommended next steps.

Possible result categories include:

* Potentially malicious.
* Suspicious.
* No obvious threat detected.
* Unable to determine.

The wording must not imply that a URL or message is guaranteed to be safe.

### 5.4 Accessible Interface

The interface will be designed with:

* Semantic HTML.
* Keyboard accessibility.
* Screen-reader support.
* Clear labels and instructions.
* Sufficient text contrast.
* Accessible result announcements.
* Text-based feedback that does not rely on sound or color alone.

The project will use WCAG 2.2 Level AA as an accessibility target and test relevant requirements throughout development.

### 5.5 Privacy-Conscious Processing

The system will minimize the collection and retention of submitted information.

It will avoid logging raw submitted messages unnecessarily, protect configuration secrets, and disclose external data sharing before introducing services that transmit submitted content.

### 5.6 Security Awareness

The application will explain detected indicators in plain language and provide practical recommendations for safer behavior.

### 5.7 Language Support

The initial interface and explanations will be developed in English.

Amharic support is a planned feature that will be introduced after the core analysis and interface functionality are established.

## 6. Technology Stack

### Frontend

* React.
* JavaScript.
* Vite.
* CSS.

### Backend

* Python.
* FastAPI.
* Pydantic for request and response validation.
* Pytest for backend testing.

### Development and Version Control

* Git.
* GitHub.
* Visual Studio Code.
* GitHub Actions for automated testing in a later milestone.

Additional detection libraries and threat-intelligence services will be evaluated when needed.

## 7. Initial System Design

The application will contain three primary layers:

1. Frontend: accepts user input and displays analysis results.
2. Backend API: validates requests and coordinates analysis.
3. Detection engine: examines URLs and messages, then returns findings and explanations.

The frontend and backend will communicate through a documented API.

The initial implementation will use local analysis rules. External threat-intelligence services and machine-learning models may be considered later.

## 8. Privacy and Security Requirements

* Do not automatically visit submitted URLs.
* Validate user input on the backend.
* Avoid storing submitted messages unless storage becomes necessary and is explicitly designed.
* Do not log raw submitted content unnecessarily.
* Never commit API keys, passwords, or other secrets.
* Clearly disclose external services that receive submitted data.
* Use defensive error handling.
* Communicate uncertainty and detection limitations.
* If external URL retrieval is introduced later, implement appropriate protections against server-side request forgery (SSRF).

## 9. Project Scope

### Initial Release

The initial release will focus on:

* URL analysis.
* Pasted-message analysis.
* Explainable results.
* Accessible user interaction.
* Privacy-conscious processing.
* Safety recommendations.
* Automated tests.
* Clear documentation.

### Future Enhancements

Potential future improvements include:

* Amharic interface and explanations.
* External threat-intelligence integration.
* Machine-learning-assisted detection.
* More extensive educational resources.
* Additional language support.

These enhancements will be evaluated after the initial release is working reliably.

## 10. Limitations

PhishAware cannot guarantee that every phishing attempt will be detected.

A result indicating no obvious threat does not prove that content is safe.

Detection accuracy will depend on the available evidence, analysis methods, and any external intelligence sources that may be introduced.

Accessibility and privacy claims will be supported by implementation and testing rather than assumed from design intentions.

## 11. Success Criteria

The initial release will be considered successful when:

* Users can submit URLs and receive structured analysis results.
* Users can submit messages and receive structured analysis results.
* Results include understandable evidence and safety guidance.
* Backend validation and error handling are tested.
* Core interface interactions work using a keyboard.
* Relevant screen-reader and accessibility checks have been performed.
* Automated tests cover the main analysis and API functionality.
* Privacy practices are documented and reflected in the implementation.
* Installation and usage instructions are available in the repository.
