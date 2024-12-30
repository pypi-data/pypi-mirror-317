from setuptools import setup

setup(
    name='termux-select',
    version='0.1',
    py_modules=['select_item'],
    description='A simple script to select items',  # A brief description
    long_description=open('README.md').read(),  # Optional: detailed description from README.md
    long_description_content_type='text/markdown',  # The format of the long description
    author='Sakib Salim',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Adjust the license
        'Programming Language :: Python :: 3.8',  # Specify the Python version compatibility
    ],
)
