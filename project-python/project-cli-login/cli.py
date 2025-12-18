#!/usr/bin/env python3

import argparse
import msal
import keyring
import requests
import sys
import os
from dotenv import load_dotenv

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLI_CLIENT_ID = os.getenv("CLI_CLIENT_ID")
API_CLIENT_ID = os.getenv("API_CLIENT_ID")
SCOPE_NAME = os.getenv("SCOPE_NAME")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

SCOPE = [f"api://{API_CLIENT_ID}/{SCOPE_NAME}"]

KEYRING_SERVICE = "securecli"
KEYRING_KEY = "access_token"

API_URL = os.getenv("API_URL", "http://localhost:5000")


def save_token(token):
    keyring.set_password(KEYRING_SERVICE, KEYRING_KEY, token)


def load_token():
    return keyring.get_password(KEYRING_SERVICE, KEYRING_KEY)


def delete_token():
    try:
        keyring.delete_password(KEYRING_SERVICE, KEYRING_KEY)
    except:
        pass



def login():
    app = msal.PublicClientApplication(
        CLI_CLIENT_ID,
        authority=AUTHORITY,
    )

    flow = app.initiate_device_flow(scopes=SCOPE, claims_challenge=None)
    if "user_code" not in flow:
        sys.exit("Failed to initiate device flow")

    print(flow["message"])

    result = app.acquire_token_by_device_flow(flow)

    if "access_token" not in result:
        print("Authentication failed:")
        print(result.get("error_description"))
        sys.exit(1)

    save_token(result["access_token"])
    print("Login successful")


def logout():
    delete_token()
    print("Logged out")


def call_api(endpoint):
    token = load_token()

    if not token:
        sys.exit("Not logged in. Run: cli.py login")

    resp = requests.get(
        f"{API_URL}{endpoint}",
        headers={"Authorization": f"Bearer {token}"}
    )

    print(resp.json())


def main():
    parser = argparse.ArgumentParser(description="Secure Azure CLI")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("login")
    sub.add_parser("logout")

    data_cmd = sub.add_parser("data")
    data_cmd.add_argument("--path", default="/api/data")

    args = parser.parse_args()

    match args.command:
        case "login":
            login()
        case "logout":
            logout()
        case "data":
            call_api(args.path)
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
