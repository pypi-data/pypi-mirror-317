# ruff: noqa: D100, D103

import shutil

import nox

nox.options.default_venv_backend = "uv"
nox.options.sessions = [
    "mypy",
    "ruff",
    "refactor",
    "interrogate",
    "pip_audit",
    "bandit",
    "pytest",
    "detect_secrets",
    "dependency_versions",
]


@nox.session(python=["3.11", "3.12"])  # 3.13 not yet supported by msgspec
def mypy(session):
    session.install("-e", ".")
    session.install("mypy", "types-toml", "types-aiofiles")
    session.run("mypy", "src/")


@nox.session
def ruff(session):
    session.install("ruff")
    session.run("ruff", "format", "src/")
    session.run("ruff", "check", "src/")


@nox.session
def refactor(session):
    session.install("codelimit")
    session.run("codelimit", "--version")
    session.run("codelimit", "check", "src")


@nox.session
def interrogate(session):
    session.install("interrogate", "setuptools")
    session.run("interrogate", "-vv", "src/")


@nox.session(python=["3.11", "3.12"])  # Python 3.13 not yet supported by msgpack
def pip_audit(session):
    session.install("pip-audit")
    session.run("pip-audit", "--version")
    session.run("pip-audit")


@nox.session
def bandit(session):
    session.install("bandit", "PyYAML", "tomli", "GitPython", "sarif-om", "jschema-to-python")
    session.run("bandit", "-r", "src/")


@nox.session(python=["3.11", "3.12"])  # Python 3.13 not yet supported by msgspec
def pytest(session):
    session.install("-e", ".")
    session.install("pytest-cov", "pytest-asyncio", "pytest-httpx")
    session.run("pytest", "-vv", "--cov-report", "term-missing", "--cov=lemmy2fedi", "tests")


@nox.session
def build_docs(session):
    session.install("-e", ".")
    session.install("Sphinx", "sphinx-rtd-theme")
    session.run("git", "branch", "--show-current", external=True)
    session.run("sphinx-build", "-M", "clean", "docs", "docs/_build")
    session.run("sphinx-build", "-M", "html", "docs", "docs/_build")
    session.run("git", "stash", external=True)
    session.run("git", "checkout", "pages", external=True)
    shutil.copytree(src="docs/_build/html", dst=".", dirs_exist_ok=True)
    session.run("git", "status", "--porcelain", "-uno", external=True)


@nox.session
def detect_secrets(session):
    session.install("detect-secrets")
    session.run("detect-secrets", "scan", "--baseline", ".secrets.baseline", ".")


@nox.session
def dependency_versions(session):
    session.install("git+https://codeberg.org/marvin8/dependency-checker.git")
    session.run("check")
