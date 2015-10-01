#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Balazs Kocso"
__version__ = "1.0.0"
__status__ = "beta"

import argparse
import logging
import json
import urllib
import urllib2
import os.path

from postfile import PostFile

# Objects
from objects import Cert
from objects import PE
from objects import JAR
from objects import APK
from objects import PKey
from objects import Result
from objects import ConnectedResult

# Search objects
from search import Filter
from search import CertSearch
from search import PESearch
from search import JARSearch
from search import APKSearch
from search import PKeySearch

logger = logging.getLogger("ROSCOClient")

FILE_SIZE_LIMIT = 10 * 1024 ** 3 # 10 GB

class ObjectTypes(object):
    CERT =   'cert'
    PE =     'pe'
    JAR =    'jar'
    APK =    'apk'
    PKEY =   'pkey'

class RelationTypes(object):
    CONTAIN = 'contain'
    VERIFY = 'verify'

class ROSCO(object):
    HOST_PORT = "https://rosco.crysys.hu/"
    OBJECT_TYPES = ObjectTypes

    class ApiError(Exception):
        def __init__(self, message):
            Exception.__init__(self, message)

    class GetObjectRequest(object):
        OBJECT_TYPES = [ObjectTypes.CERT, ObjectTypes.PE, ObjectTypes.JAR, ObjectTypes.PE, ObjectTypes.PKEY]
        def __init__(self, hash, object_type = None):
            self.hash = hash

            if object_type in self.OBJECT_TYPES:
                self.object_type = object_type

    class GetConnectedObjectRequest(object):
        def __init__(self, hash):
            self.hash = hash

    class SearchObjectRequest(object):
            def __init__(self, api_key, filter):
                self.api_key = api_key
                self.filter = filter

    def __init__(self, api_key):
        self.api_key = api_key
        if not api_key:
            raise self.ApiError("API key is empty.")

    def __repr__(self):
        return "<ROSCO API proxy>"

    @staticmethod
    def date_to_string(date):
        return date.strftime("%Y-%m-%d %H:%M:%S")

    def get_object(self, hash, object_type = None):
        logger.info("Get object with %s" % (hash))

        params = urllib.urlencode({'api_key': self.api_key})
        req = urllib2.Request(self.HOST_PORT + 'api/get/object?%s' % params)
        req.add_header('Content-Type', 'application/json')

        get_object_request = self.GetObjectRequest(hash, object_type)
        data = json.dumps(get_object_request, default = lambda o: o.__dict__)

        try:
            handler = urllib2.urlopen(req, data)
            response = handler.read()
            result = json.loads(response)
        except urllib2.HTTPError as error:
            raise self.ApiError(error.read())
        except urllib2.URLError as error:
            raise self.ApiError(error.reason)
        except Exception as e:
            raise self.ApiError(e.message)

        if result['object_type'] == ObjectTypes.CERT:
            return Cert(**result['object'])
        elif result['object_type'] == ObjectTypes.PE:
            return PE(**result['object'])
        elif result['object_type'] == ObjectTypes.JAR:
            return JAR(**result['object'])
        elif result['object_type'] == ObjectTypes.APK:
            return APK(**result['object'])
        elif result['object_type'] == ObjectTypes.PKEY:
            return PKey(**result['object'])
        else:
            return None

    def get_connected_object(self, hash):
        logger.info("Get connected objects for %s" % (hash))

        params = urllib.urlencode({'api_key': self.api_key})
        req = urllib2.Request(self.HOST_PORT + 'api/get/connected_object?%s' % params)
        req.add_header('Content-Type', 'application/json')

        g = self.GetConnectedObjectRequest(hash)
        data = json.dumps(g, default = lambda o: o.__dict__)

        try:
            handler = urllib2.urlopen(req, data)
            response = handler.read()
            result = json.loads(response)['result']
        except urllib2.HTTPError as error:
            raise self.ApiError(error.read())
        except urllib2.URLError as error:
            raise self.ApiError(error.reason)
        except Exception as e:
            raise self.ApiError(e.message)

        contain_objects = []
        verify_objects = []
        for element in result:
            if element['relation'] == RelationTypes.CONTAIN:
                contain_objects.append(element['hash'])
            elif element['relation'] == RelationTypes.VERIFY:
                verify_objects.append(element['hash'])

        return ConnectedResult(
            contain=Result(self, contain_objects),
            verifiy=Result(self, verify_objects)
        )

    def search(self, search):
        logger.info("Search with %s" % (search.__class__.__name__))

        params = urllib.urlencode({'api_key': self.api_key})
        if isinstance(search, CertSearch):
            req = urllib2.Request(self.HOST_PORT + 'api/search/cert?%s' % params)
            object_type = ObjectTypes.CERT
        elif isinstance(search, PESearch):
            req = urllib2.Request(self.HOST_PORT + 'api/search/pe?%s' % params)
            object_type = ObjectTypes.PE
        elif isinstance(search, JARSearch):
            req = urllib2.Request(self.HOST_PORT + 'api/search/jar?%s' % params)
            object_type = ObjectTypes.JAR
        elif isinstance(search, APKSearch):
            req = urllib2.Request(self.HOST_PORT + 'api/search/apk?%s' % params)
            object_type = ObjectTypes.APK
        elif isinstance(search, PKeySearch):
            req = urllib2.Request(self.HOST_PORT + 'api/search/pkey?%s' % params)
            object_type = ObjectTypes.APK
        else:
            raise ValueError()
        req.add_header('Content-Type', 'application/json')

        search_object_request = self.SearchObjectRequest(self.api_key, search)
        data = json.dumps(search_object_request, default = lambda o: o.__dict__)

        try:
            handler = urllib2.urlopen(req, data)
            response = handler.read()
            result = json.loads(response)['result']
        except urllib2.HTTPError as error:
            raise self.ApiError(error.read())
        except urllib2.URLError as error:
            raise self.ApiError(error.reason)
        except Exception as e:
            raise self.ApiError(e.message)

        return Result(self, result, object_type)

    def upload(self, filepath):
        logger.info("Upload file: %s" % (filepath))

        with open(filepath, 'rb') as fd:
            data = fd.read()

        try:
            params = urllib.urlencode({'api_key': self.api_key})
            result = PostFile.post_multipart_url(
                url = self.HOST_PORT + 'api/upload/file?%s' % params,
                fields = [],
                files = [
                    ('file',
                     os.path.basename(filepath),
                     data)
                ]
            )
        except PostFile.PostFileException as e:
            raise self.ApiError(e)

        return result.read()

    def get_down_objects(self, object):
        connected_objects = object.get_connected_object(self)
        if isinstance(object, PKey):
            return connected_objects.verify
        else:
            return connected_objects.contain

    def get_up_objects(self, object):
        connected_objects = object.get_connected_object(self)
        if isinstance(object, PKey):
            return connected_objects.contain
        else:
            return connected_objects.verify

    def get_verified_objects(self, begin_object, filter=object, limit=None):
        queue = self.get_down_objects(begin_object)
        visited = set()
        cnt = 0
        for object in queue:
            # Check the limit
            if limit is not None and cnt > limit:
                break
            # Check the cycles
            if object.sha256 in visited:
                continue
            # Check the filter
            if isinstance(object, filter):
                yield object
            # Save the visited objects
            visited.add(object.sha256)
            # Get the new down objects and put in the queue
            queue.extend(self.get_down_objects(object))
            # Increase the counter
            cnt += 1

    def get_verifier_certs(self, begin_object, limit=None):
        queue = self.get_up_objects(begin_object)
        visited = set()
        cnt = 0
        for object in queue:
            # Check the limit
            if limit is not None and cnt > limit:
                break
            # Check the cycles
            if object.sha256 in visited:
                continue
            # Check the filter
            if isinstance(object, Cert):
                yield object
            # Save the visited objects
            visited.add(object.sha256)
            # Get the new down objects and put in the queue
            queue.extend(self.get_up_objects(object))
            # Increase the counter
            cnt += 1


