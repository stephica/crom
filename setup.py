from setuptools import setup
import sys

if (sys.version_info[0:2] < (2,7)):
    install_requires =['ordereddict', 'future']
else:
    install_requires = []

setup(
    name = 'crom',
    packages = ['crom'],
    include_package_data = True,
    package_data = {
        'crom': ['data/crm_vocab.tsv']
    },
    test_suite="tests",
    version = '0.0.3',
    description = 'A library for mapping CIDOC-CRM classes to Python objects',
    author = 'Getty Research Institute, Rob Sanderson',
    author_email = 'jgomez@getty.edu',
    url = 'https://github.com/gri-is/crom',
    install_requires=install_requires,
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: Apache License",
        "Development Status :: pre-Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
