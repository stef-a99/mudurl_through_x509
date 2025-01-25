import argparse
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
import datetime

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Generate a private key and CSR.')
parser.add_argument('filename', type=str, help='The filename for key and csr.')
args = parser.parse_args()

# Generate private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Save the private key to a file
key_filename_with_suffix = args.filename + "_key.pem"
with open(key_filename_with_suffix, "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Generate a CSR
csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"IT"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Italy"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"Bologna"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Unibo"),
    x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, u"DISI"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"iotDev.example.com"),
    x509.NameAttribute(NameOID.EMAIL_ADDRESS, u"mudIoTDev@example.com")
])).add_extension(
    x509.UnrecognizedExtension(
        oid=x509.ObjectIdentifier("1.3.6.1.5.5.7.1.25"),
        value=b"https://mudfs.example.com/pi4.json"),
        critical=False
        ).add_extension(
            x509.UnrecognizedExtension(
                oid=x509.ObjectIdentifier("1.3.6.1.5.5.7.1.30"),
                value=b"mudfs.example.com"
            ),
        critical=False).sign(private_key, hashes.SHA256())

# Save the CSR to a file
csr_filename_with_suffix = args.filename + ".csr"
with open(csr_filename_with_suffix, "wb") as f:
    f.write(csr.public_bytes(serialization.Encoding.PEM))