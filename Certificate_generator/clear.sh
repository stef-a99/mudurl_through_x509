#!/bin/bash

rm generated/*
if [ -f "/etc/ssl/certs/ca_cert.pem" ]; then
    rm /etc/ssl/certs/ca_cert.pem
fi
if [ -f "/usr/local/share/ca-certificates/ca_cert.pem" ]; then
    rm /usr/local/share/ca-certificates/ca_cert.pem
fi

#echo "
#[ custom_ext ]
#1.3.6.1.5.5.7.1.25 = critical,ASN1:IA5String:id-pe-mud-url
#1.3.6.1.5.5.7.1.26 = ASN1:UTF8String:id-pe-mudsigner
#" >> /etc/ssl/openssl.cnf
