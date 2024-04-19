from importlib.metadata import Distribution, distributions, distribution
import sys

import requests
from packaging.requirements import Requirement
from rich import print
from dataclasses import dataclass


@dataclass
class Metadata:
    version: str
    requires: list[Requirement]

    @classmethod
    def from_pypi(cls, name: str):
        metadata = requests.get(f"https://pypi.org/pypi/{name}/json").json()
        return cls(
            version=metadata["info"]["version"],
            requires=[Requirement(req) for req in metadata["info"]["requires_dist"]],
        )

    @classmethod
    def from_dist(cls, dist: Distribution):
        return cls(
            version=dist.version,
            requires=[Requirement(req) for req in dist.requires or []],
        )

    def filter(self, dependency: str) -> list[Requirement]:
        return [req for req in self.requires if req.name == dependency]

    def contains(self, dependency, version) -> dict[Requirement, bool]:
        return {req: req.specifier.contains(version) for req in self.filter(dependency)}


def main():
    solution = []
    if len(sys.argv) < 2:
        print("usage: pip-blame NAME")
        return
    name = sys.argv[1]
    installed = distribution(name)
    latest = Metadata.from_pypi(name)
    print(f"[bold]{name} installed={installed.version} latest={latest.version}\n")

    for dist in distributions():
        installed_dist = Metadata.from_dist(dist)
        installed_contains = installed_dist.contains(name, latest.version)
        if not installed_contains:
            continue

        color = "red" if False in installed_contains.values() else "green"
        print(f"[{color}]{dist.name}[/] installed={dist.version}")
        for spec in installed_contains:
            print(f"  {spec}")
        print()

        if False in installed_contains.values():
            latest_dist = Metadata.from_pypi(dist.name)
            latest_contains = latest_dist.contains(name, latest.version)
            # implicit version comparison
            if False in latest_contains.values():
                homepage = dist.metadata.get("Home-page", "")
                if homepage.startswith("https://github.com"):
                    homepage += "/issues/new"
                print(
                    "[yellow]not fixed in the latest version, reach out to maintainers"
                )
                print(f"{homepage}\n")
                solution.append(homepage)
            else:
                print(
                    f"[green]{dist.name}[/] latest={latest_dist.version} [yellow]* upgrade to fix"
                )
                solution.append(f"pip install {dist.name}>={latest_dist.version}")
                for spec in latest_contains:
                    print(f"  {spec}")
                print()

    if solution:
        print("[yellow]suggested solution:")
        for sol in solution:
            print(sol)


if __name__ == "__main__":
    main()
