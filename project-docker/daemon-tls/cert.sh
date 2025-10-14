#!/usr/bin/env bash

set -euo pipefail
set -x  # Optional: Debug mode

IP="10.192.36.102"
CERT_DIR=~/docker-certs
DOCKER_CERT_DIR="/etc/docker/certs"

mkdir -p "$CERT_DIR"
cd "$CERT_DIR"

# Step 1: Create CA key and cert
openssl genrsa -out ca-key.pem 4096
chmod 400 ca-key.pem

openssl req -new -x509 -days 3650 -key ca-key.pem -sha256 -out ca.pem \
  -subj "/CN=Docker Root CA"

# Step 2: Create server key and CSR
openssl genrsa -out server-key.pem 4096
chmod 400 server-key.pem

openssl req -new -key server-key.pem -out server.csr \
  -subj "/CN=${IP}"

# Step 3: Create SAN extension config
cat > extfile.cnf <<EOF
subjectAltName = IP:${IP},IP:127.0.0.1,DNS:localhost
extendedKeyUsage = serverAuth
basicConstraints = CA:FALSE
EOF

# Step 4: Sign the server cert with the CA
openssl x509 -req -days 365 -sha256 -in server.csr \
  -CA ca.pem -CAkey ca-key.pem -CAcreateserial \
  -out server-cert.pem -extfile extfile.cnf

chmod 444 server-cert.pem

# Step 5: (Optional) Create client certs for mutual TLS
openssl genrsa -out key.pem 4096
chmod 400 key.pem

openssl req -new -key key.pem -out client.csr \
  -subj "/CN=client"

cat > client-ext.cnf <<EOF
extendedKeyUsage = clientAuth
basicConstraints = CA:FALSE
EOF

openssl x509 -req -days 365 -sha256 -in client.csr \
  -CA ca.pem -CAkey ca-key.pem -CAcreateserial \
  -out cert.pem -extfile client-ext.cnf

chmod 444 cert.pem

# Step 6: Move server certs to Docker config directory
sudo mkdir -p "$DOCKER_CERT_DIR"
sudo cp ca.pem server-cert.pem server-key.pem "$DOCKER_CERT_DIR"

echo "✅ Docker TLS certs created and installed to $DOCKER_CERT_DIR"


# export DOCKER_HOST="tcp://10.192.36.106:2376"
# export DOCKER_TLS_VERIFY=1
# export DOCKER_CERT_PATH="~/docker-certs"
