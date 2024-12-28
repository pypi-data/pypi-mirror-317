from setuptools import setup, find_packages

setup(
    name="opal_fetcher_dynamodb",
    version="0.1",
    description="Fetcher implementation for DynamoDB using OPAL framework for internal Informa usage.",
    author="Nikola Markovic",
    author_email="nikola.markovic@informa.com",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "boto3>=1.20.0",
        "pydantic>=1.8",
        "tenacity>=8.0.1",
        "botocore>=1.31.60",
        "opal-common",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    extras_require={
        "dev": ["pytest", "pytest-asyncio", "mypy", "black"],
    },
)
