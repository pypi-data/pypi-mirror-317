# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README 2.0.0.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="cleantweet",
    version="2.0.1",
    description="a python library to clean textual data fetched from API's",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://cleantweet.org/",
    author="Lare Adeola",
    author_email="lare@cleantweet.org",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=["nltk", "pandas", "matplotlib", "wordcloud"]
)
