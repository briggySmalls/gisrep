"""Python package definition
"""
from setuptools import setup, find_packages


setup(
    name='gisrep',
    version='0.1.0',
    description="The command line Github issues reporter",
    url="https://github.com/briggySmalls/gisrep",
    download_url='https://github.com/briggySmalls/gisrep/archive/0.1.0.tar.gz',
    author="Sam Briggs",
    licence="GPLv3",
    classifiers=[
        # Development status
        "Development Status :: 2 - Pre-Alpha",

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
    entry_points={
        'console_scripts': ['gisrep=gisrep.gisrep:main']
    },
    python_requires='>=3.4',
)
