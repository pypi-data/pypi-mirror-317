# How to publish on PyPi

This repo contains a somewhat minimal setup for publishing on [PyPi](https://pypi.org).

## Publishing steps

1. Create an account (preferably for [test PyPi](https://test.pypi.org) where one can
   freely experiment) and get a token.

2. Create a
   [`~/.pypirc`](https://packaging.python.org/en/latest/specifications/pypirc/#the-pypirc-file)
   with the following content:

   ```
    [distutils]
	  index-servers = pypi testpypi

	[pypi]
	  username = __token__
      password = ...

	[testpypi]
	  username = __token__
      password = ...
   ```

3. Create a git repository, with your python package and add a tag with a release
   version (e.g., `0.0.1`). Dev versions like `0.0.2.dev1` cannot be published. Note
   that in the
   [`pyproject.toml`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#writing-your-pyproject-toml)
   we use `dynamic = ["version"]`, i.e., the version is dynamically generatd (see
   [setuptools_scm](https://setuptools-scm.readthedocs.io/en/latest/usage/#default-versioning-scheme)).

4. Publish using `make publish`

   The `install-local` and `dist-local` targets are not necessary when publishing but
   are useful in general.

## Notes on package name (underscore vs. dash)

+ The name of our package is `example_publish_pypi` (stored in
  `src/example_publish_pypi`) -- we shouldn't use dashes in this name.

+ All mensions of our package in `pyproject.toml` could be using `example_publish_pypi`
  (i.e., with underscores). Sometimes doing this is necessary:
  + `write_to = "src/example_publish_pypi/_version.py"`

  and sometimes it is optional:
  + `name = "example-publish-pypi"` -- here dashes and underscores are
	[interchangeable](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#name)
  + `dev = ["example-publish-pypi[lint,code]"]`

+ Regardless of whether we set `name = "example-publish-pypi"`or `name =
  "example_publish_pypi"`, once the package is published, it could be installed in any number of ways:
  + `pip install example-publish-pypi`
  + `pip install example_publish_pypi`
  + `pip install example.publish.pypi`
