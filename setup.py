import os
import re

from setuptools import setup

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                       "aiocopr", "__init__.py"), "r") as fp:
    try:
        version = re.findall(r'^__version__ = "([^"]+)"\r?$', fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError("Unable to determine version.")

args = dict(
    name="aiocopr",
    version=version,
    description="COPR client for asyncio",
    author="Igor Gnatenko",
    author_email="ignatenko@redhat.com",
    url="https://github.com/ignatenkobrain/aiocopr",
    license="GPL-3.0+",
    packages=["aiocopr"],
    install_requires=["aiohttp"])

setup(**args)
