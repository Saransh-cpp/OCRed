# Contributing guide

If you are planning to develop `OCRed`, or want to use the latest commit of `OCRed` on your local machine, you might want to install it from the source. This installation is not recommended for users who want to use the stable version of `OCRed`. The steps below describe the installation process of `OCRed`'s latest commit. It also describes how to test `OCRed`'s codebase and build `OCRed`'s documentation.

**Note**: `OCRed` uses [Scikit-HEP's developer information](https://scikit-hep.org/developer) as a reference for all the development work. The guide is a general and much more explained collection of documentation available for developing `Scikit-HEP` packages. `OCRed` is not a `Scikit-HEP` package, but it still loosely follows this developer guide as it is absolutely amazing!

## Installing OCRed

We recommend using a virtual environment to install `OCRed`. This would isolate the library from your global `Python` environment, which would be beneficial for reproducing bugs, and the overall development of `OCRed`. The first step would be to clone `OCRed` -

```
git clone https://github.com/Scikit-hep/OCRed.git
```

and then we can change the current working directory and enter `OCRed` -

```
cd OCRed
```

### Creating a virtual environment

A virtual environment can be set up and activated using `venv` in both `UNIX` and `Windows` systems.

**UNIX**:

```
python3 -m venv .env
. .env/bin/activate
```

**Windows**:

```
python -m venv .env
.env\bin\activate
```

### Installation

The developer installation of `OCRed` comes with a lot of options -

- `test`: the test dependencies
- `docs`: extra dependencies to build and develop `OCRed`'s documentation
- `dev`: installs the `test` and `docs` dependencies

These options can be used with `pip` with the editable (`-e`) mode of installation in the following ways -

```
pip install -e .[dev,test]
```

For example, if you want to install the `docs` dependencies along with the dependencies included above, use -

```
pip install -e .[dev,test,docs]
```

### Adding OCRed for notebooks

`OCRed` can be added to the notebooks using the following commands -

```
python -m ipykernel install --user --name ocred
```

## Activating pre-commit

`OCRed` uses a set of `pre-commit` hooks and the `pre-commit` bot to format, type-check, and prettify the codebase. The hooks can be installed locally using -

```
pre-commit install
```

This would run the checks every time a commit is created locally. The checks will only run on the files modified by that commit, but the checks can be triggered for all the files using -

```
pre-commit run --all-files
```

If you would like to skip the failing checks and push the code for further discussion, use the `--no-verify` option with `git commit`.

## Testing OCRed

`OCRed` is tested with `pytest` and `xdoctest`. `pytest` is responsible for testing the code, whose configuration is available in [pyproject.toml](https://github.com/Saransh-cpp/OCRed/blob/main/pyproject.toml), and on the other hand, `xdoctest` is responsible for testing the examples available in every docstring, which prevents them from going stale. Additionally, `OCRed` also uses `pytest-cov` to calculate the coverage of these unit tests.

### Running tests locally

The tests can be executed using the `test` dependencies of `OCRed` in the following way -

```
python -m pytest -ra
```

### Running tests with coverage locally

The coverage value can be obtained while running the tests using `pytest-cov` in the following way -

```
python -m pytest -ra --cov=ocred tests/
```

### Running doctests

The doctests can be executed using the `test` dependencies of `OCRed` in the following way -

```
xdoctest ./src/ocred/
```

A much more detailed guide on testing with `pytest` is available [here](https://scikit-hep.org/developer/pytest).

## Documenting OCRed

`OCRed`'s documentation is mainly written in the form of [docstrings](https://peps.python.org/pep-0257/) and [Markdown](https://en.wikipedia.org/wiki/Markdown). The docstrings include the description, arguments, examples, return values, and attributes of a class or a function, and the `.md` files enable us to render this documentation on `OCRed`'s documentation website.

`OCRed` primarily uses [MkDocs](https://www.mkdocs.org/) and [mkdocstrings](https://mkdocstrings.github.io/) for rendering documentation on its website. The configuration file (`mkdocs.yml`) for `MkDocs` can be found [here](https://github.com/Saransh-cpp/OCRed/blob/main/mkdocs.yml). The documentation is deployed on <https://readthedocs.io> [here](https://ocred.readthedocs.io/en/latest/).

Ideally, with the addition of every new feature to `OCRed`, documentation should be added using comments, docstrings, and `.md` files.

### Building documentation locally

The documentation is located in the `docs` folder of the main repository. This documentation can be generated using the `docs` dependencies of `OCRed` in the following way -

```
mkdocs serve
```

The commands executed above will clean any existing documentation build, create a new build (in `./site/`), and serve it on your `localhost`. To just build the documentation, use -

```
mkdocs build
```

## Nox

`OCRed` supports running various critical commands using [nox](https://github.com/wntrblm/nox) to make them less intimidating for new developers. All of these commands (or sessions in the language of `nox`) - `lint`, `tests`, `doctests`, `docs`, and `build` - are defined in [noxfile.py](https://github.com/Saransh-cpp/OCRed/blob/main/noxfile.py).

`nox` can be installed via `pip` using -

```
pip install nox
```

The default sessions (`lint`, `tests`, and `doctests`) can be executed
using -

```
nox
```

### Running pre-commit with nox

The `pre-commit` hooks can be run with `nox` in the following way -

```
nox -s lint
```

### Running tests with nox

Tests can be run with `nox` in the following way -

```
nox -s tests
```

### Building documentation with nox

Docs can be built with `nox` in the following way -

```
nox -s docs
```

Use the following command if you want to deploy the docs on `localhost` -

```
nox -s docs -- serve
```
