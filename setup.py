from setuptools import setup, find_packages

setup(
    name='MsConnection',
    version='0.1.0',  # Change this as needed
    description='A package for managing connections to MS services',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Paul Volden',
    author_email='paul@mystore.no',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
