from codecs import encode
from textwrap import dedent

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey


class WireguardKeypair:
    def __init__(self, private: str, public: str) -> None:
        self.private: str = private
        self.public: str = public

    def __repr__(self) -> str:
        return f"Keypair(private={self.private}, public={self.public})"


def crypt_rand_char() -> str:
    return "crypt_rand_char: Not yet implemented"


def crypt_rand_hex() -> str:
    return "crypt_rand_hex: Not yet implemented"


def crypt_rand_pw() -> str:
    return "crypt_rand_pw: Not yet implemented"


def crypt_simple_enc() -> str:
    return "crypt_simple_enc: Not yet implemented"


def crypt_simple_dec() -> str:
    return "crypt_simple_dec: Not yet implemented"


def crypt_wireguard(script: bool) -> str:
    encoding: serialization.Encoding = serialization.Encoding.Raw
    priv_format: serialization.PrivateFormat = serialization.PrivateFormat.Raw
    pub_format: serialization.PublicFormat = serialization.PublicFormat.Raw
    private_key: X25519PrivateKey = X25519PrivateKey.generate()
    private_bytes: bytes = private_key.private_bytes(
        encoding=encoding,
        format=priv_format,
        encryption_algorithm=serialization.NoEncryption(),
    )
    private_text: str = encode(private_bytes, "base64").decode("utf8").strip()
    public_bytes: bytes = private_key.public_key().public_bytes(
        encoding=encoding, format=pub_format
    )
    public_text: str = encode(public_bytes, "base64").decode("utf8").strip()
    keypair = WireguardKeypair(private_text, public_text)
    if script:
        return f"{keypair.private} {keypair.public}"
    return dedent(
        f"""
        Private key : {keypair.private}
        Public key  : {keypair.public}
        """
    )
