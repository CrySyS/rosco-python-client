from datetime import datetime

from api_object import APIObject
from result import Result

class JAR(APIObject):
    def __init__(self, md5=None, sha1=None, sha256=None, object_uploads=None, signatures=None, last_viewed=None,
        queried_count=None, create_date=None, compress_type=None, create_system=None, create_version=None,
        extract_version=None, manifest_java_version=None, signfile_java_version=None, manifest_version=None,
        signfile_version=None, classpath=None, manifest_vendor=None, signfile_vendor=None, has_enveloped_data=None,
        certs=None, inner_files=None, potential_malware=None
    ):
        super(JAR, self).__init__(md5, sha1, sha256, last_viewed, queried_count, object_uploads, signatures)

        self.create_date =              tuple(datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in create_date.split(' - ')) # Create datetime
        self.compress_type =            set(compress_type.split('; '))      # Compress type
        self.create_system =            create_system                       # Create system
        self.create_version =           set(create_version.split('; '))     # Create version
        self.extract_version =          set(extract_version.split('; '))    # Extract version
        self.manifest_java_version =    manifest_java_version               # Java version from manifest
        self.signfile_java_version =    signfile_java_version               # Java version from signature file
        self.manifest_version =         manifest_version                    # Manifest version
        self.signfile_version =         signfile_version                    # Signature file version
        self.classpath =                classpath                           # Classpath
        self.manifest_vendor =          manifest_vendor                     # Vendor from manifest
        self.signfile_vendor =          signfile_vendor                     # Vendor from signature file
        self.has_enveloped_data =       has_enveloped_data == 'True'        # Has enveloped data
        self.certs =                    certs                               # Certificates sha256 hash in JAR
        self.inner_files =              inner_files                         # Inner files and hashes
        self.potential_malware =        potential_malware == 'True'         # Potential malware

    def get_contained_certs(self, api):
        certs = list(cert['sid'] for cert in self.certs)
        return Result(api, certs, api.OBJECT_TYPES.CERT)

    def __repr__(self):
        return '<ROSCO Java archive object at %s>' % (hex(id(self)))

    def __str__(self):
        return_string = self._to_string(width=20, blacklist=['certs', 'signatures', 'object_uploads', 'inner_files'])

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

def as_jar(dictionary):
    return JAR(**dictionary)
