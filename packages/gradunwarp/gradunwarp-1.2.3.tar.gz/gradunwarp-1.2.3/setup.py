"""Setup gradunwarp

Most configuration is now in pyproject.toml. This file configures
extensions and a legacy script.
"""
from setuptools import setup

setup(
    scripts=['gradunwarp/core/gradient_unwarp.py'],
)
