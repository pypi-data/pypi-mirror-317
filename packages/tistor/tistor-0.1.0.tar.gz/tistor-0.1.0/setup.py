from setuptools import setup, find_packages

setup(
    name='tistor',
    version='0.1.0',
    author='nicecode',
    author_email='akash.verma1076@gmail.com',
    description='A simple calculator package for arithmetic operations.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/akash-verma998/calculator',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)