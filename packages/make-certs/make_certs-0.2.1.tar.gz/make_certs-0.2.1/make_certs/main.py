#!/bin/env python3

from __future__ import annotations

import argparse

from pathlib import Path
from typing import Any

import yaml

from cryptography import x509
from cryptography.x509.oid import NameOID

from make_certs.private_key import PrivateKey
from make_certs.certificate import Certificate, load_from_file
from make_certs.certificate_revokation_list import CertificateRevokationList


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='make_cert',
        description='Create x509 certificates heirarhy',
    )
    parser.add_argument('filename')
    return parser.parse_args()


class HierBuilder:
    def __init__(self, hier_file_path: Path | str) -> None:
        if isinstance(hier_file_path, str):
            hier_file_path = Path(hier_file_path)

        print(f'Creating certificates for {hier_file_path} hierarhy...')
        with open(hier_file_path, 'r') as file:
            data = yaml.safe_load(file)

        self.base_dir = hier_file_path.absolute().parent
        self.subjects = {k: self.name_from_dict(val) for k, val in data['names'].items()}

        for cert_path_str, cert_dict in data['certs'].items():
            self.cert_from_dict(cert_path=Path(cert_path_str), options=cert_dict)

        for crl_path_str, crl_dict in data.get('revokation_lists', {}).items():
            self.revokation_list_from_dict(crl_path=Path(crl_path_str), options=crl_dict)

        print(f'Hierarhy {hier_file_path} is done.')

    def resolve_path(self, path: Path | str) -> Path:
        path = Path(path)
        if not path.is_absolute():
            return self.base_dir / path
        return path

    @staticmethod
    def name_from_dict(data: dict[str, str]) -> x509.Name:
        attrs_list = []
        for k, val in data.items():
            attr_type = getattr(NameOID, k.upper())
            attr = x509.NameAttribute(attr_type, val)
            attrs_list.append(attr)
        return x509.Name(x509.RelativeDistinguishedName(attrs_list))

    def cert_from_dict(
        self,
        cert_path: Path,
        options: dict[str, Any],
        issuer_cert: None | Certificate = None,
        signing_key: None | PrivateKey = None,
    ) -> None:
        cert_path = self.resolve_path(cert_path)

        print(f'Processing {cert_path} cert...')

        cert_dir = cert_path.parent
        key_path = cert_dir / f'{cert_path.stem}.key'
        key_type = options.get('key_type', 'ecc')
        key_password = options.get('key_password')
        key = self._get_or_create_key(key_path, key_type=key_type, password=key_password)

        cert = Certificate(key)
        if cert_path.exists():
            print(f'{cert_path} already exists')
            cert.load_from_file(cert_path)
        else:
            subject = self.subjects[options['subject']]
            cert.create(
                subject=subject,
                issuer_cert=issuer_cert,
                not_valid_after_days=options.get('not_valid_after_days'),
            )
            self._tune_cert(cert=cert, options=options)
            cert.sign()
            cert.save(cert_path)

        for next_cert_path_str, next_cert_options in options.get('issue', {}).items():
            next_cert_path = Path(next_cert_path_str)
            self.cert_from_dict(
                cert_path=next_cert_path,
                options=next_cert_options,
                issuer_cert=cert,
                signing_key=key,
            )

    def revokation_list_from_dict(self, crl_path: Path, options: dict[str, Any]) -> None:
        crl_path = self.resolve_path(crl_path)

        print(f'Processing {crl_path} CRL...')

        crl_dir = crl_path.parent
        key_path = crl_dir / f'{crl_path.stem}.key'
        key_type = options.get('key_type', 'ecc')
        key_password = options.get('key_password')
        key = self._get_or_create_key(key_path, key_type=key_type, password=key_password)

        crl = CertificateRevokationList(key)
        next_update_days = options.get('next_update_days')

        if crl_path.exists():
            crl.load_from_file(crl_path)
            crl.set_next_update(next_update_days)
        else:
            issuer = self.subjects[options['issuer']]
            crl.create(issuer=issuer, next_update_days=next_update_days)

        certs = [load_from_file(self.resolve_path(p)) for p in options.get('revoke',  [])]
        if crl.revoke(certs):
            crl.save(crl_path)

    def _get_or_create_key(
        self, key_path: Path,
        key_type: str,
        password: None | str
    ) -> PrivateKey:
        if key_path.exists():
            print(f'{key_path} already exists')
            key = PrivateKey.from_file(key_path, password)
        else:
            key = PrivateKey(key_type)
            key.save(key_path, password)
        return key

    def _tune_cert(self, cert: Certificate, options: dict[str, Any]) -> None:
        basic_constr = options.get('basic_constraints', {})
        ca = basic_constr.get('ca', False)
        path_length = basic_constr.get('path_length')
        cert.add_extension_basic_constraints_and_key_usage(ca=ca, path_length=path_length)
        ex_key_usage = options.get('extended_key_usage', {})
        is_server = ex_key_usage.get('server', False)
        is_client = ex_key_usage.get('client', False)
        cert.add_extension_extended_key_usage(server=is_server, client=is_client)
        dns_names = options.get('alternative_names_dns', [])
        ip_addrs = options.get('alternative_names_ip', [])
        cert.add_extension_subject_alternative_name(dns_names=dns_names, ip_addresses=ip_addrs)


def main() -> None:
    args = get_args()
    HierBuilder(args.filename)


if __name__ == '__main__':
    main()
