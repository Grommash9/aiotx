from setuptools import find_packages, setup


extras_test = (
    [
        "hypothesis",
        "ruff",
        "pyproj",
        "pytest",
        "pytest-cov",
        "sphinx",
        "pytest-asyncio",
        "tox",
        "build",
        "vcrpy"
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
    packages=find_packages(exclude=("tests", "scripts", "examples", "docs")),
    package_data={
        "aiotx": ["py.typed"],
        "aiotx.utils": ["*.json"],
    },
    setup_requires=[
        "setuptools_scm",
    ],
    install_requires=[
        "aiohttp",
        "eth_keys==0.5.*",
        "eth_utils==4.1.*",
        "eth_account==0.13.*",
        "sqlalchemy",
        "aiosqlite",
        "aiomysql",
        "cryptography",
        "bitcoinlib==0.6.*",
        "greenlet",
        "setuptools",
        "pynacl>=1.4.0",
        "tronpy",
    ],
    extras_require={
        "test": extras_test,
    },
    url="https://github.com/Grommash9/aiotx",
    project_urls={
        'Documentation': 'https://grommash9.github.io/aiotx/',
        'Source': 'https://github.com/Grommash9/aiotx'
        },
    author="Oleksandr Prudnikov",
    author_email="prudnikov21@icloud.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
