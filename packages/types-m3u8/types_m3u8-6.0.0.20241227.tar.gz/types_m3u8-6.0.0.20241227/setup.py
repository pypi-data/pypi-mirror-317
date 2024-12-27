from setuptools import setup

name = "types-m3u8"
description = "Typing stubs for m3u8"
long_description = '''
## Typing stubs for m3u8

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`m3u8`](https://github.com/globocom/m3u8) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `m3u8`. This version of
`types-m3u8` aims to provide accurate annotations for
`m3u8==6.0.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/m3u8`](https://github.com/python/typeshed/tree/main/stubs/m3u8)
directory.

This package was tested with
mypy 1.14.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`7178fa3356086f5dfbde5b7c53f2523a0123430c`](https://github.com/python/typeshed/commit/7178fa3356086f5dfbde5b7c53f2523a0123430c).
'''.lstrip()

setup(name=name,
      version="6.0.0.20241227",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/m3u8.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['m3u8-stubs'],
      package_data={'m3u8-stubs': ['__init__.pyi', 'httpclient.pyi', 'mixins.pyi', 'model.pyi', 'parser.pyi', 'protocol.pyi', 'version_matching.pyi', 'version_matching_rules.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
