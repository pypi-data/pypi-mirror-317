   # setup.py
from setuptools import setup, find_packages

setup(
       name='sysfunc',
       version='0.3',
       packages=find_packages(),
       include_package_data=True,
       description='A library for interacting with system functions',
       author='Hosne432',
       python_requires="==3.10.*",
       classifiers=[
           'Programming Language :: Python :: 3',
           'License :: OSI Approved :: MIT License',
           'Operating System :: OS Independent',
       ]
)