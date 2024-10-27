#!/bin/bash

# Check if the user provided a certificate file
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <certificate-file>"
    exit 1
fi


CERT_FILE=$1
CA_FILE="generated/manufacturer_ca_cert.pem"
MUDFS_FILE="generated/mudfs_cert.pem"

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

    # Check if the certificate was signed by the CA with common name "ca.example.com"
    IOT_ISSUER=$(openssl x509 -in "$CERT_FILE" -noout -text -issuer |  grep -A1 "Issuer" | head -n1 | cut -d ':' -f2- | xargs)
    CA_SUBJECT=$(openssl x509 -in "$CA_FILE" -noout -text -subject |  grep -A1 "Subject" | head -n1 | cut -d ':' -f2- | xargs)

    if [ "$IOT_ISSUER" != "$CA_SUBJECT" ]; then
        echo "Certificate was not signed by the CA with common name 'ca.example.com'."
        exit 1
    else
        echo "Certificate was signed by the CA with common name 'ca.example.com'."
        # Checks if the MUD signer was the MUDFS
        MUDFS_ISSUER=$(openssl x509 -in "$MUDFS_FILE" -noout -text -issuer |  grep -A1 "Issuer" | head -n1 | cut -d ':' -f2- | xargs)
        if [ "$MUDFS_ISSUER" != "$CA_SUBJECT" ]; then
            echo "Unable to find the MUD Signer for this certificate."
            exit 1
        else
            echo "MUD Signer found."
            # Checks if the MUD signer was the MUDFS
            MUDFS_ISSUER=$(openssl x509 -in "$MUDFS_FILE" -noout -text -issuer |  grep -A1 "Issuer" | head -n1 | cut -d ':' -f2- | xargs)
        fi
    fi

  
fi


