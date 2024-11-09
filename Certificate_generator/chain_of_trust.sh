#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <p7s_file> <device_cert>"
    exit 1
fi

P7S_FILE=$1
DEVICE_CERT=$2

openssl verify "$P7S_FILE" "$DEVICE_CERT"

# Clean up
#rm extracted_certs.pem