def main():
    parser = argparse.ArgumentParser(description='ROSCOClient')
    runmode_group = parser.add_mutually_exclusive_group(required = True)
    runmode_group.add_argument(
        "--hash",
        dest = "hash",
        default = None,
        help = "Hash search"
    )
    runmode_group.add_argument(
        "--connected",
        dest = "connected",
        default = None,
        help = "Get connected objects"
    )
    runmode_group.add_argument(
        "--cert",
        dest = "cert",
        default = None,
        help = "Certificate search"
    )
    runmode_group.add_argument(
        "--pe",
        dest = "pe",
        default = None,
        help = "PE search"
    )
    runmode_group.add_argument(
        "--jar",
        dest = "jar",
        default = None,
        help = "JAR search"
    )
    runmode_group.add_argument(
        "--apk",
        dest = "apk",
        default = None,
        help = "APK search"
    )
    runmode_group.add_argument(
        "--pkey",
        dest = "pkey",
        default = None,
        help = "Public key search"
    )
    runmode_group.add_argument(
        "--upload",
        dest = "upload",
        default = None,
        help = "Upload file"
    )
    api_key_group = parser.add_mutually_exclusive_group(required = False)
    api_key_group.add_argument(
        "-k", "--key",
        dest = "api_key",
        default = None,
        help = "Set ROSCO API key."
    )
    api_key_group.add_argument(
        "-kf", "--keyfile",
        dest = "api_key_file",
        default = None,
        help = "Set ROSCO API key from file"
    )
    parser.add_argument(
        "-v", "--verbose",
        dest = "verbose",
        action = "store_true",
        default = False,
        help = "Verbose."
    )
    args = parser.parse_args()

    logging.basicConfig(format='[%(levelname)0.1s %(asctime)s %(name)s] %(message)s', datefmt="%y%m%d %H:%M:%S")
    logging.getLogger().setLevel(logging.DEBUG if args.verbose else logging.WARNING)

    # Key management
    API_KEY = "1"
    if args.api_key is not None:
        api_key = args.api_key
    elif args.api_key_file is not None:
        with open(args.api_key_file, 'r') as fp:
            api_key = fp.readline()
    else:
        api_key = API_KEY

    # Initialize ROSCO object
    rosco = ROSCO(api_key)

    # Processing search
    if args.hash is not None:
        try:
            result = rosco.get_object(args.hash)
            if args.verbose: print
            print 'Requested object:', result.__class__.__name__, '\n'
            print result
        except ROSCO.ApiError as err:
            logger.warning(err)
            return
    elif args.connected is not None:
        try:
            result = rosco.get_connected_object(args.connected)
            if args.verbose: print
            print result
            print 'Total object count:', len(result)
        except ROSCO.ApiError as err:
            logger.warning(err)
            return
    elif args.upload is not None:
        try:
            result = rosco.upload(args.upload)
            if args.verbose: print
            print result
        except ROSCO.ApiError as err:
            logger.warning(err)
            return
    else:
        if args.cert is not None:
            search = CertSearch()
            text = args.cert
        elif args.pe is not None:
            search = PESearch()
            text = args.pe
        elif args.jar is not None:
            search = JARSearch()
            text = args.jar
        elif args.apk is not None:
            search = APKSearch()
            text = args.apk
        elif args.pkey is not None:
            search = PKeySearch()
            text = args.pkey
        else:
            parser.print_help()
            return

        for filter in text.replace(',', ';').split(';'):
            try:
                key_value, type = filter.split('#', 1)
            except ValueError:
                key_value = filter
                type = 'prefix'
            if type.strip() not in ['prefix', 'start', 'stop', 'substring']:
                logger.warning("'%(name)s' is not compatible search mode" % {'name': type.strip()})
                return

            try:
                key, value = key_value.split(':', 1)
            except ValueError:
                logger.warning("'%(name)s' doesn't contain 'key:value'" % {'name': key_value})
                return

            try:
                search.add_filter(key.strip(), **{type.strip(): value.strip()})
            except (search.SearchException, Filter.FilterException) as e:
                logger.warning(e.message)
                return

        try:
            result = rosco.search(search)
            if args.verbose: print
            print result
            print 'Total object count:', len(result)
        except ROSCO.ApiError as err:
            logger.warning(err)
            return

if __name__ == "__main__":
    main()
