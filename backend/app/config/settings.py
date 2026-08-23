import os

from dotenv import load_dotenv

load_dotenv()

# SUPPLYMIND_JWT_SECRET is read from .env not .env.example file, so that it can be set in the deployment environment.
SECRET_KEY = os.getenv(
    "SUPPLYMIND_JWT_SECRET",
)

if not SECRET_KEY:
    raise RuntimeError("SUPPLYMIND_JWT_SECRET is not configured.")
