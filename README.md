[![](https://img.shields.io/badge/released-2021.6.4-green.svg?longCache=True)](https://pypi.org/project/setuppy/)
[![](https://img.shields.io/badge/license-Unlicense-blue.svg?longCache=True)](https://unlicense.org/)

### Installation
```bash
$ pip install setuppy
```

### How it works
+   environment variables `SETUPPY_KEY`
+   attrs
+   methods `get_key`

##### default methods
method|value
-|-
`get_install_requires`|`requirements.txt` lines
`get_name`|`os.path.basename(os.getcwd()).split('.')[0]`
`get_packages`|`setuptools.find_packages()`
`get_scripts`|`bin/` or `scripts/` files

### Examples
```bash
$ cd path/to/project
$ export SETUPPY_VERSION="42"
$ python -m setuppy > setup.py
```

`setup.py`
```python
setup(
    name='project',
    version='42',
    install_requires=[
        ...
    ],
    packages=[
        ...
    ]
)
```




subclassing
```python
from setuppy import SetupPy

class MySetupPy(SetupPy):
    def get_scripts(self):
        ...

print(MySetupPy(version="42"))
```

