from setuptools import setup, find_packages
import os

# Read long description from README file
long_description = ""
try:
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "A detailed description of the package is missing."

setup(
    name='para_api_security',              # Name of your package
    version='0.0.6',                       # Version of your package
    packages=find_packages(),              # Automatically find all packages in the directory
    install_requires=[                     # List dependencies here
        'python-dotenv',                   # Example dependency
    ],
    author='Hussein Habhab',               # Author of the package
    author_email='hussein.habhab@dar.com', # Author email
    description='Common Package to authenticate APIs',
    long_description=long_description,     # Read the long description from the README file
    long_description_content_type='text/markdown',  # Set content type for markdown
    url='https://github.com/paratwin/para_be_common_lib',  # URL to your repo
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)