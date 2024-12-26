from setuptools import setup, find_packages

setup(
    name='file_scan_dd',
    version='1.1',
    packages=find_packages(),  # Use packages instead of py_modules
    install_requires=[
        'requests==2.26.0',
        'requests-toolbelt==0.9.1'
    ],
    description='A simple library to scan files using Metadefender',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)