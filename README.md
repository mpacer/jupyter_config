In order to use this

    pip install jupyter_config

Which is then executed as

    jupyter config search "your_search_term"

on the command line to search for "`your_search_term`".

If you pass 

    jupyter config list

it will return the total list of configuration files that it found relative to
the directory that you are running the command from (not just the directories,
which you can find using `jupyter --paths` beneath `config:`).


## Developing on jupyter_config

If you want to work on this codebase we recommend that you first fork the repository on GitHub.

Then clone your repository locally. 

`cd` into that directory and create a new remote called **upstream** that you will point at
this repo.

```
git remote add upstream https://github.com/mpacer/jupyter_config
```

Then you can editably install this with development dependencies so that any changes you make
to the codebase get propagated to the rest of the system. Assuming you are still in the root
directory of this project, you can do this with: 

```
pip install -e .[dev]
```

To speed up the iteration cycle on developing in the library, you can run our tests locally.

To do so run: 

```
pytest --pyargs jupyter_config
```

## Releasing jupyter_config

Before you release, you should make sure to run `check-manifest` to ensure your `MANIFEST.in`
is up to date.

More detailed release instructions are en route per issue #1.
