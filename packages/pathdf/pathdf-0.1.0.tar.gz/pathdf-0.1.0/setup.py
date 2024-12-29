from setuptools import setup, find_packages

setup(
    name='pathdf',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'openpyxl',  # Required for Excel support
    ],
    entry_points={
        'console_scripts': [
            'pathdf=pathdf.pathdf:pathdf',
        ],
    },
    author='Dr.Majeed Jamakhani',
    author_email='mjbioinfo@gmail.com',
    description='A package to export file paths to various formats like csv or dataframe',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MJBioInfo/pathdf',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)