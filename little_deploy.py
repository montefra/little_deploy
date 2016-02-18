"""Script that deploys some files (typically documentation and/or coverage
reports) to some directory

The MIT License (MIT)

Copyright (c) 2015 Francesco Montesano
"""

from configparser import ConfigParser, ExtendedInterpolation
import os
import pathlib
import shutil
import sys

import pkg_resources

__version__ = pkg_resources.get_distribution('little-deploy').version


def parse(argv=None):
    import argparse as ap

    msg = """Deploy the documentation or coverage report to some directory,
          removing first the content of the said direcretory. The target
          directory for the deployment must be given in the ``type`` option of
          the ``[name]`` section of the ``~/.config/tox_deploy.cfg``
          configuration file. If the file, section or option do not exist, the
          deployment is aborted"""
    p = ap.ArgumentParser(description=msg,
                          formatter_class=ap.ArgumentDefaultsHelpFormatter)

    p.add_argument("project", help='''Name of the project. It can be replaced in
                   the target directory using the {project} placeholder
                   (without the trailing ``$``).''')
    p.add_argument('type', help='''Type of the files to deploy.  It can be
                   replaced in the target directory using the {type_}
                   placeholder (without the trailing ``$``).''')
    p.add_argument('deploy_from', help='''Directory from which to copy the
                   files''')

    p.add_argument('-c', '--config-file',
                   default=os.path.join('~', '.config', "little_deploy.cfg"),
                   help="Name of the configuration file")

    return p.parse_args(args=argv)


def check_type(type_):
    """Check that ``type_`` is not one of the reserved options

    Parameters
    ----------
    type_ : string
        name to check

    Raises
    ------
    ValueError
        if the name is among the reserved ones
    """
    if type_ in ['pkg_name', 'overwrite_releases', 'overwrite_dev',
                 'version_dev']:
        raise ValueError('The name "{}" for the type is not'
                         ' allowed'.format(type_))


def get_version(deploy_dir, conf):
    """Check if the deploy directory requires the version and deal with it
    properly

    Parameters
    ----------
    deploy_dir : string
        directory where the stuff meed to be deployed
    conf : dict-like
        configurations for the current project

    Returns
    -------
    version : string
        version number or None, if not required
    allow_overwrite : bool
        whether overwriting the deploy_dir, if existing, is allowed
    """
    has_version = (('{version}' in deploy_dir) and
                   ('{{version}}' not in deploy_dir) and
                   ('${version}' not in deploy_dir))
    version = None
    allow_overwrite = False

    if has_version:
        pkg_name = conf['pkg_name']
        pversion = pkg_resources.get_distribution(pkg_name).parsed_version
        if pversion.is_prerelease or pversion.is_postrelease:
            version = conf.get('version_dev', pversion.public)
            allow_overwrite = conf.getboolean('overwrite_dev', True)
        else:
            version = pversion.public
            allow_overwrite = conf.getboolean('overwrite_releases', False)

    return version, allow_overwrite


def main(argv=None):
    args = parse(argv=argv)

    check_type(args.type)

    conf = ConfigParser(interpolation=ExtendedInterpolation())
    if not conf.read(os.path.expanduser(args.config_file)):
        print('Missing configuration file: deployment aborted')
        sys.exit()

    try:
        conf_project = conf[args.project]
    except KeyError:
        print('Missing project "{}": deployment aborted'.format(args.project))
        sys.exit()

    # if not already present, inject the package name into the configuration
    if 'pkg_name' not in conf_project:
        conf_project['pkg_name'] = args.project

    try:
        deploy_to = conf_project[args.type]
    except KeyError:
        print('Missing type "{}": deployment aborted'.format(args.type))
        sys.exit()

    version, allow_overwrite = get_version(deploy_to, conf_project)

    try:
        deploy_to = pathlib.Path(deploy_to.format(name=args.project,
                                                  type_=args.type,
                                                  version=version))
    except KeyError as e:
        print("Error while creating the target directory because of"
              " {}".format(e))
        sys.exit(1)

    if not deploy_to.exists():
        # do nothing
        pass
    elif deploy_to.is_dir():
        if allow_overwrite:
            # remove the directory
            shutil.rmtree(str(deploy_to))
        else:
            # print and exit
            print("The directory '{}' already exists and I'm not allowed to"
                  "  overwrite it".format(deploy_to))
            sys.exit(1)
    else:
        print("The target {} is not a directory, remove it manually or adapt"
              " the configuration file".format(deploy_to))
        sys.exit(1)

    # copy the content of ``args.deploy_from`` into the ``deploy_to`` directory
    shutil.copytree(args.deploy_from, str(deploy_to))

    print("{} deployed to {}".format(args.deploy_from, deploy_to))


if __name__ == "__main__":
    main()
