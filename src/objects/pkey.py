from api_object import APIObject

class PKey(APIObject):
    def __init__(self, md5=None, sha1=None, sha256=None, object_uploads=None, signatures=None, last_viewed=None,
        queried_count=None, type=None, length=None, rsa_e=None, rsa_n=None, dsa_p=None, dsa_q=None, dsa_g=None,
        ecdsa_pub_x=None, ecdsa_pub_y=None, ecdsa_curve=None
    ):
        super(PKey, self).__init__(md5, sha1, sha256, last_viewed, queried_count, object_uploads, signatures)

        self.type =     type            # Public key type: RSA, DSA, ECDSA
        self.length =   length          # Public key length

        # Various attributes
        if self.type == 'RSA':
            self.rsa_e = rsa_e
            self.rsa_n = rsa_n
        elif self.type == 'DSA':
            self.dsa_p = dsa_p
            self.dsa_q = dsa_q
            self.dsa_g = dsa_g
        elif self.type == 'ECDSA':
            self.ecdsa_pub_x = ecdsa_pub_x
            self.ecdsa_pub_y = ecdsa_pub_y
            self.ecdsa_curve = ecdsa_curve

    def __repr__(self):
        return '<ROSCO Public key object at %s>' % (hex(id(self)))

def as_pkey(dictionary):
    return PKey(**dictionary)


