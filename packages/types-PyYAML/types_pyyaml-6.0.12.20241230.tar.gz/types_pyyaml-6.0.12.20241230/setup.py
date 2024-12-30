from setuptools import setup

name = "types-PyYAML"
description = "Typing stubs for PyYAML"
long_description = '''
## Typing stubs for PyYAML

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`PyYAML`](https://github.com/yaml/pyyaml) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `PyYAML`. This version of
`types-PyYAML` aims to provide accurate annotations for
`PyYAML==6.0.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/PyYAML`](https://github.com/python/typeshed/tree/main/stubs/PyYAML)
directory.

This package was tested with
mypy 1.14.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`d634fc2f52b1f35e3bc664c7635859debbfe5e5d`](https://github.com/python/typeshed/commit/d634fc2f52b1f35e3bc664c7635859debbfe5e5d).
'''.lstrip()

setup(name=name,
      version="6.0.12.20241230",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/PyYAML.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['yaml-stubs'],
      package_data={'yaml-stubs': ['__init__.pyi', '_yaml.pyi', 'composer.pyi', 'constructor.pyi', 'cyaml.pyi', 'dumper.pyi', 'emitter.pyi', 'error.pyi', 'events.pyi', 'loader.pyi', 'nodes.pyi', 'parser.pyi', 'reader.pyi', 'representer.pyi', 'resolver.pyi', 'scanner.pyi', 'serializer.pyi', 'tokens.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
