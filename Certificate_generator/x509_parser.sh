#!/bin/bash

# Check if the user provided a certificate file
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <certificate-file>"
    exit 1
fi

CERT_FILE=$1

# Check if the file exists
if [ ! -f "$CERT_FILE" ]; then
    echo "File not found: $CERT_FILE"
    exit 1
fi

# Extract the value of the extension called "id-pe-mud-url"
EXTENSION_VALUE=$(openssl x509 -in "$CERT_FILE" -noout -text | grep -A1 "1.3.6.1.5.5.7.1.25" | tail -n1 | awk '{$1=$1;print}')

if [ -z "$EXTENSION_VALUE" ]; then
    echo "Extension id-pe-mud-url not found in the certificate."
else
    echo "id-pe-mud-url: $EXTENSION_VALUE"
fi

# Extract the value of the extension called "id-pe-mudsigner"
MUDSIGNER_VALUE=$(openssl x509 -in "$CERT_FILE" -noout -text | grep -A1 "1.3.6.1.5.5.7.1.30" | tail -n1 | awk '{$1=$1;print}')

if [ -z "$MUDSIGNER_VALUE" ]; then
    echo "Extension id-pe-mudsigner not found in the certificate."
else
    echo "id-pe-mudsigner: $MUDSIGNER_VALUE"
fi

