from setuptools import find_packages, setup


extras_test = (
    [
        "black",
        "flake8",
        "hypothesis",
        "isort",
        "mypy>=0.910",
        "pyproj",
        "pytest",
        "pytest-cov",
        "tox",
        "build"
    ]
)

setup(
    name="aiotx",
    keywords=[
        "cryptocurrency",
        "blockchain",
        "bitcoin",
        "ethereum",
        "asyncio",
        "aiohttp",
        "json-rpc",
        "payment",
        "wallet",
        "transaction",
    ],
    use_scm_version=True,
    description="An asynchronous library for interacting with various cryptocurrencies and blockchains",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    version="0.0.3",
    packages=find_packages(exclude=("tests", "scripts")),
    package_data={
        "aiotx": ["py.typed"],
    },
    setup_requires=[
        "setuptools_scm",
    ],
    install_requires=[
        "aiohttp",
    ],
    extras_require={
        "test": extras_test,
    },
    url="https://github.com/Grommash9/aiotx",
    author="Oleksandr Prudnikov",
    author_email="prudnikov21@icloud.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
