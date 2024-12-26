from os import sep

from typer import Exit

from start.cli import params as _p
from start.core.dependency import DependencyManager
from start.core.pip_manager import PipManager
from start.logger import Detail, Error, Info, Success, Warn
from start.utils import ensure_path


def show(packages: _p.Packages):
    """Show information about installed packages."""
    pip = PipManager()
    pip.execute(["show", *(packages or [])])
    if pip.stdout:
        Detail("\n".join(pip.stdout))
    if pip.stderr:
        Error("\n".join(pip.stderr))


def list_packages(tree: _p.Tree = False, group: _p.Group = "", dependency: _p.Dependency = ""):
    """Display all installed packages."""

    pip = PipManager()

    status = ""
    if dependency:
        if not (config_path := ensure_path(dependency)):
            Error(f"Dependency file {dependency} not found")
            raise Exit(1)
        status = f"({group}-Dependencies)" if group else "(Dependencies)"
        dm = DependencyManager(config_path)
        packages = [dep.name for dep in dm.packages(group)]
    else:
        packages = pip.execute(["list"]).parse_list_output()

    if not packages:
        Warn("No packages found")
        raise Exit(1)

    if not tree:
        Info(f"Installed{status} packages:")
        Detail("\n".join("- " + package for package in packages))
        raise Exit(0)

    analyzed_packages = pip.analyze_packages_require(*packages)
    Success("Analysis for installed packages:")

    Info(pip.execu.split(sep)[-4] + status if sep in pip.execu else pip.execu)

    installed_packages = set(packages)
    for i, package in enumerate(analyzed_packages):
        name, dependencies = list(package.items())[0]
        for branch, tree_string in pip.generate_dependency_tree(
            name, dependencies, i == len(analyzed_packages) - 1
        ):
            Status = Detail if branch in installed_packages else Warn
            Detail(tree_string + Status(branch, display=False))
