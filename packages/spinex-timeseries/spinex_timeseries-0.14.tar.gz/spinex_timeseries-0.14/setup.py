from setuptools import setup, find_packages
import os


setup(
    name='spinex_timeseries',
    version='0.14',
    packages=find_packages(),
    description='A Python package for Timeseries',
    url='https://doi.org/10.1016/j.cie.2024.110812',
    long_description=open('README.md').read(),
    install_requires=[
        'numpy>=1.26.4',
        'pandas>=2.2.2',
        'scikit-learn>=1.6.0',
        'scipy>=1.14.1',
        'matplotlib>=3.0.0',
        'numba>=0.57.1',
        'seaborn>=0.11.0',
        'statsmodels>=0.13.0',
    ],
    python_requires='>=3.6',
)
