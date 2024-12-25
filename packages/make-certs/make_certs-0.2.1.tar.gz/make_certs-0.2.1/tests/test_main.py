#! /usr/bin/env python3

import unittest

from distutils.version import LooseVersion
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml
import cryptography

from make_certs.private_key import PrivateKey
from make_certs.certificate import Certificate
from make_certs.main import HierBuilder

CONF = '''
names:
  imyarek:
    country_name: RU
    state_or_province_name: Central Federal District
    locality_name: Moscow
    organization_name: OOO Vector
    common_name: imyarek

certs:
  ./tst_out/ca.crt:
    subject: imyarek
    not_valid_after_days: null
    key_type: ecc
    key_password: null
    basic_constraints:
      ca: true
      path_length: null
    issue:
      ./tst_out/inter.crt:
        subject: imyarek
        not_valid_after_days: null
        key_type: ecc
        key_password: null
        basic_constraints:
          ca: true
          path_length: 0
        issue:
          ./tst_out/server.crt:
            subject: imyarek
            not_valid_after_days: null
            key_type: ecc
            key_password: null
            basic_constraints:
              ca: false
              path_length: null
            alternative_names_ip:
              - '127.0.0.1'
            alternative_names_dns:
              - localhost
              - ooo-vector.example.com
            extended_key_usage:
              server: true
              client: false
'''


def cryptography_enought(required_version: str) -> bool:
    current = LooseVersion(cryptography.__version__)
    required = LooseVersion(required_version)
    return current >= required


class TestIntegral(unittest.TestCase):
    def setUp(self):
        self._tmpdir = TemporaryDirectory()
        self.path = Path(self._tmpdir.name)
        self.hier_file = self.path / 'hier.yaml'
        self.conf = yaml.safe_load(CONF)

    def tearDown(self):
        self._tmpdir.cleanup()

    def _save_conf(self):
        with open(self.hier_file, 'w') as file:
            yaml.dump(self.conf, file)

    def test_creation(self):
        self._save_conf()
        self.assertFalse((self.path / 'tst_out').exists(), 'Temporary test dir is not empty')
        HierBuilder(self.hier_file)
        self.assertTrue((self.path / 'tst_out/ca.key').exists(), 'Missing expected result file')
        self.assertTrue((self.path / 'tst_out/ca.crt').exists(), 'Missing expected result file')
        self.assertTrue((self.path / 'tst_out/inter.key').exists(), 'Missing expected result file')
        self.assertTrue((self.path / 'tst_out/inter.crt').exists(), 'Missing expected result file')
        self.assertTrue((self.path / 'tst_out/server.key').exists(), 'Missing expected result file')
        self.assertTrue((self.path / 'tst_out/server.crt').exists(), 'Missing expected result file')

    def test_create_with_encrypted_keys(self):
        self.conf['certs']['./tst_out/ca.crt']['key_password'] = 'Secret-1'
        issued = self.conf['certs']['./tst_out/ca.crt']['issue']
        issued['./tst_out/inter.crt']['key_password'] = 'Secret-2'
        issued = issued['./tst_out/inter.crt']['issue']
        issued['./tst_out/server.crt']['key_password'] = 'Secret-3'
        self._save_conf()
        HierBuilder(self.hier_file)

    def test_append_new(self):
        self.conf['certs']['./tst_out/ca.crt']['key_password'] = 'Secret-1'
        self._save_conf()
        HierBuilder(self.hier_file)
        with open(self.path / 'tst_out/ca.crt', 'rb') as file:
            ca_crt = file.read()

        issued = self.conf['certs']['./tst_out/ca.crt']['issue']
        issued = issued['./tst_out/inter.crt']['issue']
        issued['./tst_out/client.crt'] = issued['./tst_out/server.crt'].copy()
        issued['./tst_out/client.crt']['key_password'] = 'Secret-2'
        self._save_conf()
        HierBuilder(self.hier_file)
        self.assertTrue((self.path / 'tst_out/client.key').exists(), 'Missing expected result file')
        self.assertTrue((self.path / 'tst_out/client.crt').exists(), 'Missing expected result file')
        with open(self.path / 'tst_out/ca.crt', 'rb') as file:
            ca_crt_new = file.read()

        self.assertEqual(ca_crt, ca_crt_new, 'Seems cert has been recreated')

    @unittest.skipUnless(cryptography_enought('42.0.0'), 'Too old cryptography')
    def test_validate_cert(self):
        from cryptography import x509
        from cryptography.x509.verification import PolicyBuilder, Store

        self._save_conf()
        HierBuilder(self.hier_file)

        ca_key = PrivateKey.from_file(self.path / 'tst_out/ca.key')
        ca_cert = Certificate(ca_key)
        ca_cert.load_from_file(self.path / 'tst_out/ca.crt')

        ica_key = PrivateKey.from_file(self.path / 'tst_out/inter.key')
        ica_cert = Certificate(ica_key)
        ica_cert.load_from_file(self.path / 'tst_out/inter.crt')

        ee_key = PrivateKey.from_file(self.path / 'tst_out/server.key')
        ee_cert = Certificate(ee_key)
        ee_cert.load_from_file(self.path / 'tst_out/server.crt')

        store = Store([ca_cert.value])
        builder = PolicyBuilder().store(store)
        verifier = builder.build_server_verifier(x509.DNSName('false.example.com'))
        with self.assertRaisesRegex(Exception, 'AltName'):
            chain = verifier.verify(ee_cert.value, [ica_cert.value])

        verifier = builder.build_server_verifier(x509.DNSName('ooo-vector.example.com'))
        chain = verifier.verify(ee_cert.value, [ica_cert.value])
        self.assertEqual((len(chain)), 3)

    def test_revokation(self):
        self.conf['revokation_lists'] = {
            './tst_out/crl.pem': {
                'issuer': 'imyarek',
                'key_password': 'Secret-1',
                'revoke': ['./tst_out/server.crt'],
            }
        }
        self._save_conf()
        HierBuilder(self.hier_file)
        self.assertTrue((self.path / 'tst_out/crl.key').exists(), 'Missing expected result file')
        self.assertTrue((self.path / 'tst_out/crl.pem').exists(), 'Missing expected result file')


if __name__ == '__main__':
    unittest.main()
