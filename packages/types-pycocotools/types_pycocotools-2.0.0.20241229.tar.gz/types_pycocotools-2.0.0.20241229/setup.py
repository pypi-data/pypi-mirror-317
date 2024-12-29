from setuptools import setup

name = "types-pycocotools"
description = "Typing stubs for pycocotools"
long_description = '''
## Typing stubs for pycocotools

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`pycocotools`](https://github.com/ppwwyyxx/cocoapi) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `pycocotools`. This version of
`types-pycocotools` aims to provide accurate annotations for
`pycocotools==2.0.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/pycocotools`](https://github.com/python/typeshed/tree/main/stubs/pycocotools)
directory.

This package was tested with
mypy 1.14.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`2cdda12df78275b98a5d3cdc8a92f93d596d9d5d`](https://github.com/python/typeshed/commit/2cdda12df78275b98a5d3cdc8a92f93d596d9d5d).
'''.lstrip()

setup(name=name,
      version="2.0.0.20241229",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pycocotools.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['numpy>=2.0.0rc1; python_version >= "3.9"'],
      packages=['pycocotools-stubs'],
      package_data={'pycocotools-stubs': ['__init__.pyi', 'coco.pyi', 'cocoeval.pyi', 'mask.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.9",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
