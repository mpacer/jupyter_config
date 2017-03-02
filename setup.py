from setuptools import setup
from jupyter_conf_search import __version__


setup(
    name='jupyter_conf_search',
    packages=['jupyter_conf_search'],
    version=__version__,
    author='Mike Pacer',
    author_email='mpacer@berkeley.edu',
    url='https://github.com/michaelpacer/jupyter_conf_search',
    install_requires=[
        "jupyter"
        ]
)
