from caesarcipher import __version__

scripts = ['bin/caesarcipher']

setup_args = {
    'name': 'caesarcipher',
    'version': __version__,
    'url': 'https://github.com/RobSpectre/Caesar-Cipher',
    'description': 'A Python package and command line script for encoding, '
                   'decoding and cracking Caesar ciphers.',
    'long_description': open('README.rst').read(),
    'author': 'Rob Spectre',
    'author_email': 'rob@brooklynhacker.com',
    'license': 'MIT',
    'packages': ['caesarcipher', 'tests'],
    'scripts': ['bin/caesarcipher'],
    'include_package_data': True,
    'classifiers': [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Environment :: Console',
        'Topic :: Security :: Cryptography',
    ]
}

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(**setup_args)
