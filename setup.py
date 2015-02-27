#! /usr/bin/env python
from setuptools import setup, find_packages


setup(
    name='django-offsite-storage',
    author='Mirumee Software',
    author_email='hello@mirumee.com',
    description="Cloud static and media file storage suitable for app containers",
    license='MIT',
    version='0.0.1',
    url='https://github.com/mirumee/django-offsite-storage',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'boto>=2.36.0',
        'Django>=1.7',
    ],
    zip_safe=False
)
