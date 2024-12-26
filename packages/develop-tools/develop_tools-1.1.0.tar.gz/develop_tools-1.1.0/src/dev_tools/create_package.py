#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import sys
import os
import datetime
from typing import List, Dict

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s')
_LOGGER = logging.getLogger(__name__)


def _get_setup_text(package_name: str, your_name: str) -> str:

    setup_text = f"""
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('LICENSE') as f:
    lic = f.read()

setup(
    name='{package_name}',
    version='0.1.0',
    author='{your_name}',
    author_email='',
    description='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/javatechy/dokr",
    zip_safe=True,
    license=lic,
    packages=find_packages('src'),
    package_dir={{"": "src"}},
    include_package_data=True,
    entry_points={{
        "console_scripts":
            []
    }},
    install_requires=[

    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
"""
    return setup_text


def create_package_structure(folders: List[str], files: Dict[str, str]):

    # create folders
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

    # create files
    for file, value in files.items():
        with open(file, 'w') as datei:
            datei.write(value)


def generate_structure(path_target: str, project_name: str, package_name: str, your_name: str, *args, **kwargs):

    folders: List[str]
    files: Dict[str, str]
    setup_text: str

    datetime.datetime.now().year
    setup_text = _get_setup_text(package_name, your_name)
    # Ordner erstellen in path-Verzeichnis
    folders = [
        os.path.join(path_target, project_name),
        os.path.join(path_target, project_name, 'src'),
        os.path.join(path_target, project_name, 'src', package_name)
    ]
    _LOGGER.debug(f'Ordner: {folders}')

    files = {
        os.path.join(path_target, project_name, 'LICENSE'): f'Copyright (c) {datetime.datetime.now().year} {your_name}',
        os.path.join(path_target, project_name, 'MANIFEST.in'): 'graft src\n\ninclude LICENSE\ninclude README.rst\ninclude README.md\ninclude version.py',
        os.path.join(path_target, project_name, 'README.md'): 'description of ' + package_name,
        os.path.join(path_target, project_name, 'requirements.txt'): ' # to create a requirements.txt open "cmd" and navigate to your project repository and use command : "pip freeze > requirements.txt"',
        os.path.join(path_target, project_name, 'src', package_name, '__init__.py'): '',
        os.path.join(path_target, project_name, 'src', package_name, 'mein_scrip.py'): '',
        os.path.join(path_target, project_name, 'setup.py'): setup_text
    }
    _LOGGER.debug(f'Files: {files.keys}')

    create_package_structure(folders, files)


def _parse_args(raw_args):

    parser = argparse.ArgumentParser(
                        prog='package',
                        description='script creates a complete folder structure for the development of a package')
    parser.add_argument('path_target',
                        help='path to target directory where package is located')
    parser.add_argument('project_name',
                        help='')
    parser.add_argument('package_name',
                        help='')
    parser.add_argument('your_name',
                        help='')
    parser.add_argument('--debug',  # Activate debug mode
                        action='store_true',
                        help=argparse.SUPPRESS)
    args = parser.parse_args(raw_args)

    return args


def main(raw_args=None):  # pragma: no cover
    args = _parse_args(raw_args)

    if args.debug:
        _LOGGER.setLevel(logging.DEBUG)

    generate_structure(**vars(args))


if __name__ == '__main__':  # pragma: no cover
    main(sys.argv[1:])
