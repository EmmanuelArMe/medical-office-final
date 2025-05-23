# Authentication Setup and Usage Guide

This guide explains how to set up the necessary environment variables, install dependencies, and use the JWT-based authentication system for this API.

## 1. Environment Variables

The application uses a `.env` file to manage environment variables.

1.  **Create or Update `.env` file**:
    Ensure you have a `.env` file in the root directory of the project. If not, create one.

2.  **Set `SECRET_KEY`**:
    This is a critical variable used to sign and verify JWTs. It should be a long, random, and secret string. Add or update the following line in your `.env` file:

    ```
    SECRET_KEY='your_very_strong_and_secret_key_here'
    ```
    **Important**: Replace `'your_very_strong_and_secret_key_here'` with a securely generated key. You can generate one using Python's `secrets` module:
    `python -c "import secrets; print(secrets.token_hex(32))"`

3.  **Other Variables**:
    Your `.env` file should also contain database configuration and other settings as previously defined (e.g., `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `JWT_EXPIRATION`). Example:
    ```
    DB_HOST=localhost
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_NAME=medical_office
    DB_PORT=3306
    JWT_EXPIRATION=3600 # Token expiration time in seconds (e.g., 3600 for 1 hour)
    API_PORT=5000
    DEBUG_MODE=True
    ```

## 2. Install Dependencies

If you haven't installed the project dependencies or have pulled recent changes, install or update them using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```
It's recommended to do this within a virtual environment.

## 3. Running the Application

Once the environment variables are set and dependencies are installed, you can run the FastAPI application using Uvicorn (as configured in `main.py` or your run script):

```bash
uvicorn main:app --reload --port 5000
```
Adjust the port if `API_PORT` in your `.env` file is different.

## 4. Using the Authentication System

### 4.1. Creating a User

*   Ensure you have a user in the database. You can create one via the `POST /api/usuarios` endpoint.
    *   **Request Body Example** (for `POST /api/usuarios`):
        ```json
        {
          "username": "testuser",
          "password": "testpassword123",
          "rol_id": 1 # Replace with a valid role ID
        }
        ```
    *   **Note**: The password will be hashed automatically upon creation.

### 4.2. Logging In (Getting a Token)

*   To get an access token, send a `POST` request to the `/api/login` endpoint.
*   The request body must be `x-www-form-urlencoded` with `username` and `password` fields.
*   **Example using `curl`**:
    ```bash
    curl -X POST "http://localhost:5000/api/login" \
         -H "Content-Type: application/x-www-form-urlencoded" \
         -d "username=testuser&password=testpassword123"
    ```
*   **Successful Response Example**:
    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "token_type": "bearer"
    }
    ```

### 4.3. Accessing Protected Endpoints

*   Once you have an `access_token`, you must include it in the `Authorization` header of your requests to protected endpoints, using the `Bearer` scheme.
*   **Example using `curl`** (assuming you want to access `GET /api/pacientes`):
    ```bash
    TOKEN="your_access_token_here" # Replace with the token from the login step
    curl -X GET "http://localhost:5000/api/pacientes" \
         -H "Authorization: Bearer $TOKEN"
    ```
*   If the token is missing, invalid, or expired, you will receive a `401 Unauthorized` error.

This completes the setup and basic usage guide for the JWT authentication.
```
