from api_object import APIObject
from result import Result


class PE(APIObject):
    def __init__(self, md5=None, sha1=None, sha256=None, object_uploads=None, signatures=None, last_viewed=None,
        queried_count=None, characteristic=None, machine=None, timestamp=None, linker_version=None, minimum_os=None,
        minimum_subsystem=None, pe_type=None, has_enveloped_data=None, certs=None, potential_malware=None
    ):
        super(PE, self).__init__(md5, sha1, sha256, last_viewed, queried_count, object_uploads, signatures)

        self.characteristic =       characteristic                  # Characteristic of PE
        self.machine =              machine                         # Targeted CPU
        self.timestamp =            timestamp                       # Datetime of compiling
        self.linker_version =       linker_version                  # Linker version
        self.minimum_os =           minimum_os                      # Minimum OS requirement
        self.minimum_subsystem =    minimum_subsystem               # Minimum Subsystem
        self.pe_type =              pe_type                         # Type: EXE, DLL, DRIVER, UNKNOWN
        self.has_enveloped_data =   has_enveloped_data == 'True'    # Has enveloped data
        self.certs =                certs                           # Certificates sha256 hash in PE
        self.potential_malware =    potential_malware == 'True'     # Potential malware

    def get_contained_certs(self, api):
        certs = list(cert['sid'] for cert in self.certs)
        return Result(api, certs, api.OBJECT_TYPES.CERT)

    def __repr__(self):
        return '<ROSCO Portable executable object at %s>' % (hex(id(self)))

    def __str__(self):
        return_string = self._to_string(width=20, blacklist=['certs', 'signatures', 'object_uploads'])

        return_string += "Certificates:\n"
        for cert in self.certs:
            return_string += '   ' + 'resource: ' + str(cert['sid']) + "\n"
        return_string += '\n'

        return_string += "Signatures:\n"
        for signature in self.signatures:
            return_string += str(signature) + "\n"

        return_string += 'Object uploads:\n'
        for object_upload in self.object_uploads:
            return_string += str(object_upload) + "\n"

        return return_string


def as_pe(dictionary):
    return PE(**dictionary)
