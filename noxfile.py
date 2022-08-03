import nox

ALL_PYTHONS = ["3.7", "3.8", "3.9"]

nox.options.sessions = ["lint", "tests", "doctests"]


@nox.session(reuse_venv=True)
def lint(session):
    """Run the linter."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", *session.posargs)


@nox.session(python=ALL_PYTHONS, reuse_venv=True)
def tests(session):
    """Run the unit and regular tests."""
    session.install(".[dev]")
    session.run("pytest", *session.posargs)


@nox.session(reuse_venv=True)
def doctests(session):
    """Run the doctests."""
    session.install(".[dev]")
    session.run("xdoctest", "./ocred/", *session.posargs)


@nox.session(reuse_venv=True)
def docs(session):
    """Build the docs. Pass "serve" to serve."""
    session.install("-e", ".[docs]")

    if session.posargs:
        if "serve" in session.posargs:
            print("Launching docs at http://localhost:8000/ - use Ctrl-C to quit")
            session.run("mkdocs", "serve")
        else:
            print("Unsupported argument to docs")
    else:
        session.run("mkdocs", "build")


@nox.session
def build(session):
    """Build an SDist and wheel."""
    session.install("build")
    session.run("python", "-m", "build")
