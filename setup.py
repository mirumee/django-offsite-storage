#! /usr/bin/env python
from setuptools import setup, find_packages


setup(
    name='django-offsite-storage',
    author='Mirumee Software',
    author_email='hello@mirumee.com',
    description="Cloud static and media file storage suitable for app containers",
    license='MIT',
    version='0.0.5',
    url='https://github.com/mirumee/django-offsite-storage',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'boto>=2.36.0',
        'Django>=1.7',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe=False
)
