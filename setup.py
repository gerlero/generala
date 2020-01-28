#!/usr/bin/env python

from setuptools import setup, find_packages

classifiers = ('Development Status :: 5 - Production/Stable',
               'Intended Audience :: Developers',
               'Intended Audience :: Education',
               'Intended Audience :: End Users/Desktop',
               'License :: OSI Approved :: MIT License',
               'Programming Language :: Python',
               'Programming Language :: Python :: 3',
               'Programming Language :: Python :: 3.5',
               'Programming Language :: Python :: 3.6',
               'Programming Language :: Python :: 3.7',
               'Programming Language :: Python :: 3.8',
               'Topic :: Games/Entertainment',
               'Topic :: Software Development :: Libraries',
               'Operating System :: OS Independent')

with open("README.md", 'r') as fh:
    long_description = fh.read()

setup(
    name='generala',
    version='1.0.1',
    author="Gabriel Gerlero",
    description="Maximize your score in a turn of the Generala dice game",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/gerlero/generala",
    project_urls={
        "Bug Tracker": "https://github.com/gerlero/generala/issues",
        "Source Code": "https://github.com/gerlero/generala",
    },
    packages=find_packages(),
    entry_points = {
        'console_scripts': ('generala=generala.__main__:main'),
    },
    license='MIT',
    classifiers=classifiers,
    python_requires='>=3.5'
)