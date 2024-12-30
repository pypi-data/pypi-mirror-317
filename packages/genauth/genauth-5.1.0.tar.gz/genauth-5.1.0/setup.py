# coding: utf-8

import io
import os
import re
from setuptools import setup, find_packages


def find_version():
    file_dir = os.path.dirname(__file__)
    with io.open(os.path.join(file_dir, 'genauth', 'version.py')) as f:
        version = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', f.read())
        if version:
            return version.group(1)
        else:
            raise RuntimeError("Unable to find version string.")


with io.open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='genauth',
    version=find_version(),
    description="Python SDK for GenAuth",  # description
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='GenAuth sso AaaS IdaaS',
    author='GenAuth',  # author
    author_email='dev@genauth.ai',  # author email
    maintainer='GenAuth',
    maintainer_email='dev@genauth.ai',
    url='https://github.com/GenAuth-Official/genauth-py-sdk',  # author link
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    install_requires=[
        'requests',
        'pyjwt'
    ]
)
