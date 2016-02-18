# little_deploy

Python script that copies files from one place to an other

## Why?

I use [``tox``](http://tox.readthedocs.org/en/latest/) to run my tests, but also
to build the documentation and the
[``coverage``](https://pypi.python.org/pypi/coverage) report.

So why not having ``tox`` also copy the documentation and the report somewhere?

Here it comes ``little_deploy``

## Usage

    usage: little_deploy [-h] [-c CONFIG_FILE] project type deploy_from

    Deploy the documentation or coverage report to some directory, removing first
    the content of the said direcretory. The target directory for the deployment
    must be given in the ``type`` option of the ``[name]`` section of the
    ``~/.config/tox_deploy.cfg`` configuration file. If the file, section or
    option do not exist, the deployment is aborted

    positional arguments:
    project               Name of the project. It can be replaced in the target
                            directory using the {project} placeholder (without the
                            trailing ``$``).
    type                  Type of the files to deploy. It can be replaced in the
                            target directory using the {type_} placeholder
                            (without the trailing ``$``).
    deploy_from           Directory from which to copy the files

    optional arguments:
    -h, --help            show this help message and exit
    -c CONFIG_FILE, --config-file CONFIG_FILE
                            Name of the configuration file (default:
                            ~/.config/little_deploy.cfg)

## Configuration

``little_deploy`` is configuration driven. To be used for ``project`` the
configuration file needs to have the corresponding section. To run for ``type``,
the corresponding option must be present. ``type`` can be any string, except for
a few reserved ones, described and commented in the following example

    [project]
    # section for the project

    # the following options are directly handled by little_deploy and their
    # names are reserved

    # If present use it as the package name for the extraction of the version
    # number, if the version is required. If not present the package name is
    # assumed to be ``project``
    pkg_name = 
    # when using the version number: if the version is a release number allow
    # overwriting the target directory if exists; default False
    overwrite_releases = False
    # when using the version number: if the version is a pre-release number
    # allow overwriting the target directory if exists; default True
    overwrite_dev = True
    # when using the version number: if the version is a pre-release number
    # and this option is given change the version name to the value of
    # ``version_dev``; WARNING: setting this option and ``overwrite_dev`` to
    # False can lead to unexpected results
    version_dev = development

    # types names
    type = /path/to/where/the/type/must/be/deployed

In the ``type`` value the following placeholders are expanded using [python
format
syntax](https://docs.python.org/3/library/string.html#custom-string-formatting)

* ``{project}``: the project name
* ``{type}``: the type of the files to deploy
* ``{version}``: the version of the package; the version is extracted **only**
  if this placeholder is present; the version is extracted using
  [``pkg_resources``](https://pythonhosted.org/setuptools/pkg_resources.html)

## Example

Let's say that your project is called ``my_project`` and you want to move some
file of a given ``type``, let's say some documentation, from a directory
``/my/doc/is/here`` somewhere else. You just copy call:

    little_deploy my_project doc /my/doc/is/here

To instruct ``little_deploy`` about where to copy the files of ``doc`` from
``my_project``, we need a configuration file. And yes, to have guessed
correctly: by default it looks for ``~/.config/little_deploy.cfg``. This is how
the configuration file looks like:

    # this is the little_deploy configuration file
    [my_project]
    doc = /path/where/i/want/to/copy/{project}_{type_}

This will make ``little_deploy`` copy the content of ``/my/doc/is/here`` into
``/path/where/i/want/to/copy/my_project_doc``

If you need to use it for other projects and types you can create other entries
in the configuration file:

    # this is the little_deploy configuration file
    [my_project]
    doc = /path/where/i/want/to/copy/{project}_{type_}
    cover = ${doc}/{version}  # it uses extended interpolation

    [other_project]

    doc = ${my_project:doc}
    other = /path/to/fantasia

## Example of usage in Tox

Use ``little_deploy`` to build and copy the documentation using tox. This is an
example of ``tox.ini``:

    [tox]
    envlist = doc, py34, py35

    project = my_project

    [testenv]
    # your test configuration goes here

    [testenv:doc]
    # create the documentation
    basepython = python3  # this is important: little_deploy works in python >= 3.4
    changedir = doc
    deps =
        sphinx
        git+https://github.com/montefra/little_deploy.git#egg=little_deploy

    commands =
        sphinx-build -b html -d {envtmpdir}/doctrees source {envtmpdir}/html
        little_deploy {[tox]project} doc {envtmpdir}/html


----

Enjoy!
