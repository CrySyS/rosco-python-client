from jar import JAR

class APK(JAR):
    def __init__(self, md5=None, sha1=None, sha256=None, object_uploads=None, signatures=None, last_viewed=None,
        queried_count=None, create_date=None, compress_type=None, create_system=None, create_version=None,
        extract_version=None, manifest_java_version=None, signfile_java_version=None, manifest_version=None,
        signfile_version=None, classpath=None, manifest_vendor=None, signfile_vendor=None, has_enveloped_data=None,
        certs=None, inner_files=None, potential_malware=None, android_version=None, package_name=None, permissions=None,
        activities=None, services=None, receivers=None, providers=None
    ):
        super(APK, self).__init__(md5, sha1, sha256, object_uploads, signatures, last_viewed, queried_count,
            create_date, compress_type, create_system, create_version, extract_version, manifest_java_version,
            signfile_java_version, manifest_version, signfile_version, classpath, manifest_vendor, signfile_vendor,
            has_enveloped_data, certs, inner_files, potential_malware)

        self.android_version =      android_version                 # Android version
        self.package_name =         package_name                    # Package name
        self.permissions =          permissions.split('; ')         # Permissions
        self.activities =           activities.split('; ')          # Activities
        self.services =             services.split('; ')            # Services
        self.receivers =            receivers.split('; ')           # Receivers
        self.providers =            providers.split('; ')           # Providers

    def __repr__(self):
        return '<ROSCO Android package object at %s>' % (hex(id(self)))

    def __str__(self):
        return_string = self._to_string(width=20, blacklist=['certs', 'signatures', 'object_uploads', 'inner_files'])

        return_string += "Certificates:\n"
        for cert in self.certs:
            return_string += ' ' * 3 + 'resource: ' + str(cert['sid']) + "\n"
        return_string += '\n'

        return_string += "Signatures:\n"
        for signature in self.signatures:
            return_string += str(signature) + "\n"

        return_string += 'Object uploads:\n'
        for object_upload in self.object_uploads:
            return_string += str(object_upload) + "\n"

        return return_string

def as_apk(dictionary):
    return APK(**dictionary)
