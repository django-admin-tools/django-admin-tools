#!/usr/bin/env python
import os
import sys
from setuptools import setup, find_packages
from admin_tools import VERSION


repo_url = 'https://github.com/django-admin-tools/django-admin-tools'
long_desc = '''
%s

%s
''' % (open('README.rst').read(), open('CHANGELOG').read())


if sys.argv[-1] == 'publish':
    cmd = "rm -rf dist && {0} -m build && {0} -m twine upload dist/*"
    if os.system(cmd.format(sys.executable)) != 0:
        sys.exit("Publish failed.")
    print("You probably want to also tag the version now:")
    print("  git tag -a {0} -m 'version {0}'".format(VERSION))
    print("  git push --tags")
    sys.exit()


setup(
    name='django-admin-tools',
    version=VERSION.replace(' ', '-'),
    description='A collection of tools for the django administration interface',
    long_description=long_desc,
    long_description_content_type='text/x-rst',
    author='David Jean Louis',
    author_email='izimobil@gmail.com',
    url=repo_url,
    download_url='https://pypi.python.org/packages/source/d/django-admin-tools/django-admin-tools-%s.tar.gz' % VERSION,
    packages=find_packages(exclude=['test_proj*']),
    include_package_data=True,
    license='MIT License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Programming Language :: Python :: 3.15',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Framework :: Django :: 5.1',
        'Framework :: Django :: 5.2',
        'Framework :: Django :: 6.0',
        'Framework :: Django :: 6.1',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe=False,
)
