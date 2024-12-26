from setuptools import setup, find_packages
from __init__ import __version__

setup(
    name='dbase3-py',
    version=__version__,
    description='A Python library to manipulate DBase III database files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Domingo E. Savoretti',
    author_email='esavoretti@gmail.com',
    url='https://github.com/sandy98/dbase3-py',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)