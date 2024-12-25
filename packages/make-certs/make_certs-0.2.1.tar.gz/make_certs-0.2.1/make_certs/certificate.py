import ipaddress

from datetime import timedelta
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization

from make_certs.exceptions import MakeCertCertificateError, MakeCertFileError
from make_certs.private_key import PrivateKey
from make_certs.utils import RFC5280_UNDEFINED_NOT_AFTER, utcnow

DEFAULT_CA_KEY_USAGE = {
    'digital_signature': True,
    'content_commitment': False,
    'key_encipherment': False,
    'data_encipherment': False,
    'key_agreement': False,
    'key_cert_sign': True,
    'crl_sign': True,
    'encipher_only': False,
    'decipher_only': False,
}
DEFAULT_END_ENTITY_KEY_USAGE = DEFAULT_CA_KEY_USAGE | {
    'key_encipherment': True,
    'key_cert_sign': False,
}


def load_from_file(load_from: Path | str) -> x509.Certificate:
    with open(load_from, 'rb') as file:
        return x509.load_pem_x509_certificate(file.read())


class Certificate:
    """
    load_from_file() | (create() -> sing()) -> add_extensions_*() -> save()
    """
    def __init__(self, key: PrivateKey) -> None:
        self._key = key
        self._cert: None | x509.Certificate = None
        self._signing_key: None | PrivateKey = None
        self._builder = x509.CertificateBuilder()

    def load_from_file(self, load_from: Path) -> None:
        self._cert = load_from_file(load_from)

    @property
    def value(self) -> x509.Certificate:
        if not self._cert:
            raise MakeCertCertificateError('Trying to get not yet built certificate')
        return self._cert

    @property
    def key(self) -> PrivateKey:
        return self._key

    def save(self, save_to: Path) -> None:
        if not self._cert:
            raise MakeCertCertificateError('Trying to save not yet built certificate')

        cert_data = self._cert.public_bytes(serialization.Encoding.PEM)
        if save_to.exists():
            raise MakeCertFileError(f'Certificate {save_to} already exists')
        save_to.parent.mkdir(parents=True, exist_ok=True)
        with open(save_to, 'wb') as file:
            file.write(cert_data)
        print(f'{save_to} saved')

    def create(
        self,
        subject: x509.Name,
        issuer_cert: 'None | Certificate' = None,
        not_valid_after_days: None | int = None,
    ):
        """
        :issuer_cert: when None, create root cert
        """
        if issuer_cert is None:
            issuer = subject
            self._signing_key = self._key
        else:
            issuer = issuer_cert.value.subject
            self._signing_key = issuer_cert.key

        key = self._key.value

        key_identifier = x509.SubjectKeyIdentifier.from_public_key(key.public_key())

        now = utcnow()
        not_valid_after = RFC5280_UNDEFINED_NOT_AFTER
        if not_valid_after_days is not None:
            not_valid_after = now + timedelta(days=not_valid_after_days)

        self._builder = self._builder\
            .subject_name(subject)\
            .issuer_name(issuer)\
            .public_key(key.public_key())\
            .serial_number(x509.random_serial_number())\
            .not_valid_before(now)\
            .not_valid_after(not_valid_after)\
            .add_extension(key_identifier, critical=False)

        if issuer_cert:
            ext = issuer_cert.value\
                .extensions\
                .get_extension_for_class(x509.SubjectKeyIdentifier)\
                .value
            auth_key_indent = x509.AuthorityKeyIdentifier.from_issuer_subject_key_identifier(ext)
            self._builder = self._builder\
                .add_extension(auth_key_indent, critical=False)

    def add_extension_basic_constraints_and_key_usage(self, ca: bool, path_length: None | int = None) -> None:
        constr = x509.BasicConstraints(ca=ca, path_length=path_length)
        if ca:
            key_usage = x509.KeyUsage(**DEFAULT_CA_KEY_USAGE)
        else:
            key_usage = x509.KeyUsage(**DEFAULT_END_ENTITY_KEY_USAGE)

        self._builder = self._builder\
            .add_extension(constr, critical=True)\
            .add_extension(key_usage, critical=True)
        print(f'Added BasicConstraints = {constr}')
        print(f'Added KeyUsage = {key_usage}')

    def add_extension_extended_key_usage(self, client=False, server=False) -> None:
        usages = []
        if client:
            usages.append(x509.ExtendedKeyUsageOID.CLIENT_AUTH)
        if server:
            usages.append(x509.ExtendedKeyUsageOID.SERVER_AUTH)
        if usages:
            ext_key_usage = x509.ExtendedKeyUsage(usages)
            self._builder = self._builder.add_extension(ext_key_usage, critical=False)
            print(f'Added ExtendedKeyUsage = {usages}')

    def add_extension_subject_alternative_name(
        self,
        dns_names: None | list[str] = None,
        ip_addresses: None | list[str] = None,
    ) -> None:
        names: list[x509.GeneralName] = []
        if dns_names:
            names += [x509.DNSName(n) for n in dns_names]
        if ip_addresses:
            names += [x509.IPAddress(ipaddress.ip_address(i)) for i in ip_addresses]
        if names:
            san = x509.SubjectAlternativeName(names)
            self._builder = self._builder.add_extension(san, critical=False)
            print(f'Added subjectAltName = {names}')

    def sign(self) -> None:
        if self._cert:
            raise MakeCertCertificateError('Trying to sign already signed certificate')
        if not self._signing_key:
            raise MakeCertCertificateError('Trying to sign before create')
        self._cert = self._builder.sign(self._signing_key.value, hashes.SHA256())
        print(f'Certificate for {self._cert.subject.rfc4514_string()} has been created')
