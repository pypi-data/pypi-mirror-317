from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="crypto_cli_tool",
    version="0.0.3",
    author="Timur Gabaidulin",
    author_email="timur.gab@gmail.com",
    description="`crypto-cli-tool` is a simple and efficient command-line tool written in Python that allows you to quickly retrieve the latest prices of various cryptocurrencies. It fetches data from a reliable source and presents it in an easy-to-read format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/905timur/crypto-cli",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests",
        "fuzzywuzzy",
    ],
    entry_points={
        "console_scripts": [
            "crypto.cli=crypto.cli.tool:main",
        ],
    },
    keywords="cryptocurrency cli tool crypto price",
)
