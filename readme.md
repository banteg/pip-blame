# pip-blame

*finds packages that prevent upgrading a transitive dependency*

<img width="369" alt="pip-blame" src="https://github.com/banteg/pip-blame/assets/4562643/4981ca69-4952-4583-97c3-07dd7e93bed5">

## install

```
pip install pip-blame
```

## usage

```
pip-blame NAME
```

it will fetch the latest version of the package from pypi and compare it against the requirement specifiers declared by the installed packages.

then it will highlight the dependencies that need relaxing their requirements, as well as provide links to open new issues where repo links can be found in the metadata.

## philosophy

**when making a library, prefer `>=` specifiers for requirements.**

capping dependencies scales poorly when you build a project with dependencies by multiple maintainers. everyone has been through the dependency hell. 

**every person has a different understanding of semver.**

you simply cannot predict that your library breaks with a patch release from a change so small it didn't make it to the changelog, or that it would still function with the next major release.

**swim upstream to freshness.**

not capping requirements allows you to find out when things break earlier and keep the requirements fresh.
people who rely on your work as a building block will be thankful as they spend less time pulling their hair.

**overrides as a last resort.**

if you struggle with a transitive dependency, use [depencency overrides](https://github.com/astral-sh/uv?tab=readme-ov-file#dependency-overrides) feature of `uv`. it allows you to lie to the resolver and install the version you know that works.
