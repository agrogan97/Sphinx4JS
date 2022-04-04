# Sphinx4JS #

An addon for Sphinx (https://github.com/sphinx-doc/sphinx) that will perform autodocumentation of vanilla javascript code using the standard JS docstring format.

## Installation ##
This only uses packages that come pre-packaged with Python3, so there is no requirements file. Simply download the source, and ensure you have an installation of Python3 on your device of choice.

## Usage ##

Run

    python parseJS.py <JSSourceDir> -v

Eg:

    python parseJS.py src/ -v

Replace <JSSourceDir> with the source directory of your javascript. The Python produced by this process will be saved locally in a directory called 'parsedPython/'. Use this as your target directory for Sphinx make.

-v is a verbose flag. Delete it to prevent the ASCII header from printing (boo boring!)

NB: This is in progress, not done yet! Only part of the functionality has been built.
