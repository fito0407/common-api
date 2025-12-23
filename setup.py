from setuptools import setup, find_packages

setup(
    name="fitos",
    version="0.2.1",
    packages=["fitos"],
    install_requires=[
        'Werkzeug',
        'pandas'
    ]
)