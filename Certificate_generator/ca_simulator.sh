#!/bin/bash

# Function to prompt user for input
prompt() {
    read -p "$1: " input
    echo $input
}

# Prompt user for certificate details
country=$(prompt "Enter Country Name (2 letter code)")
state=$(prompt "Enter State or Province Name (full name)")
locality=$(prompt "Enter Locality Name (eg, city)")
organization=$(prompt "Enter Organization Name (eg, company)")
organizational_unit=$(prompt "Enter Organizational Unit Name (eg, section)")
common_name=$(prompt "Enter Common Name (e.g. server FQDN or YOUR name)")
email=$(prompt "Enter Email Address")

# Create a configuration file for the certificate
cat > ca_cert.conf <<EOL
[ req ]
default_bits       = 2048
default_md         = sha256
default_keyfile    = ca_key.pem
prompt             = no
encrypt_key        = no
distinguished_name = req_distinguished_name

[ req_distinguished_name ]
C  = $country
ST = $state
L  = $locality
O  = $organization
OU = $organizational_unit
CN = $common_name
emailAddress = $email
EOL

# Generate the CA private key
openssl genpkey -algorithm RSA -out ca_key.pem -pkeyopt rsa_keygen_bits:2048

# Generate the CA certificate
openssl req -new -x509 -key ca_key.pem -out ca_cert.pem -days 365 -config ca_cert.conf

# Print the subject field of the generated certificate
openssl x509 -in ca_cert.pem -noout -subject