from setuptools import setup, find_packages
from checkuser import __version__, __author__, __email__

PACKAGES = [
    *find_packages(),
    'pages',
]
REQUIREMENTS = list(
    map(
        str.strip,
        open('./requirements.txt').readlines(),
    )
)

VERSION = __version__

DESCRIPTION = open('README.md').read()
AUTHOR = __author__
AUTHOR_EMAIL = __email__
URL = 'https://github.com/DTunnel0/DTCheckUser'
LICENSE = 'MIT'

setup(
    name='CheckUser',
    version=VERSION,
    long_description=DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    package_data={'': ['main.py'], 'pages': ['*']},
    include_package_data=True,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'checkuser = checkuser.__main__:main',
        ],
    },
)
