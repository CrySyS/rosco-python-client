try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__version__ = '1.0'
__author__ = 'Balazs Kocso'

setup(name = 'rosco_client',
    version = __version__,
    description = 'Python client for ROSCO API system',
    author = __author__,
    url = "https://github.com/CrySyS/rosco-python-client",
    license = "http://www.apache.org/licenses/LICENSE-2.0",
    packages = [
        'rosco_client',
        'rosco_client.objects',
        'rosco_client.search'
    ],
    package_dir = {
        'rosco_client': 'src',
        'rosco_client.objects': 'src/objects',
        'rosco_client.search': 'src/search'
    },
    provides=['rosco_client','ROSCOClient']
)
