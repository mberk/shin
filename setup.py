from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="shin",
    version="0.0.2",
    description="Python implementation of Shin's method for calculating implied probabilities from bookmaker odds",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Maurice Berk",
    author_email="maurice@mauriceberk.com",
    url="https://github.com/mberk/shin",
    packages=["shin"],
    tests_require=["pytest"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
)
