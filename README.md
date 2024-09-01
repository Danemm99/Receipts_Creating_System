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

### **User Endpoints**

#### **Register User**

*   **URL:** /register/
    
*   **Method:** POST
    
*   **Description:** Registers a new user.
    
*   **Parameters:**
    
    *   user: A JSON object with the following fields:
        
        *   username (string): The user's unique username.
            
        *   name (string): The user's full name.
            
        *   password (string): The user's password.
            
*   **Response:** A JSON object with the registered user's username and name.
    

#### **Login User**

*   **URL:** /login/
    
*   **Method:** POST
    
*   **Description:** Authenticates a user and returns a JWT token.
    
*   **Parameters:**
    
    *   user: A JSON object with the following fields:
        
        *   username (string): The user's username.
            
        *   password (string): The user's password.
            
*   **Response:** A JSON object with an access\_token (JWT token) and token\_type (bearer).
    

#### **Get Current User**

*   **URL:** /me/
    
*   **Method:** GET
    
*   **Description:** Retrieves information about the currently authenticated user.
    
*   **Parameters:** None
    
*   **Response:** A JSON object with the current user's username and name.
    

### **Receipt Endpoints**

#### **Create Receipt**

*   **URL:** /create\_receipt/
    
*   **Method:** POST
    
*   **Description:** Creates a new receipt for the authenticated user.
    
*   **Parameters:**
    
    *   receipt\_id: A JSON object with the following fields:
        
        *   products (list of ProductSchema): The products included in the receipt.
            
        *   payment\_type (string): The type of payment used, either "cash" or "cashless."
            
        *   payment\_amount (float): The total payment amount.
            
*   **Response:** A JSON object with the created receipt's details, including its id, products, payment\_type, payment\_amount, total, rest, and created\_at.
    

#### **Get Receipts**

*   **URL:** /get\_receipts/
    
*   **Method:** GET
    
*   **Description:** Retrieves a list of receipts for the authenticated user, filtered by the provided parameters.
    
*   **Parameters:**
    
    *   filters (optional): A JSON object with the following fields:
        
        *   created\_from (datetime): Filter receipts created from this date.
            
        *   created\_to (datetime): Filter receipts created up to this date.
            
        *   min\_total (float): Filter receipts with a minimum total amount.
            
        *   max\_total (float): Filter receipts with a maximum total amount.
            
        *   payment\_type (string): Filter receipts by payment type.
            
    *   pagination (optional): A JSON object with the following fields:
        
        *   page (int): The page number for pagination (default is 1).
            
        *   page\_size (int): The number of receipts per page (default is 10).
            
*   **Response:** A JSON list of receipt objects, each including details like id, created\_at, total, payment\_type, payment\_amount, rest, and products.
    

#### **Get Receipt by ID**

*   **URL:** /get\_receipt/{receipt\_id}
    
*   **Method:** GET
    
*   **Description:** Retrieves a specific receipt by its ID for the authenticated user.
    
*   **Parameters:**
    
    *   receipt\_id (int): The ID of the receipt to retrieve.
        
*   **Response:** A JSON object with the receipt's details.
    

#### **Get Public Receipt**

*   **URL:** /public/{receipt\_id}
    
*   **Method:** GET
    
*   **Description:** Retrieves a public receipt in plain text format, suitable for sharing without authentication.
    
*   **Parameters:**
    
    *   receipt\_id (int): The ID of the receipt to retrieve.
        
    *   line\_length (int, optional): The number of characters per line in the receipt (default is 40, minimum is 30).
        
*   **Response:** A plain text representation of the receipt.












