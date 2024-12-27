# Para Common Lib
Common Utilities Python library for Para Projects

## How to Package

Create the setup.py file

Before uploading to PyPI, you need a few tools to package and upload your project. Run these commands to install them:
```bash
pip install setuptools wheel twine
```
Build Your Package
```bash
python setup.py sdist bdist_wheel
```
This will create a dist/ folder that contains the files you need to upload to PyPI. Inside dist/, you should see files like my_package-0.1.0.tar.gz and my_package-0.1.0-py3-none-any.whl.


Upload Your Package to PyPI
```bash
twine upload dist/*
```

You can install the package with pip:

```bash
pip install my-package
```

Here's an example of how to use the package:
```bash
from my_package import authenticate
authenticate_user()
```
