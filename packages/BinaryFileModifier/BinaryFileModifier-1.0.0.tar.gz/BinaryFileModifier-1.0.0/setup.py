__author__ = "Rainer Schmitz <rainer.ch.franz87@gmail.com>"
__copyright__ = "Rainer Schmitz <rainer.ch.franz87@gmail.com>"
__version__ = "1.0.0"

from setuptools import setup, find_packages

setup(
    name='BinaryFileModifier',
    version='1.0.0',
    packages=find_packages(),
    description='The package changes the JavaScript signature in WebDrivers ChromeDriver',
    author='Rainer Schmitz',
    author_email='rainer.ch.franz87@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)