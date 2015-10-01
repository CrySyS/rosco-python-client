from datetime import datetime

from base_object import BaseObject

class Signatures(BaseObject):
    def __init__(self, signature=None, signature_algorithm=None):
        self.signature =            signature               # Signature
        self.signature_algorithm =  signature_algorithm     # Signature algorithm

    def __repr__(self):
        return '<ROSCO Signature object at %s>' % (hex(id(self)))

    def __str__(self):
        return self._to_string(prefix=' ' * 3)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

class ObjectUpload(BaseObject):
    def __init__(self, timestamp=None, batch = None, filename=None, original_link=None, download_link=None,
            container_object=None):

        self.timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

        # Optional attributes
        if filename is not None:                            # Filename
            self.filename = filename
        if batch is not None:                               # Batch
            self.batch = batch
        if original_link is not None:                       # Original link
            self.original_link = original_link
        if download_link is not None:                       # Download link
            self.download_link = download_link
        if container_object is not None:                    # Container object SHA256 hash
            self.container_object = container_object

    def __repr__(self):
        return '<ROSCO Object upload object at %s>' % (hex(id(self)))

    def __str__(self):
        return self._to_string(width=15, prefix=' ' * 3)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

class APIObject(BaseObject):
    def __init__(self, md5=None, sha1=None, sha256=None, last_viewed=None, queried_count=None, object_uploads=None,
        signatures=None
    ):
        self.md5 =              md5                     # MD5 hash from object content
        self.sha1 =             sha1                    # SHA1 hash from object content
        self.sha256 =           sha256                  # SHA256 hash from object content
        self.last_viewed =      datetime.strptime(last_viewed, '%Y-%m-%d %H:%M:%S') if last_viewed != '-' else None # Last view of object
        self.queried_count =    queried_count           # Query counter of object

        self.object_uploads = []                        # Object upload information
        for object_upload in object_uploads:
            self.object_uploads.append(ObjectUpload(**object_upload))

        # Optional attributes
        if signatures is not None:
            self.signatures = []                            # Signature
            for signature in signatures:
                    self.signatures.append(Signatures(**signature))
        else:
            self.signatures = None

    def get_connected_object(self, api):
        return api.get_connected_object(self.sha256)

    def __repr__(self):
        return '<ROSCO APIObject object at %s>' % (hex(id(self)))

    def __str__(self):
        return_string = self._to_string(width=27, blacklist=['signatures', 'object_uploads'])

        if self.signatures is not None:
            return_string += "Signatures:\n"
            for signature in self.signatures:
                return_string += str(signature) + "\n"

        return_string += 'Object uploads:\n'
        for object_upload in self.object_uploads:
            return_string += str(object_upload) + "\n"

        return return_string

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __hash__(self):
        return self.sha256
