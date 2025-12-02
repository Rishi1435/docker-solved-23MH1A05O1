**Secure 2FA Microservice**

A production-ready, containerized microservice that implements Public Key Infrastructure (PKI) and Time-based One-Time Password (TOTP) authentication. This project demonstrates secure seed transmission using RSA encryption, persistent storage management, and automated background tasks using Cron.

**🚀 Features**

Secure Seed Transmission: Decrypts RSA-encrypted seeds using OAEP padding with SHA-256.

TOTP Generation: Generates standard 6-digit 2FA codes (RFC 6238 compliant).

Verification Logic: Verifies codes with a time-window tolerance of ±30 seconds.

Dockerized: Fully containerized using a multi-stage Docker build for optimized image size.

Automated Logging: Background Cron job logs valid 2FA codes every minute.

Persistence: Uses Docker Volumes to ensure seed data survives container restarts.

**🛠️ Tech Stack**

Language: Python 3.11

Framework: FastAPI

Cryptography: cryptography (RSA/OAEP), pyotp (TOTP), hashlib

Containerization: Docker & Docker Compose

Scheduling: Linux Cron

**📂 Project Structure**

├── main.py                 # FastAPI application and logic

├── Dockerfile              # Multi-stage build configuration

├── docker-compose.yml      # Service and volume definition

├── requirements.txt        # Python dependencies

├── cron/

│   └── 2fa-cron            # Cron schedule configuration

├── scripts/

│   └── log_2fa_cron.py     # Script to log codes (runs every minute)

└── README.md


**⚙️ Setup & Installation**

Prerequisites

Docker Desktop installed and running.

Git.

*1. Clone the Repository*

git clone [https://github.com/Rishi1435/docker-solved-23MH1A05O1](https://github.com/Rishi1435/docker-solved-23MH1A05O1)
cd docker-solved-23MH1A05O1


*2. Build and Run*

Start the container using Docker Compose. This builds the image and mounts the necessary volumes.

docker-compose up --build -d


The API will be accessible at http://localhost:8080.

**🔌 API Endpoints**

*1. Decrypt Seed*

Decrypts the encrypted seed using the stored private key and saves it securely.

URL: /decrypt-seed

Method: POST

Body:

{
  "encrypted_seed": "BASE64_STRING_HERE..."
}


*2. Generate 2FA Code*

Returns the current valid TOTP code and remaining validity time.

URL: /generate-2fa

Method: GET

Response:

{
  "code": "123456",
  "valid_for": 15
}


*3. Verify Code*

Verifies a user-provided code against the stored seed (allows ±30s drift).

URL: /verify-2fa

Method: POST

Body:

{
  "code": "123456"
}


**🕰️ Cron Job & Persistence**

Cron Job: A background task runs every minute to generate a code and log it.

View Logs:

docker exec <container_name> cat /cron/last_code.txt
