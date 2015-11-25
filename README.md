# little_deploy

Python script that copies files from one place to an other

## Why?

I use [``tox``](http://tox.readthedocs.org/en/latest/) to run my tests, but also
to build the documentation and the
[``coverage``](https://pypi.python.org/pypi/coverage) report.

So why not having ``tox`` also copy the documentation and the report somewhere?

Here it comes ``little_deploy``

## How?

    usage: Deploy the documentation or coverage report to some directory,
            removing first the content of the said direcretory. The target
            directory for the deployment must be given in the ``type`` option of
            the ``[name]`` section of the ``~/.config/tox_deploy.cfg``
            configuration file. If the file, section or option do not exist, the
            deployment is aborted

    positional arguments:
    project      Name of the project. It can be replaced in the target directory
                using the {project} placeholder (without the trailing ``$``).
    type         Type of the files to deploy. It can be replaced in the target
                directory using the {type_} placeholder (without the trailing
                ``$``).
    deploy_from  Directory from which to copy the files

    optional arguments:
    -h, --help   show this help message and exit
