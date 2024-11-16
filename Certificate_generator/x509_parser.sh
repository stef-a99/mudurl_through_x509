#!/bin/bash

CERT_FILE="generated/iot_dev_cert.pem"
CA_FILE="generated/ca_cert.pem"
CA_FILE_SHORT="ca_cert.pem"
MUDFS_FILE="generated/mudfs_cert.pem"

# Check if the file exists
if [ ! -f "/usr/local/share/ca-certificates/$CA_FILE_SHORT" ]; then
    sudo cp "$CA_FILE" /usr/local/share/ca-certificates/
    sudo cp "$CA_FILE" /etc/ssl/certs/
    sudo update-ca-certificates
else
    echo "The CA certificate is already copied."
fi

#Check if the certificate was signed by a trusted CA
if ! openssl verify -CAfile "$CA_FILE" "$CERT_FILE" > /dev/null 2>&1; then
    echo "The certificate is not signed by a trusted CA."
    # Print the issuer of the CA file
    CA_SUBJECT=$(openssl x509 -in "$CA_FILE" -noout -subject | sed 's/subject= //')
    echo "The subject of the CA file is:"
    echo "$CA_SUBJECT"
    echo "The issuer of the CA file is:"
    CA_ISSUER=$(openssl x509 -in "$CA_FILE" -noout -issuer | sed 's/issuer= //')
    echo "$CA_ISSUER"
    # Print the issuer of the certificate file
    CERT_ISSUER=$(openssl x509 -in "$CERT_FILE" -noout -issuer | sed 's/issuer= //')
    echo "The issuer of the certificate file is:"
    echo "$CERT_ISSUER"
    exit 1
else
    echo "The certificate is signed by a trusted CA."
    # Extract and print the value of the 1.3.6.1.5.5.7.1.25 OID extension
    EXT_VALUE=$(openssl x509 -in "$CERT_FILE" -noout -text | grep -A1 "1.3.6.1.5.5.7.1.25" | tail -n1 | awk '{$1=$1;print}')

    if [ -z "$EXT_VALUE" ]; then
        echo "The certificate does not contain the id-pe-mud-url extension."
    else
        echo "The value of the id-pe-mud-url extension is:"
        echo "$EXT_VALUE"
    fi
    # Extract and print the value of the mudsigner extension
    MUDSIGNER_VALUE=$(openssl x509 -in "$CERT_FILE" -noout -text | grep -A1 "1.3.6.1.5.5.7.1.30" | tail -n1 | awk '{$1=$1;print}')

    if [ -z "$MUDSIGNER_VALUE" ]; then
        echo "The certificate does not contain the mudsigner extension."
    else
        echo "The value of the mudsigner extension is:"
        echo "$MUDSIGNER_VALUE"

        # Check if the mudsigner extension value matches the mudfs certificate
        #MUDFS_VALUE=$(openssl x509 -in "$MUDFS_FILE" -noout -text | grep -A1 "Subject: CN = " | tail -n1 | awk '{$1=$1;print}')
        MUDFS_VALUE=$(openssl x509 -in "$MUDFS_FILE" -noout -subject | sed -n 's/^.*CN = //p' | sed 's/,.*//')
        if [ "$MUDSIGNER_VALUE" == "$MUDFS_VALUE" ]; then
            echo "The mudsigner extension value matches the mudfs certificate."
        else
            echo "The mudsigner extension value does not match the mudfs certificate."
        fi
        echo "Mudfs subject: $MUDFS_VALUE"
        echo "Mudsigner value: $MUDSIGNER_VALUE"
    fi
fi

# Prima controlla la validità e poi fai il parsing.