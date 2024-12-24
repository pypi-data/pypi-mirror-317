# AWMT_BasicPythonPackage
Template for creating PyPI hosted python packages

This repo is intended to be used as a template for new AWMT python projects 

## Release Notes

For detailed release notes see:

[Releases Page](https://github.com/andowt/AWMT_BasicPythonPackage/releases)


## Manual Buildling Instructiibs

### Build Tools
Poetry was selected based on this article suggesting it has the best support and is most widely adopted:

https://www.pyopensci.org/python-package-guide/package-structure-code/python-package-build-tools.html

Repo structure has been adopted from Poetry docs here:

https://python-poetry.org/docs/basic-usage/#project-setup

Poetry can be installed as documented here:

https://python-poetry.org/docs/#installation

### Unit tests
Pytest has been chosen for unit testing based on its scalability and flexability for different applications - see here for more: https://builtin.com/data-science/pytest-vs-unittest

pytest can be installed using

```
pip install pytest
```

### Uploading to PyPI
Install twine using

```
pip install twine
```

Run the command

```
poetry build
```

Test upload to PyPI

```
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```


Test install from PyPI

```
pip install -i https://test.pypi.org/simple/ AWMT_BasicPythonPackage
```

Full Upload to PyPI

```
twine upload dist/*
```

View Project

```
https://pypi.org/project/<package_name>
```

Full install

```
pip install <package_name>
```

## Tokens

For the automated pull requests to create releases a token called "PAT_PUSH_TOKEN" is required.

This can be generated under https://github.com/settings/personal-access and should have Read and Write access to code and pull requests as well as Read access to metadata

PAT_PUSH_TOKEN should be added to the repo under secrets.

For uploading to PyPI and API kep is needed

This can be generated through your PyPI settings and should be added to the repo secrets as PYPI_API_TOKEN


