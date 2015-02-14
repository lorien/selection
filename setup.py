from setuptools import setup, find_packages

"""
with open('selection/version.py') as f:
    code = compile(f.read(), 'version.py', 'exec')
    exec(code, None, None)
"""

setup(
    name = 'selection',
    version = '0.0.6',
    description = 'API to extract content from HTML & XML documents',
    author = 'Gregory Petukhov',
    author_email = 'lorien@lorien.name',
    install_requires = ['lxml', 'tools', 'six'],
    packages = ['selection', 'selection.backend', 'script', 'test'],
    license = "MIT",
    classifiers = (
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
)
