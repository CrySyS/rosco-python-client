from base_object_search import BaseObjectSearch

class CertSearch(BaseObjectSearch):
    class Filters(object):
        filename =                  'filename'
        serial_number =             'serial_number'
        issuer_common_name =        'issuer_common_name'
        issuer_state =              'issuer_state'
        issuer_organization =       'issuer_organization'
        issuer_country =            'issuer_country'
        not_before =                'not_before'
        not_after =                 'not_after'
        subject_common_name =       'subject_common_name'
        subject_state =             'subject_state'
        subject_organization =      'subject_organization'
        subject_country =           'subject_country'
        extension_basic_constraints = 'extension_basic_constraints'
        extension_key_usage =       'extension_key_usage'
        extension_extended_key_usage = 'extension_extended_key_usage'
        extension_ns_cert_type =    'extension_ns_cert_type'

class PESearch(BaseObjectSearch):
    class Filters(object):
        filename =                  'filename'
        minimum_os =                'minimum_os'
        timestamp =                 'timestamp'
        type =                      'type'
        potential_malware =         'potential_malware'

class JARSearch(BaseObjectSearch):
    class Filters(object):
        filename =                  'filename'
        hash =                      'hash'
        vendor =                    'vendor'
        potential_malware =         'potential_malware'

class APKSearch(BaseObjectSearch):
    class Filters(object):
        filename =                  'filename'
        hash =                      'hash'
        vendor =                    'vendor'
        potential_malware =         'potential_malware'
        permissions =               'permissions'
        package_name =              'package_name'

class PKeySearch(BaseObjectSearch):
    class Filters(object):
        type =                      'type'
        length =                    'length'
