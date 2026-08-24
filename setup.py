from setuptools import setup, find_packages

setup(
    name="fitos",
    version="0.2.11",
    packages=["fitos"],
    install_requires=[
        'Werkzeug',
        'pandas',
        'scikit-learn',
    ]
)