# Receipts Creating System

## Setup

**1. Clone the repository to your folder:**
```commandline
https://github.com/Danemm99/Receipts_Creating_System.git
```

**2. Navigate to the project directory:**
```commandline
cd Receipts_Creating_System
```

**3. Install dependencies:**

```commandline
pip install -r requirements.txt
```

**4. Setup your database and set environment variable in .env file with needed data:**

```commandline
cp .env.example .env
```

**5. Apply all migrations:**

```commandline
alembic upgrade head
```

**6. Generate private key + public key pair:**

```commandline
mkdir certs
```

```commandline
cd certs
```

Generate an RSA private key, of size 2048:
```commandline
openssl genrsa -out jwt-private.pem 2048
```

Extract the public key from the key pair, which can be used in a certificate:
```commandline
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```

```commandline
cd ..
```

**7. Run the application:**

```commandline
uvicorn app.main.main:app --reload
```

**8. Run tests:**

```commandline
pytest app/test_api/test_receipts_api.py
```

```commandline
pytest app/test_api/test_auth_api.py
```

## Endpoint documentation:

```commandline
localhost:8000/docs
```












