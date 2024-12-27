from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.4'
DESCRIPTION = 'A package for adding scenes to TKinter and CustomTKinter'
LONG_DESCRIPTION = 'A simple package for adding different scenes to TKinter and CustomTKinter'

# Setting up
setup(
    name="TkScenes",
    version=VERSION,
    author="TonyLovesCoding",
    author_email="<tonyhyphens@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['scene', "simple"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
