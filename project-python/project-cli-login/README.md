# Azure AD Secured CLI + API (Device Code Flow)

This repository demonstrates how to build a **secure CLI application** and a **Flask API** using **Microsoft Entra ID (Azure AD)** with:

- OAuth 2.0 Device Code Flow
- Public client (CLI) + Confidential resource (API)
- Scope-based authorization
- App Roles (RBAC)
- JWT validation using Azure JWKS
- Refresh tokens (silent reauthentication)

This is an **enterprise-grade reference architecture** aligned with Microsoft best practices.

---

## Architecture Overview

```
User
 └── CLI (Public Client)
       └── Device Code Login
             └── Microsoft Entra ID
                   └── Issues Access Token (JWT)
                         └── API (Resource Server)
                               └── Validates Token (iss, aud, scp, roles)
```

---

## Prerequisites

- Azure account with **Microsoft Entra ID**
- Admin access (required for consent & app roles)
- Python 3.9+
- pip, virtualenv

---

## App Registrations Required

You **must create two app registrations**.

| App | Type | Purpose |
|-----|------|---------|
| CLI App | Public Client | User login (Device Code Flow) |
| API App | Resource / API | Token validation & authorization |

---

## STEP 1 — Create API App Registration

### Create App
Azure Portal → Entra ID → App registrations → New registration

- Name: my-secure-api
- Supported account types: Single tenant
- Redirect URI: leave empty

### Expose the API

- Application ID URI:
  ```
  api://<API_CLIENT_ID>
  ```

- Scope:
  ```
  access_as_user (Admins only)
  ```

---

## STEP 2 — Create CLI App Registration

- Name: my-secure-cli
- Enable: Allow public client flows
- API Permissions:
  ```
  My APIs → my-secure-api → access_as_user
  ```
- Grant admin consent

---

## Enable V2 Tokens (CRITICAL)

For **both apps**, in Manifest:

```json
"accessTokenAcceptedVersion": 2
```

---

## App Roles (Optional)

Define roles in API app manifest:

```json
"appRoles": [
  {
    "allowedMemberTypes": ["User"],
    "displayName": "UserAccess",
    "value": "UserAccess",
    "id": "<GUID>",
    "isEnabled": true
  },
  {
    "allowedMemberTypes": ["User"],
    "displayName": "AdminAccess",
    "value": "AdminAccess",
    "id": "<GUID>",
    "isEnabled": true
  }
]
```

Assign roles under **Enterprise Applications → Users and Groups**.

---

## Environment Variables

```ini
TENANT_ID=<tenant-guid>
CLI_CLIENT_ID=<cli-app-id>
API_CLIENT_ID=<api-app-id>
SCOPE_NAME=access_as_user
API_URL=http://localhost:5000
```

---

## Token Expectations

| Claim | Expected |
|------|---------|
| iss | https://login.microsoftonline.com/<TENANT_ID>/v2.0 |
| aud | <API_CLIENT_ID> |
| scp | access_as_user |
| ver | 2.0 |
| roles | UserAccess / AdminAccess |

---

## Common Issues

### Invalid issuer
- Cause: V1 token (sts.windows.net)
- Fix: accessTokenAcceptedVersion = 2, re-login

### Audience mismatch
- Fix: API audience must be API_CLIENT_ID (GUID)

### Need admin approval
- Fix: Grant admin consent in CLI app

### JWKS 404
- Use:
  ```
  https://login.microsoftonline.com/<TENANT_ID>/discovery/v2.0/keys
  ```

---

## Debugging Tokens

```bash
python3 - <<EOF
import keyring, jwt
t = keyring.get_password("securecli", "access_token")
print(jwt.decode(t, options={"verify_signature": False}))
EOF
```

---

## Security Notes

- No secrets in CLI
- No passwords transmitted
- Tokens scoped to API
- Tenant isolated
- Zero Trust compliant

---

## Final Notes

This setup mirrors how Azure CLI and Microsoft Teams authenticate users.
