from setuptools import setup, find_packages

setup(
    name = 'selection',
    version = '0.0.13',
    description = 'API to extract content from HTML & XML documents',
    author = 'Gregory Petukhov',
    author_email = 'lorien@lorien.name',
    install_requires = [
        'lxml;platform_system!="Windows"',
        'weblib',
        'six',
    ],
    packages = find_packages(exclude=['test']),
    license = "MIT",
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
