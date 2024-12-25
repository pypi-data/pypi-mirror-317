class MakeCertError(RuntimeError):
    ...


class MakeCertKeyError(MakeCertError):
    ...


class MakeCertCertificateError(MakeCertError):
    ...


class MakeCertCertificateRevocationListError(MakeCertError):
    ...


class MakeCertFileError(MakeCertError):
    ...
