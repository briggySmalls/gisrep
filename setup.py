from setuptools import setup, find_packages

setup(
    name='gisrep',
    version='0.1.0',
    description="Tool for publishing Github issues",
    # TODO: Add long_description
    url="https://github.com/briggySmalls/issues-reporter",
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
    keywords="Github development issues reports documentation release note",
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
    python_requires='>=3',
)
