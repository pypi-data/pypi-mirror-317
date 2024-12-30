from setuptools import setup, find_packages
import os


setup(
    name='spinex_timeseries',
    version='0.1',
    packages=find_packages(),
    description='A Python package for SPINEX Anomaly',
    url='https://doi.org/10.1016/j.cie.2024.110812',
    long_description=open('README.md').read(),
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'scipy',
    ],
    python_requires='>=3.6',
)
