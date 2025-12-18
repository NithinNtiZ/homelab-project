#!/usr/bin/env python3

from flask import Flask, request, jsonify
import jwt
import requests
import os
from dotenv import load_dotenv
from functools import wraps
from jwt.algorithms import RSAAlgorithm

load_dotenv()

app = Flask(__name__)

TENANT_ID = os.getenv("TENANT_ID")
API_CLIENT_ID = os.getenv("API_CLIENT_ID")
SCOPE_NAME = os.getenv("SCOPE_NAME")

ISSUER = f"https://login.microsoftonline.com/{TENANT_ID}/v2.0"
AUDIENCE = f"{API_CLIENT_ID}"

JWKS_URL = f"https://login.microsoftonline.com/{TENANT_ID}/discovery/v2.0/keys"
JWKS = requests.get(JWKS_URL).json()


def validate_token(token):
    header = jwt.get_unverified_header(token)
    kid = header.get("kid")


    signing_key = None
    for key in JWKS["keys"]:
        if key["kid"] == kid:
            signing_key = RSAAlgorithm.from_jwk(key)
            break

    if signing_key is None:
        raise Exception("Signing key not found in Azure JWKS")

    payload = jwt.decode(
        token,
        signing_key,
        algorithms=["RS256"],
        audience=AUDIENCE,
        issuer=ISSUER
    )
    print("Token payload:", payload)
    scopes = payload.get("scp", "").split()
    if SCOPE_NAME not in scopes:
        raise Exception("Insufficient scope")
    return payload


def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")

        if not auth.startswith("Bearer "):
            return jsonify({"error": "missing token"}), 401

        token = auth.split()[1]


        try:
            request.user = validate_token(token)
        except Exception as e:
            return jsonify({"error during validation": str(e)}), 401

        return f(*args, **kwargs)

    return wrapper


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/data")
@auth_required
def data():
    return jsonify({
        "message": "Secure data delivered",
        "user": request.user.get("preferred_username"),
        "tenant_id": request.user.get("tid"),
        "scope": request.user.get("scp"),
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
 