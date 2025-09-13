from setuptools import setup

setup(
    name="selection",
    version="0.0.21",
    packages=["selection"],
    install_requires=[
        'lxml;platform_system!="Windows"',
        "six",
    ],
    extras_require={
        "pyquery": [
            'pyquery<=1.4.1; python_version < "3.0"',
            'pyquery; python_version >= "3.0"',
        ]
    },
)
