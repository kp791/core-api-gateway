#!/bin/bash

# Set names and optional subject for cert
CERT_FILE="cert.pem"
KEY_FILE="key.pem"
DAYS_VALID=365
SUBJECT="/C=US/ST=Test/L=Local/O=Dev/OU=Example/CN=localhost"

echo "Generating self-signed certificate for local development..."

mkdir -p certs

openssl req -x509 -nodes -days $DAYS_VALID \
    -newkey rsa:2048 \
    -keyout "./certs/$KEY_FILE" \
    -out "./certs/$CERT_FILE" \
    -subj "$SUBJECT"

echo "Done."
echo "Generated $CERT_FILE and $KEY_FILE to ./certs"

