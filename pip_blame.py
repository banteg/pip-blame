import importlib.metadata
import sys

import requests
from packaging.requirements import Requirement
from rich import print


def main():
    if len(sys.argv) < 2:
        print("usage: pip-blame NAME")
        return
    name = sys.argv[1]
    resp = requests.get(f"https://pypi.org/pypi/{name}/json")
    version = resp.json()["info"]["version"]
    print(f"[bold green]{name} v{version}")

    for dist in importlib.metadata.distributions():
        homepage = dist.metadata.get("Home-page")
        if dist.requires is None:
            continue
        for req in dist.requires:
            req = Requirement(req)
            if req.name != name:
                continue
            contains = req.specifier.contains(version)
            if not contains:
                color = "bold red"
            elif "<" in str(req.specifier):
                color = "yellow"
            else:
                color = "green"
            msg = f"[{color}]{dist.name}[/]"
            if not contains:
                msg += f" {homepage}/issues/new" if homepage else ""
            print(f"{msg}\n  {req}")


if __name__ == "__main__":
    main()
