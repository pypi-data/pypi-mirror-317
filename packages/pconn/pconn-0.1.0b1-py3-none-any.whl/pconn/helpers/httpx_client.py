"""Utility to convert pfx certificate to pem format."""

from datetime import UTC, datetime, timedelta
import os
import ssl

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
import httpx

from pconn.core import PConn

DATA_ASYNC_CLIENT = "httpx_async_client"
DATA_ASYNC_CLIENT_NOVERIFY = "httpx_async_client_noverify"
CERT_PATH = ".cert/certificate.pem"
PRIV_KEY_PATH = ".cert/priv_key.pem"
SSL_CIPHER_LISTS = (
    "ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:"
    "ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:"
    "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:"
    "ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:"
    "ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256"
)


def server_context_modern() -> ssl.SSLContext:
    """Return an SSL context following the Mozilla recommendations.

    TLS configuration follows the best-practice guidelines specified here:
    https://wiki.mozilla.org/Security/Server_Side_TLS
    Modern guidelines are followed.
    """
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    context.options |= ssl.OP_CIPHER_SERVER_PREFERENCE
    if hasattr(ssl, "OP_NO_COMPRESSION"):
        context.options |= ssl.OP_NO_COMPRESSION

    context.set_ciphers(SSL_CIPHER_LISTS)

    return context


def create_self_signed_cert(pconn: PConn) -> str:
    """Creates a self-signed certificate and return its thumbprint."""
    if os.path.exists(pconn.config.path(CERT_PATH)) and os.path.exists(
        pconn.config.path(PRIV_KEY_PATH)
    ):
        return get_cert_thumbprint(pconn)

    os.makedirs(pconn.config.path(".cert"), exist_ok=True)

    host = "platform-connectors"

    # Generate a private key
    priv_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    # Build the subject and issuer information
    subject = issuer = x509.Name(
        [
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Platform Connectors"),
            x509.NameAttribute(NameOID.COMMON_NAME, host),
        ]
    )

    # Generate the certificate
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(priv_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now(UTC))
        .not_valid_after(datetime.now(UTC) + timedelta(days=365))
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName(host)]),
            critical=False,
        )
        .sign(priv_key, hashes.SHA256())
    )

    with open(pconn.config.path(CERT_PATH), "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    with open(pconn.config.path(PRIV_KEY_PATH), "wb") as f:
        f.write(
            priv_key.private_bytes(
                serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
    return get_cert_thumbprint(pconn)


def create_async_httpx_client(pconn: PConn, verify_ssl: bool) -> httpx.AsyncClient:
    """Return a httpx client."""
    if verify_ssl is False:
        return httpx.AsyncClient(verify=False)
    context = server_context_modern()
    if not os.path.exists(pconn.config.path(CERT_PATH)) or not os.path.exists(
        pconn.config.path(PRIV_KEY_PATH)
    ):
        create_self_signed_cert(pconn)

    context.load_cert_chain(
        pconn.config.path(CERT_PATH), pconn.config.path(PRIV_KEY_PATH)
    )
    return httpx.AsyncClient(verify=context)


def get_cert_thumbprint(pconn: PConn) -> str:
    """Return the thumbprint of the certificate."""
    with open(pconn.config.path(CERT_PATH), "rb") as cert_file:
        cert = x509.load_pem_x509_certificate(cert_file.read())
    fingerprint = cert.fingerprint(hashes.SHA1()).hex()
    return fingerprint


def get_httpx_client(pconn: PConn, verify_ssl: bool = False) -> httpx.AsyncClient:
    """Return an httpx client based on ssl."""
    key = DATA_ASYNC_CLIENT if verify_ssl else DATA_ASYNC_CLIENT_NOVERIFY

    if (client := pconn.data.get(key)) is None:
        client = pconn.data[key] = create_async_httpx_client(pconn, verify_ssl)

    return client
