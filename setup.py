"""Python package definition

Attributes:
    README_FILE (str): File path of project readme
    VERSION (str): Project version number
"""
from os import path
from setuptools import setup, find_packages


# Get the long description from the README file
README_FILE = path.join(path.abspath(path.dirname(__file__)), 'README.rst')
with open(README_FILE, encoding='utf-8') as file:
    long_description = file.read()

VERSION = '0.0.1'

setup(
    name='gisrep',
    version=VERSION,
    description="The command line Github issues reporter",
    long_description=long_description,
    url="https://github.com/briggySmalls/gisrep",
    download_url=(
        "https://github.com/briggySmalls/gisrep/archive/"
        "{}.tar.gz".format(VERSION)),
    author="Sam Briggs",
    author_email="briggySmalls90@gmail.com",
    license="GPLv3",
    classifiers=[
        # Audience
        "Intended Audience :: Developers",

        # Licence
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",

        # Python versions
        "Programming Language :: Python :: 3",

        # Topics
        "Topic :: Software Development :: Bug Tracking",
        "Topic :: Software Development :: Documentation",
    ],
    keywords=(
        "Github issues tracker reports reporting documentation release"
        "note publish"),
    install_requires=[
        'toml',
        'jinja2',
        'PyGithub',
        'keyring',
        'pyperclip',
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': ['gisrep=gisrep.gisrep:main']
    },
    python_requires='>=3.4',
)
