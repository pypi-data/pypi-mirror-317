from setuptools import setup, find_packages

VERSION = '0.1.0'
DESCRIPTION = 'Barcode rectifier'
LONG_DESCRIPTION = 'MIPT 2024 4th semester fall project module: barcode rectifier'

setup(
        name="mipt2024f_4_barrect",
        version=VERSION,
        author="Alexander Koshelev",
        author_email="alexander.y.koshelev@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],

        license="LGPL",

        keywords=['python', 'rectification'],

        classifiers= [
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3"
        ]
)
