from setuptools import setup, find_packages

setup(
    name='calculator_wxb',
    version='1.0.0',
    author='Chanke',
    author_email='yichan521@gmail.com',
    description='A simple package for calculating the sum of two numbers',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://www.example.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        # Add any dependencies here
    ],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    entry_points={
        'console_scripts': [
            'matrix_operations=matrix_operations.operations:main_function',
        ],
    },
)