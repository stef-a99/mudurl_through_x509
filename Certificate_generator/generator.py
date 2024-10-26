from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import ExtensionOID
import datetime
import subprocess



# Generate a private key
private_key = rsa.generate_private_key(public_exponent=65537,key_size=2048)

# Create a certificate signing request (CSR)
csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
    x509.NameAttribute(x509.NameOID.COMMON_NAME, u"ca.example.com")
])).add_extension(
    x509.UnrecognizedExtension(oid=x509.ObjectIdentifier("1.3.6.1.5.5.7.1.25"),value=b"https://example.com/mud-url"),
    critical=False).sign(private_key, hashes.SHA256())

# Generate a self-signed certificate
certificate = x509.CertificateBuilder().subject_name(x509.Name([
    x509.NameAttribute(x509.NameOID.COMMON_NAME, u"ca.example.com")
])).issuer_name(x509.Name([
    x509.NameAttribute(x509.NameOID.COMMON_NAME, u"ca.example.com")
])).public_key(csr.public_key()).serial_number(x509.random_serial_number()).not_valid_before(
    datetime.datetime.now()).not_valid_after(
        datetime.datetime.now() + datetime.timedelta(days=365)).add_extension(
    x509.UnrecognizedExtension(
        oid=x509.ObjectIdentifier("1.3.6.1.5.5.7.1.25"),
        value=b"https://example.com/mud-url"
    ),
    critical=False).add_extension(
        x509.UnrecognizedExtension(
            oid=x509.ObjectIdentifier("1.3.6.1.5.5.7.1.30"),
            value=b"C = IT, ST = Italy, L = Bolo, O = UniBo, OU = DISI, CN = manuf.unibo.it, emailAddress = manufacturer.one@unibo.it"
        ),
    critical=False).sign(private_key, hashes.SHA256())

# Save the private key and certificate to files
with open("private_key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

with open("certificate.pem", "wb") as f:
    f.write(certificate.public_bytes(serialization.Encoding.PEM))
