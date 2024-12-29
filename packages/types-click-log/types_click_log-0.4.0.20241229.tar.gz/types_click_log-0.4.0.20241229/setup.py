from setuptools import setup

name = "types-click-log"
description = "Typing stubs for click-log"
long_description = '''
## Typing stubs for click-log

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`click-log`](https://github.com/click-contrib/click-log) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `click-log`. This version of
`types-click-log` aims to provide accurate annotations for
`click-log==0.4.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/click-log`](https://github.com/python/typeshed/tree/main/stubs/click-log)
directory.

This package was tested with
mypy 1.14.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`2cdda12df78275b98a5d3cdc8a92f93d596d9d5d`](https://github.com/python/typeshed/commit/2cdda12df78275b98a5d3cdc8a92f93d596d9d5d).
'''.lstrip()

setup(name=name,
      version="0.4.0.20241229",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/click-log.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['click>=8.0.0'],
      packages=['click_log-stubs'],
      package_data={'click_log-stubs': ['__init__.pyi', 'core.pyi', 'options.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
