import base64
import json
from functools import lru_cache

import requests
from fastapi import HTTPException
from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from config import settings

# Constants
KEYCLOAK_PUBLIC_KEY_URL = settings.KEYCLOAK_PUBLIC_KEY_URL
security = HTTPBearer()  # Enforces Bearer token in Authorization header
KEYCLOAK_CLIENT_ID = settings.KEYCLOAK_CLIENT_ID

# Cache the public key to avoid multiple calls
@lru_cache
def get_keycloak_public_key():
    response = requests.get(KEYCLOAK_PUBLIC_KEY_URL)
    response.raise_for_status()
    return response.json()  # JWKS


# Verify token and check for the required scope
def verify_and_check_scope(token: str, required_scope: str):
    jwks = get_keycloak_public_key()
    header = jwt.get_unverified_header(token)
    key = next((key for key in jwks["keys"] if key["kid"] == header["kid"]), None)

    if not key:
        raise HTTPException(status_code=401, detail="Unable to find public key")

    try:
        token_parts = token.split(".")
        payload = json.loads(base64.urlsafe_b64decode(token_parts[1] + "==").decode())
        scopes = payload.get("scope", "").split()

        # Check if required scope is present
        if required_scope not in scopes:
            raise HTTPException(status_code=403, detail="Insufficient scope")

        return payload  # Return decoded claims
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Dependency to enforce token and scope validation
def get_token_validator(required_scope: str):
    async def validate_token(credentials: HTTPAuthorizationCredentials = Security(security)):
        token = credentials.credentials  # Extract Bearer token
        return verify_and_check_scope(token, required_scope)

    return validate_token
