from pathlib import Path

from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.hazmat.primitives import serialization

from make_certs.exceptions import MakeCertKeyError, MakeCertFileError

KeyType = rsa.RSAPrivateKey | ec.EllipticCurvePrivateKey


class PrivateKey:
    def __init__(self, key_type='ecc') -> None:
        self._key: KeyType
        if key_type == 'ecc':
            self._key = ec.generate_private_key(ec.SECP256R1())
            print('Elliptic curve private key has been created')
        elif key_type == 'rsa':
            key_size = 2048
            self._key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
            print('RSA private key has been created')
        else:
            raise MakeCertKeyError(f'Unknown key_type == {key_type}')

    @classmethod
    def from_file(cls, load_from: Path, password: None | str = None) -> 'PrivateKey':
        obj = PrivateKey.__new__(PrivateKey)
        b_pass = password.encode() if password is not None else None
        with open(load_from, 'rb') as file:
            key = serialization.load_pem_private_key(file.read(), b_pass)
        if not isinstance(key, (rsa.RSAPrivateKey, ec.EllipticCurvePrivateKey)):
            raise MakeCertKeyError(f'Unsupported key type {type(key)}')
        obj._key = key
        return obj

    @property
    def value(self) -> KeyType:
        return self._key

    def save(self, save_to: Path, password: None | str = None) -> None:
        encryption_algorithm: serialization.KeySerializationEncryption = serialization.NoEncryption()

        if password:
            encryption_algorithm = serialization.BestAvailableEncryption(password.encode())

        key_data = self._key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=encryption_algorithm,
        )
        if save_to.exists():
            raise MakeCertFileError(f'Keyfile {save_to} already exists')
        save_to.parent.mkdir(parents=True, exist_ok=True)
        with open(save_to, 'wb') as file:
            file.write(key_data)
