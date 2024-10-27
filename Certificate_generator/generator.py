from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
import datetime

# Generate a CA private key
ca_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

# Generate a CA self-signed certificate
ca_subject = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"IT"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Italy"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"Bologna"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"UniBo"),
    x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, u"DISI"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"ca.example.com"),
    x509.NameAttribute(NameOID.EMAIL_ADDRESS, u"ca@example.email.com")
])

ca_certificate = x509.CertificateBuilder().subject_name(ca_subject).issuer_name(
    ca_subject).public_key(ca_private_key.public_key()).serial_number(
    x509.random_serial_number()).not_valid_before(
    datetime.datetime.now()).not_valid_after(
    datetime.datetime.now() + datetime.timedelta(days=365)).add_extension(
    x509.BasicConstraints(ca=True, path_length=None), critical=True).sign(
    ca_private_key, hashes.SHA256())

# Generate a private key for the certificate
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

# Create a certificate signing request (CSR)
csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"IT"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Italy"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"Bologna"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"UniBo"),
    x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, u"DISI"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"manifacturer.example.com"),
    x509.NameAttribute(NameOID.EMAIL_ADDRESS, u"manufacturerOne@unibo.it")
])).add_extension(
    x509.UnrecognizedExtension(
        oid=x509.ObjectIdentifier("1.3.6.1.5.5.7.1.25"),
        value=b"https://mudfs.example.com/pi4.json"),
        critical=False
        ).add_extension(
            x509.UnrecognizedExtension(
                oid=x509.ObjectIdentifier("1.3.6.1.5.5.7.1.30"),
                value=b"C = IT, ST = Italy, L = Bologna, O = UniBo, OU = DISI, CN = mudfs.example.com, emailAddress = manufacturerOne@unibo.it"
            ),
        critical=False).sign(private_key, hashes.SHA256())

# Generate a certificate signed by the CA
certificate = x509.CertificateBuilder().subject_name(csr.subject).issuer_name(
    ca_certificate.subject).public_key(csr.public_key()).serial_number(
    x509.random_serial_number()).not_valid_before(
    datetime.datetime.now()).not_valid_after(
    datetime.datetime.now() + datetime.timedelta(days=365)).add_extension(
    x509.UnrecognizedExtension(
        oid=x509.ObjectIdentifier("1.3.6.1.5.5.7.1.25"),
        value=b"https://mudfs.example.com/pi4.json"
    ),
    critical=False).add_extension(
    x509.UnrecognizedExtension(
        oid=x509.ObjectIdentifier("1.3.6.1.5.5.7.1.30"),
        value=b"C = IT, ST = Italy, L = Bolo, O = UniBo, OU = DISI, CN = mudfs.example.com, emailAddress = manufacturerOne@unibo.it",
    ),
    critical=False).sign(ca_private_key, hashes.SHA256())

# Generate a private key for the certificate
man_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

# Generates csr for the manufacturer mud file server
csr_mudfs = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"IT"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Italy"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"Bologna"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"UniBo"),
    x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, u"DISI"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"mudfs.example.com"),
    x509.NameAttribute(NameOID.EMAIL_ADDRESS, u"mudfs@example.email.com")
])).sign(man_private_key, hashes.SHA256())

# Generate a certificate signed by the CA
man_certificate = x509.CertificateBuilder().subject_name(csr.subject).issuer_name(
    ca_certificate.subject).public_key(csr.public_key()).serial_number(
    x509.random_serial_number()).not_valid_before(
    datetime.datetime.now()).not_valid_after(
    datetime.datetime.now() + datetime.timedelta(days=365)).sign(ca_private_key, hashes.SHA256())

# Save the manufacturer mudfs private key and certificate to files
with open("generated/mudfs_key.key", "wb") as f:
    f.write(man_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Save the manufacturer mudfs certificate to files
with open("generated/mudfs_cert.pem", "wb") as f:
    f.write(man_certificate.public_bytes(serialization.Encoding.PEM))

# Save the CA private key and certificate to files
with open("generated/manufacturer_ca_key.key", "wb") as f:
    f.write(ca_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

with open("generated/manufacturer_ca_cert.pem", "wb") as f:
    f.write(ca_certificate.public_bytes(serialization.Encoding.PEM))

# Save the private key and certificate to files
with open("generated/iot_dev_key.key", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

with open("generated/iot_dev_cert.pem", "wb") as f:
    f.write(certificate.public_bytes(serialization.Encoding.PEM))
