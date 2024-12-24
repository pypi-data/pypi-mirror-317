from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="apitoolkit-fastapi",
    version="2.0.0",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email='hello@apitoolkit.io',
    author='APIToolkit',
    install_requires=[
        'fastapi',
        'apitoolkit-common',
        "opentelemetry-api>=1.0.0",
    ]
)
