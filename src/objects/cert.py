from api_object import APIObject
from base_object import BaseObject
from datetime import datetime

class CertExtension(BaseObject):
    def __init__(self, type, value, criticality):
        self.type =                         type                            # Extension type
        self.value =                        value                           # Extension Value
        self.criticality =                  bool(criticality)               # Extension criticality

    def __repr__(self):
        return '<ROSCO Certificate Extension object at %s>' % (hex(id(self)))

    def __str__(self):
        return self._to_string(width=13, prefix=' ' * 3)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

class Cert(APIObject):
    def __init__(self, md5=None, sha1=None, sha256=None, object_uploads=None, signatures=None, last_viewed=None,
        queried_count=None, der_md5=None, der_sha1=None, der_sha256=None, version=None, serial_number=None,
        issuer_common_name=None, issuer_country=None, issuer_email=None, issuer_given_name=None, issuer_location=None,
        issuer_organization=None, issuer_organization_unit=None, issuer_serial_number=None, issuer_state=None,
        issuer_street=None, issuer_surname=None, not_before=None, not_after=None, subject_common_name=None,
        subject_country=None, subject_email=None, subject_given_name=None, subject_location=None,
        subject_organization=None, subject_organization_unit=None, subject_serial_number=None, subject_state=None,
        subject_street=None, subject_surname=None, extensions=None
    ):

        super(Cert, self).__init__(md5, sha1, sha256, last_viewed, queried_count, object_uploads, signatures)

        self.der_md5 =                      der_md5                         # MD5 hash from Cert DER format
        self.der_sha1 =                     der_sha1                        # SHA1 hash from Cert DER format
        self.der_sha256 =                   der_sha256                      # SHA256 hash from Cert DER format
        self.version =                      int(version)                    # Version
        self.serial_number =                serial_number                   # Serial number
        self.issuer_common_name =           issuer_common_name              # Issuer common name
        self.issuer_country =               issuer_country                  # Issuer country
        self.issuer_email =                 issuer_email                    # Issuer e-mail
        self.issuer_given_name =            issuer_given_name               # Issuer given name
        self.issuer_location =              issuer_location                 # Issuer location
        self.issuer_organization =          issuer_organization             # Issuer organization
        self.issuer_organization_unit =     issuer_organization_unit        # Issuer organization unit
        self.issuer_serial_number =         issuer_serial_number            # Issuer serial number
        self.issuer_state =                 issuer_state                    # Issuer state or province
        self.issuer_street =                issuer_street                   # Issuer street
        self.issuer_surname =               issuer_surname                  # Issuer surname
        self.not_before =                   datetime.strptime(not_before, '%Y-%m-%d %H:%M:%S')  # Valid not before
        self.not_after =                    datetime.strptime(not_after, '%Y-%m-%d %H:%M:%S')   # Valid not after
        self.subject_common_name =          subject_common_name             # Subject common name
        self.subject_country =              subject_country                 # Subject country
        self.subject_email =                subject_email                   # Subject e-mail
        self.subject_given_name =           subject_given_name              # Subject given name
        self.subject_location =             subject_location                # Subject location
        self.subject_organization =         subject_organization            # Subject organization
        self.subject_organization_unit =    subject_organization_unit       # Subject organization unit
        self.subject_serial_number =        subject_serial_number           # Subject serial number
        self.subject_state =                subject_state                   # Subject state or province
        self.subject_street =               subject_street                  # Subject street
        self.subject_surname =              subject_surname                 # Subject surname

        if extensions is not None:
            self.extensions = []                                                # Extensions
            for extension in extensions:
                    self.extensions.append(CertExtension(**extension))

    def __repr__(self):
        return '<ROSCO Certificate object at %s>' % (hex(id(self)))

    def __str__(self):
        return_string = self._to_string(width=27, blacklist=['extensions', 'signatures', 'object_uploads'])

        return_string += "Extensions:\n"
        for extension in self.extensions:
            return_string += str(extension) + "\n"

        return_string += "Signatures:\n"
        for signature in self.signatures:
            return_string += str(signature) + "\n"

        return_string += 'Object uploads:\n'
        for object_upload in self.object_uploads:
            return_string += str(object_upload) + "\n"

        return return_string

def as_cert(dictionary):
    return Cert(**dictionary)


