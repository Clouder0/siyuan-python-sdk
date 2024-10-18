import nox

all_supported_versions = ["3.9", "3.10", "3.11", "3.12", "3.13"]


@nox.session(python=all_supported_versions)
def check(session):
    project = nox.project.load_toml("pyproject.toml")
    deps = project["project"]["dependencies"]
    # dev_deps = project["tool"]["uv"]["dev-dependencies"]
    if len(deps) > 0:
        session.install(*deps)
    session.install("ruff")
    session.run("ruff", "check")


@nox.session(python=all_supported_versions)
def test(session):
    project = nox.project.load_toml("pyproject.toml")
    deps = project["project"]["dependencies"]
    if len(deps) > 0:
        session.install(*deps)
    session.install("pytest")
    session.run("pytest")
