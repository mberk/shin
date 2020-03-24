from setuptools import setup

setup(
    name='shin',
    version='0.0.1',
    description='Python implementation of Shin\'s method for calculating implied probabilities from bookmaker odds',
    author='Maurice Berk',
    author_email='maurice@mauriceberk.com',
    url='https://github.com/mberk/shin',
    packages=['shin'],
    tests_require=['pytest']
)
