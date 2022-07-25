from setuptools import setup

extras = {
    "test": [
        "coverage>=1",  # migrate to pytest and pytest-cov
        "xdoctest>=1.0.0",
    ],
    # "docs": [
    # ],
}

extras["dev"] = [
    # *extras["docs"],
    *extras["test"],
]

setup(extras_require=extras)
