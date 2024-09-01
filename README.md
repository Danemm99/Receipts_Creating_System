# Receipts Creating System

## Setup

**1. Clone the repository to your folder:**
```commandline
https://github.com/Danemm99/Receipts_Creating_System.git
```

**2. Install dependencies:**

```commandline
pip install -r requirements.txt
```

**3. Setup your database and set environment variable in .env file with needed data:**

```commandline
cp .env.example .env
```

**4. Apply all migrations:**

```commandline
alembic upgrade head
```

**5. Generate private key + public key pair:**

```commandline
mkdir certs
```

```commandline
cd certs
```

```commandline
# Generate an RSA private key, of size 2048
openssl genrsa -out jwt-private.pem 2048
```

```commandline
# Extract the public key from the key pair, which can be used in a certificate
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```

```commandline
cd ..
```

**6. Run the application:**

```commandline
uvicorn app.main.main:app --reload
```

**6. Run tests:**

```commandline
pytest app/test_api/test_receipts_api.py
```

```commandline
pytest app/test_api/test_users_api.py
```

## Endpoint documentation














