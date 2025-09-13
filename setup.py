from setuptools import setup

setup(
    name="selection",
    version="0.0.21",
    packages=["selection"],
    install_requires=[
        "six",
        'pyquery<=1.4.3; python_version < "3.0"',
        'pyquery; python_version >= "3.0"',
    ],
)
