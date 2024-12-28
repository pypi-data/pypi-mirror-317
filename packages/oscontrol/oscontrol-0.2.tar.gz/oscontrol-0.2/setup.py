   # setup.py
from setuptools import setup, find_packages

setup(
       name='oscontrol',
       version='0.2',
       packages=find_packages(),
       include_package_data=True,
       description='A library for interacting with subsystems.',
       author='Queezy52',
       classifiers=[
           'Programming Language :: Python :: 3',
           'License :: OSI Approved :: MIT License',
           'Operating System :: OS Independent',
       ],
       python_requires='>=3.6',
)