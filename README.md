Opencart Extension Builder
======================

Creates a Opencart module directory structure

Requirements
------------
- Python 2.7
- Opencart directory

Usage
-----
$ python /path/to/file/opencart-extension-builder.py <action> <modulename> -d </path/to/opencart/root/directory> <options>

modulename can not have a capital letter. Words must be seperated by underscore (e.g. test_module).

Actions
-------
-  create			Creates project build

Options
-------
--adminonly			Creates only admin controller, language, view and model files.

There is only one action and one option for now. Use it wisely.
