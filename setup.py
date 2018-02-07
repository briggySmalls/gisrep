#!/usr/bin/env python
import setuptools

# Ensure setuptools version is sufficient
assert setuptools.__version__ > '30.3'

# Run setup (configuration is in setup.cfg)
setuptools.setup()
