from setuptools import setup, find_packages
from excel_97 import __version__

setup(
    name='excel97_py',
    version=__version__,
    description='A Python library to manipulate Excel 97/2003 spreadsheet files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Domingo E. Savoretti',
    author_email='esavoretti@gmail.com',
    url='https://github.com/sandy98/dbase3-py',
    packages=find_packages(),
    # py_modules=['dbase3'],  # Asegúrate de incluir el módulo aquí
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)