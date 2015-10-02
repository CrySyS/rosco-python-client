# rosco-python-client
Python client for ROSCO JSON API

The ROSCO Web interface can be found on [https://rosco.crysys.hu](https://rosco.crysys.hu/). The JSON programming interface can be used with API Key after the registration.

## Use as python package

As you can see in the [test/example.py](https://github.com/CrySyS/rosco-python-client/blob/master/test/example.py), the python client can be used as a python package with `import rosco_client`.

## Use command line interface

You can use it by running [src/\_\_main\_\_.py](https://github.com/CrySyS/rosco-python-client/blob/master/src/__main__.py) or 'python -m rosco_client' after package installation.

    $ python -m rosco_client -h
    usage: src [-h]
               (--hash HASH | --connected CONNECTED | --cert CERT | --pe PE | --jar JAR | --apk APK | --pkey PKEY | --upload UPLOAD)
               [-k API_KEY | -kf API_KEY_FILE] [-v]

    ROSCOClient

    optional arguments:
      -h, --help                Show this help message and exit
      --hash HASH               Hash search
      --connected CONNECTED     Get connected objects
      --cert CERT               Certificate search
      --pe PE                   PE search
      --jar JAR                 JAR search
      --apk APK                 APK search
      --pkey PKEY               Public key search
      --upload UPLOAD           Upload file
      -k API_KEY, --key API_KEY Set ROSCO API key.
      -kf API_KEY_FILE, --keyfile API_KEY_FILE Set ROSCO API key from file
      -v, --verbose             Verbose mode

The filters for the searches are defined in the [src/search/object_search.py](https://github.com/CrySyS/rosco-python-client/blob/master/src/search/object_search.py).