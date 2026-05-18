"""
Authentication Utilities
========================
Secure password hashing and token generation using standard library tools
"""

import os
import time
import json
import hmac
import hashlib
import base64
import secrets
from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import User

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-algiers-key-12345-never-share-this")
EXPIRATION_SECONDS = 86400  # 24 hours


def hash_password(password: str) -> str:
    """Hash a password securely using PBKDF2"""
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return f"{salt}:{key.hex()}"


def verify_password(password: str, hashed_password: str, db: Session = None) -> bool:
    """Verify a password against its PBKDF2 hash or native pgcrypto crypt"""
    try:
        if ":" in hashed_password:
            salt, key_hex = hashed_password.split(":")
            new_key = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt.encode('utf-8'),
                100000
            )
            if secrets.compare_digest(new_key.hex(), key_hex):
                return True
                
        # Fallback to PostgreSQL native pgcrypto verification
        if db and hashed_password.startswith("$"):
            from sqlalchemy import text
            query = text("SELECT :hash = crypt(:password, :hash)")
            res = db.execute(query, {"password": password, "hash": hashed_password}).scalar()
            return bool(res)
            
        return False
    except Exception:
        return False


def create_access_token(data: dict, expires_in: int = EXPIRATION_SECONDS) -> str:
    """Generate a signature-verified lightweight session token"""
    payload = data.copy()
    payload["exp"] = time.time() + expires_in
    
    # Base64 encode the payload dictionary
    payload_str = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    
    # Calculate signature
    signature = hmac.new(SECRET_KEY.encode(), payload_str.encode(), hashlib.sha256).digest()
    sig_str = base64.urlsafe_b64encode(signature).decode().rstrip("=")
    
    return f"{payload_str}.{sig_str}"


def decode_access_token(token: str) -> dict:
    """Decode and verify a session token"""
    try:
        parts = token.split(".")
        if len(parts) != 2:
            return None
        payload_str, sig_str = parts[0], parts[1]
        
        # Verify signature
        expected_sig = hmac.new(SECRET_KEY.encode(), payload_str.encode(), hashlib.sha256).digest()
        expected_sig_str = base64.urlsafe_b64encode(expected_sig).decode().rstrip("=")
        
        if not hmac.compare_digest(sig_str, expected_sig_str):
            return None
        
        # Add padding back if necessary
        padding = 4 - (len(payload_str) % 4)
        if padding < 4:
            payload_str += "=" * padding
            
        payload = json.loads(base64.urlsafe_b64decode(payload_str.encode()).decode())
        
        # Check expiration
        if payload.get("exp", 0) < time.time():
            return None
            
        return payload
    except Exception:
        return None


def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)) -> User:
    """Dependency to retrieve the currently authenticated user from headers"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authentication credentials not provided")
    
    try:
        # Expecting 'Bearer <token>' format
        token_type, token = authorization.split(" ")
        if token_type.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid token type")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
        
    payload = decode_access_token(token)
    if not payload or "email" not in payload:
        raise HTTPException(status_code=401, detail="Session expired or invalid token")
        
    user = db.query(User).filter(User.email == payload["email"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="User account not found")
        
    return user
