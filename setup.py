#!/usr/bin/python2
# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

version = '0.5.1'

with open("README.md", "r") as fh:
    long_description = fh.read()

if __name__ == '__main__':
    setup(
        name='aiocaldav',
        version=version,
        description="asynchronous CalDAV (RFC4791) client library",
        long_description=long_description,
        long_description_content_type="text/markdown",
        classifiers=["Development Status :: 4 - Beta",
                     "Intended Audience :: Developers",
                     "License :: OSI Approved :: GNU General "
                     "Public License (GPL)",
                     "License :: OSI Approved :: Apache Software License",
                     "Operating System :: OS Independent",
                     "Programming Language :: Python",
                     "Programming Language :: Python :: 3.6",
                     "Topic :: Office/Business :: Scheduling",
                     "Topic :: Software Development :: Libraries "
                     ":: Python Modules"],
        keywords='',
        author='Cyril Robert',
        author_email='cyril@hippie.io',
        maintainer='Thomas Chiroux',
        maintainer_email='thomas@chroux.com',
        url='https://github.com/ThomasChiroux/aiocaldav',
        license='GPL',
        packages=find_packages(exclude=['tests']),
        include_package_data=True,
        zip_safe=False,
        install_requires=['vobject', 'lxml', 'aiohttp', 'pytz'],
    )
