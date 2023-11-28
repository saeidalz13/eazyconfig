from setuptools import setup, find_packages

setup(
    name='eazyconfig',
    version='1.2.3',

    description='Easy configuration of input files for Air Quality department',
    long_description='A longer description of your package',

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
