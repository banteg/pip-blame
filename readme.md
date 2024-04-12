# pip-blame

*finds packages that prevent upgrading a transitive dependency*

## install

```
pip install pip-blame
```

### usage

```
pip-blame NAME
```

it will fetch the latest version of the package from pypi and compare it against the requirement specifiers declared by the installed packages.

then it will highlight the dependencies that need relaxing their requirements, as well as provide links to open new issues where repo links can be found in the metadata.
