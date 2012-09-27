#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='django-kungfu',
    version='0.1',
    description=('A Flasky approach to distributed Django configuration'),
    long_description=open('README').read(),
    keywords='django settings overrides flasky',
    author='Ion Scerbatiuc',
    author_email='delinhabit@gmail.com',
    url='https://github.com/delinhabit/django-kungfu',
    license='BSD',
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks"
    ]
)