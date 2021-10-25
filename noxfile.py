import nox

nox.options.reuse_existing_virtualenvs = True
locations = ("api", "admin", "noxfile.py")


@nox.session
def black(session: nox.Session) -> None:
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@nox.session
def lint(session: nox.Session) -> None:
    args = session.posargs or locations
    session.install("flake8")
    session.run("flake8", *args)


@nox.session
def mypy(session: nox.Session) -> None:
    session.install("mypy")
    session.run(
        "mypy",
        "--disallow-untyped-defs",
        "--ignore-missing-imports",
        "api",
        "admin",
    )
