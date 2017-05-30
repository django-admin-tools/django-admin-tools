#!/usr/bin/env python

from setuptools import setup, find_packages
from admin_tools import VERSION

repo_url = 'https://github.com/django-admin-tools/django-admin-tools'
long_desc = '''
%s

%s
''' % (open('README.rst').read(), open('CHANGELOG').read())

setup(
    name='django-admin-tools',
    version=VERSION.replace(' ', '-'),
    description='A collection of tools for the django administration interface',
    long_description=long_desc,
    author='David Jean Louis',
    author_email='izimobil@gmail.com',
    url=repo_url,
    download_url='https://pypi.python.org/packages/source/d/django-admin-tools/django-admin-tools-%s.tar.gz' % VERSION,
    packages=find_packages(exclude=['test_proj*']),
    include_package_data=True,
    license='MIT License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe=False,
)
