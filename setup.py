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
    long_description_content_type='text/x-rst',
    author='David Jean Louis',
    author_email='izimobil@gmail.com',
    url=repo_url,
    packages=find_packages(exclude=['test_proj*']),
    include_package_data=True,
    license='MIT License',
    python_requires='>=3.9',
    install_requires=['Django>=4.2'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Framework :: Django',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.2',
        'Framework :: Django :: 6.0',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe=False,
)
