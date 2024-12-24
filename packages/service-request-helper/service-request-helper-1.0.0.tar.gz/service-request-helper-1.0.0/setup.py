from distutils.core import setup

from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    version='1.0.0',
    name='service-request-helper',
    packages=find_packages(exclude='test'),
    url='https://github.com/endpointuz/service-request-helper-lib',
    author='ksinn',
    author_email='ksinnd@gmail.com',
    description='Helper for client request to rest api',
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=[
        'pyhumps',
    ],
    extras_require={
        "sync": [
            "requests",
        ],
        "async": [
            "aiohttp",
        ],
    },
    setup_requires=['wheel'],
)
