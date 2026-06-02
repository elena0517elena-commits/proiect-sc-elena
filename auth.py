from datetime import datetime, timedelta
from jose import jwt
import bcrypt
import os
from dotenv import load_dotenv
import hashlib

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
ALGORITHM = os.environ.get("ALGORITHM", "HS256")


def normalizeaza(parola):
    return hashlib.sha256(parola.encode()).hexdigest()

def hash_parola(parola):
    pwd = normalizeaza(parola).encode()
    return bcrypt.hashpw(pwd, bcrypt.gensalt()).decode()

def verifica_parola(parola, hash):
    pwd = normalizeaza(parola).encode()
    return bcrypt.checkpw(pwd, hash.encode())

def creeaza_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(hours=2)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)