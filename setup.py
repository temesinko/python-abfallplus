#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

cwd = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(cwd, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

if __name__ == '__main__':
    setup(
        name='abfallplus',
        version='0.1.3',
        description='A Python wrapper for the Abfall+ API',
        long_description=long_description,
        long_description_content_type='text/markdown',
        author='Jan Temešinko',
        author_email='jan+github@temesinko.de',
        maintainer='Jan Temešinko',
        maintainer_email='jan+github@temesinko.de',
        url='https://github.com/temesinko/python-abfallplus',
        license='MIT License',
        packages=find_packages(exclude='tests'),
        platforms=['Any'],
        install_requires=[
            'requests',
            'beautifulsoup4',
        ],
        setup_requires=[
            'setuptools>=46.0.0',
            'pytest-runner',
        ],
        tests_require=[
            'pytest',
            'responses'
        ],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ]
    )
