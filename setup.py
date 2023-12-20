from setuptools import setup, find_packages

setup(
    name='eazyconfig',
    version='1.3.3',

    description='Easy configuration of input files for Air Quality department',
    long_description='To faciliate the configuration an engineering project. It includes modules for reading config files, logging functions, etc.',

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
)
