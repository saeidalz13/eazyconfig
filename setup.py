from setuptools import setup, find_packages
from eazyconfig.constants import VERSION
from pathlib import Path


setup(
    name='eazyconfig',
    version=f'v{VERSION}',

    description='Easy configuration of input files for Air Quality department',
    long_description=Path("README.md").read_text(),

    author='Saeid Alizadeh',
    author_email='saeidalz96@gmail.com',

    url='',

    keywords=['python', 'package', 'eazyconfig', 'AQ'],

    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.11',
    ],

    packages=find_packages(),
    install_requires=[
        "configparser==6.0.0",
        "colorama==0.4.6",
    ],

    zip_safe=False,
    python_requires='>=3.11',
    include_package_data=True
    
)
