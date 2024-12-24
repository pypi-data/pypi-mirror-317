import pathlib
from setuptools import setup, find_packages  # Corrected import statement

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="kubemq",
    version="3.4.2",
    description="KubeMQ SDK for Python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/kubemq-io/kubemq-Python",
    author="KubeMQ",
    author_email="info@kubemq.io",
    license="MIT",
    packages=find_packages(),  # Corrected function call
    install_requires=[
        "grpcio>=1.68.1",
        "protobuf>=5.29.2",
        "setuptools>=75.6.0",
        "PyJWT>=2.10.1",
        "pydantic>=2.10.4",
    ],
    zip_safe=False,
)
