# Intelligent-ATM-System-AI-Security
An Intelligent ATM Banking System featuring fingerprint-based authentication, AI-powered liveness detection using MediaPipe Face Mesh, email OTP verification, and customer profile visualization for enhanced banking security.
# Intelligent ATM Banking System with AI-Based Security and Profile Visualization

## Project Overview

The Intelligent ATM Banking System is a software-based banking solution designed to enhance ATM security through fingerprint-based biometric authentication, AI-powered facial liveness detection, and email-based OTP verification.

The system aims to minimize unauthorized ATM access by combining biometric verification with multiple security layers. It also introduces customer profile visualization, allowing users to view their personal banking information on the ATM interface after successful authentication.

## Objectives

- To develop a secure and intelligent ATM banking system.
- To implement fingerprint-based biometric authentication.
- To integrate AI-based facial liveness detection to distinguish real users from spoofing attempts.
- To provide an additional security layer through email OTP verification.
- To display customer profile information through an interactive ATM interface.
- To improve the security and user experience of ATM transactions.

## Key Features

### 1. Fingerprint Authentication
Provides biometric user verification through registered fingerprint data, reducing dependence on traditional ATM cards and PIN-based access.

### 2. AI-Based Liveness Detection
Uses MediaPipe Face Mesh for facial landmark detection and eye-blink monitoring. Users are prompted to blink three times to verify their physical presence.

### 3. Randomized Blink Verification
Implements randomized blink prompts to make authentication more resistant to prerecorded video-based spoofing attempts.

### 4. Email OTP Verification
Provides an additional authentication layer by sending a one-time password to the user's registered email address.

### 5. Customer Profile Visualization
Displays customer information, including name, account number, account balance, and profile picture, after successful authentication.

### 6. ATM Banking Operations
Provides access to banking functionalities after successful completion of the authentication process.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend Framework | Flask |
| Frontend | HTML, CSS, JavaScript |
| Database | MySQL |
| Facial Landmark Detection | MediaPipe Face Mesh |
| Biometric Authentication | Fingerprint Recognition |
| OTP Verification | Email-based OTP |

## System Workflow

1. The user initiates the ATM authentication process.
2. The system verifies the user's registered fingerprint.
3. Facial liveness detection is performed through randomized eye-blink prompts.
4. An OTP is sent to the user's registered email address.
5. The user enters the OTP for additional verification.
6. Upon successful authentication, the customer profile is displayed.
7. The user can access the available banking operations.

## Performance

The experimental evaluation reported the following results:

- Authentication Accuracy: 95.7%
- Average Processing Time: 12.4 seconds

*These are the reported experimental results from the project evaluation.*

## Project Architecture

The system integrates a Flask-based backend, a web-based user interface, a MySQL database, fingerprint authentication, and MediaPipe-based facial liveness detection to provide layered ATM security.

## Installation and Execution

1. Clone the repository:

   `git clone YOUR_GITHUB_REPOSITORY_URL`

2. Navigate to the project directory:

   `cd Intelligent-ATM-System-AI-Security`

3. Create a virtual environment:

   `python -m venv venv`

4. Activate the environment on Windows:

   `venv\Scripts\activate`

5. Install the required dependencies:

   `pip install -r requirements.txt`

6. Configure the MySQL database and environment variables.

7. Run the Flask application:

   `python app.py`

8. Open the local application in your browser using the Flask development server address.

*Note: Hardware-dependent fingerprint authentication and camera-based liveness detection require the appropriate local device configuration.*

## Project Report

The detailed project report documents the system design, implementation, methodology, experimental evaluation, and results.

## Future Enhancements

- Integration of advanced biometric security mechanisms.
- Enhanced anti-spoofing techniques.
- Improved transaction monitoring and fraud detection.
- Deployment and scalability improvements.

## Author

**Chandana G**

B.E. – Artificial Intelligence and Data Science

## Acknowledgement

This project was developed as part of the undergraduate engineering curriculum, with the objective of exploring AI-driven security solutions for intelligent banking systems.
