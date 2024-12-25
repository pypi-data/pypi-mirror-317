from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization

from make_certs.certificate import Certificate
from make_certs.exceptions import MakeCertCertificateRevocationListError
from make_certs.private_key import PrivateKey
from make_certs.utils import RFC5280_UNDEFINED_NOT_AFTER, utcnow


class CertificateRevokationList:
    """
    load_from_file() | create() -> revoke() -> save()
    """
    def __init__(self, key: PrivateKey) -> None:
        self._key = key
        self._crl: None | x509.CertificateRevocationList = None
        self._builder = x509.CertificateRevocationListBuilder()

    @property
    def value(self) -> x509.CertificateRevocationList:
        if self._crl is None:
            raise MakeCertCertificateRevocationListError('Trying to get not created CRL')
        return self._crl

    @property
    def key(self) -> PrivateKey:
        return self._key

    def load_from_file(self, load_from: Path) -> None:
        """
        Load signed certificate revokation list.
        """
        with open(load_from, 'rb') as file:
            self._crl = x509.load_pem_x509_crl(file.read(), default_backend())
        self._builder = x509.CertificateRevocationListBuilder().issuer_name(self._crl.issuer)

    def create(self, issuer: x509.Name, next_update_days: None | int = None) -> None:
        """
        Create signed certificate revokation list.

        :issuer:
        :next_update_days: time in days from now for nextUpdate field, max date when None
        """
        now = utcnow()

        self._builder = self._builder.issuer_name(issuer)
        self.set_next_update(next_update_days, from_time=now)
        self._sign(last_update=now)

    def set_next_update(self, next_update_days: None | int = None, from_time=utcnow()) -> None:
        """
        Change nextUpdate field of certificate revokation list.

        Will be only applied after create and sing CRL (e.g. by create() or revoke()).
        """
        if next_update_days is not None:
            next_update = from_time + timedelta(days=next_update_days)
        else:
            next_update = RFC5280_UNDEFINED_NOT_AFTER
        self._builder = self._builder.next_update(next_update)

    def save(self, save_to: Path) -> None:
        if self._crl is None:
            raise MakeCertCertificateRevocationListError('Trying to save not created CRL')
        save_to.parent.mkdir(parents=True, exist_ok=True)
        with open(save_to, 'wb') as file:
            file.write(self._crl.public_bytes(serialization.Encoding.PEM))
        print(f'{save_to} saved')

    def revoke(self, certs: Iterable[Certificate | x509.Certificate]) -> bool:
        """
        Revoke certificates and sign new certificate revokation list.

        :certs:
        :return: is changed
        """
        if self._crl is None:
            raise MakeCertCertificateRevocationListError('Trying to revoke with not created CRL')

        plain_certs = list(map(lambda x: x if isinstance(x, x509.Certificate) else x.value, certs))

        sn_revoked = {c.serial_number for c in self._crl}
        sn_new = {c.serial_number for c in plain_certs}
        if sn_new == sn_revoked:
            print('No changes for revokation list')
            return False

        now = utcnow()

        builder_orig = self._builder

        for cert in plain_certs:
            rc = x509.RevokedCertificateBuilder()\
                .serial_number(cert.serial_number)\
                .revocation_date(now)\
                .build()
            self._builder = self._builder.add_revoked_certificate(rc)

        self._sign(last_update=now)

        self._builder = builder_orig
        print(f'Revoked {plain_certs}')
        return True

    def _sign(self, last_update=utcnow()) -> None:
        sign_builder = self._builder.last_update(last_update)
        self._crl = sign_builder.sign(self._key.value, hashes.SHA256(), default_backend())
