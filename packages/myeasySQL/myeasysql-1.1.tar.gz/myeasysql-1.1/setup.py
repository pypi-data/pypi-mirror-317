from setuptools import setup, find_packages

setup(
    name='myeasySQL',
    version='1.1',
    packages=find_packages(),
    install_requires=['mysql-connector-python']
)