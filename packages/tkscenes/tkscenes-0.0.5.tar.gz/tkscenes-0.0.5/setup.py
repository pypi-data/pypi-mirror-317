from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "Readme.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.5'
DESCRIPTION = 'A package for adding scenes to TKinter and CustomTKinter'
LONG_DESCRIPTION = 'A simple package for adding different scenes to TKinter and CustomTKinter'

# Setting up
setup(
    name="tkscenes",
    version=VERSION,
    author="TonyLovesCoding",
    author_email="<tony.tonylovescoding@gmail.com>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
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
    ],
    project_urls={
        "Source": "https://github.com/TonyLovesCoding/tkscenes/"
    }
)
