import os
from setuptools import find_packages
from distutils.core import setup
from glob import glob


install_requires = [
    'xarray>=2025.9.1',
    'scipy>=1.16.2',
    'h5netcdf>=1.6.4',
    'python-irodsclient>=3.2.0',
]


setup(
    name='xarray-irods',
    version='0.1',
    description=('xarray-irods allows you to read files directly from iRODS platforms using xarray functions'),
    url='https://github.com/w-lampaert/xarray-irods',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.9',
    install_requires=install_requires,
)
