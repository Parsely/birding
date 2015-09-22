#!/usr/bin/env python
"""Stream twitter searches using the public API.

Copyright 2015 Parsely, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import re
import sys

from setuptools import setup, find_packages


classifiers = [
    'Development Status :: 3 - Alpha',
    # TODO: 'Development Status :: 4 - Beta',
    # TODO: 'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    # TODO: 'Programming Language :: Python :: 3',
    # TODO: 'Programming Language :: Python :: 3.4',
    # TODO: 'Programming Language :: Python :: 3.5',
]

# Update virtualenvs/birding.txt when editing this list.
install_requires = [
    'elasticsearch==1.7.0',
    'pykafka==1.1.0',
    'pyyaml==3.11',
    'repoze.lru==0.6',
    'six==1.9.0',
    'streamparse==2.0.2',
    'travesty==0.1.1',
    'twitter==1.17.0',
]

lint_requires = [
    'pep8',
    'pyflakes',
]

tests_require = [
    'mock',
    'nose',
]

dependency_links = []

setup_requires = []

if 'nosetests' in sys.argv[1:]:
    setup_requires.extend(tests_require)


def get_version(filepath='src/birding/version.py'):
    """Get version without import, which avoids dependency issues."""
    with open(get_abspath(filepath)) as version_file:
        return re.search(
            r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""",
            version_file.read()).group('version')


def readme(filepath='README.rst'):
    """Return project README.rst contents as str."""
    with open(get_abspath(filepath)) as fd:
        return fd.read()


def description(doc=__doc__):
    """Return project description from first line of doc."""
    for line in doc.splitlines():
        return line.strip()


def get_abspath(filepath):
    if os.path.isabs(filepath):
        return filepath
    setup_py = os.path.abspath(__file__)
    project_dir = os.path.dirname(setup_py)
    return os.path.abspath(os.path.join(project_dir, filepath))


setup(
    name='birding',
    version=get_version(),
    author='Parsely, Inc.',
    author_email='hello@parsely.com',
    url='https://github.com/Parsely/birding',
    description=description(),
    long_description=readme(),
    license='Apache License 2.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [

        ]
    },
    install_requires=install_requires,
    tests_require=tests_require,
    setup_requires=setup_requires,
    extras_require={
        'test': tests_require,
        'all': install_requires + tests_require,
        'lint': lint_requires
    },
    dependency_links=dependency_links,
    zip_safe=False,
    test_suite='nose.collector',
    include_package_data=True,
)
