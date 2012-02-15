"""
logan.runner
~~~~~~~~~~~~

:copyright: (c) 2012 David Cramer.
:license: Apache License 2.0, see LICENSE for more details.
"""

from __future__ import absolute_import

from django.core import management
from django.utils.importlib import import_module
from optparse import OptionParser
import os
import re
import sys

from logan.settings import create_default_settings, load_settings


def sanitize_name(project):
    project = project.replace(' ', '-')
    return re.sub('[^A-Z0-9a-z_-]', '-', project)


def parse_args(args):
    """
    This parses the arguments and returns a tuple containing:

    (args, command, command_args)

    For example, "--config=bar start --with=baz" would return:

    (['--config=bar'], 'start', ['--with=baz'])
    """
    index = None
    for arg_i, arg in enumerate(args):
        if not arg.startswith('-'):
            index = arg_i
            break

    # Unable to parse any arguments
    if index is None:
        return (args, None, [])

    return (args[:index], args[index], args[(index + 1):])


def run_app(project=None, default_config_path=None, default_settings=None,
            settings_initializer=None, settings_envvar=None, initializer=None):
    """
    :param project: should represent the canonical name for the project, generally
        the same name it assigned in distutils.
    :param default_config_path: the default location for the configuration file.
    :param default_settings: default settings to load (think inheritence).
    :param settings_initializer: a callback function which should return a string
        representing the default settings template to generate.
    :param initializer: a callback function which will be executed before the command
        is executed. It is passed a dictionary of various configuration attributes.
    """

    sys_args = sys.argv

    # The established command for running this program
    runner_name = sys_args[0]

    args, command, command_args = parse_args(sys_args[1:])

    if not command:
        print "usage: %s [--config=/path/to/settings.py] [command] [options]" % runner_name
        sys.exit(1)

    parser = OptionParser()

    project_filename = sanitize_name(project)

    if default_config_path is None:
        default_config_path = '~/%s/%s.conf.py' % (project_filename, project_filename)

    if settings_envvar is None:
        settings_envvar = project_filename.upper() + '_CONF'

    # normalize path
    if settings_envvar in os.environ:
        default_config_path = os.environ.get(settings_envvar)
    else:
        default_config_path = os.path.normpath(os.path.abspath(os.path.expanduser(default_config_path)))

    # The ``init`` command is reserved for initializing configuration
    if command == 'init':
        (options, opt_args) = parser.parse_args()

        config_path = ' '.join(opt_args[1:]) or default_config_path

        if os.path.exists(config_path):
            resp = None
            while resp not in ('Y', 'n'):
                resp = raw_input('File already exists at %r, overwrite? [nY] ' % config_path)
                if resp == 'n':
                    print "Aborted!"
                    return

        try:
            create_default_settings(config_path, settings_initializer)
        except OSError, e:
            raise e.__class__, 'Unable to write default settings file to %r' % config_path

        print "Configuration file created at %r" % config_path

        return

    parser.add_option('--config', metavar='CONFIG', default=default_config_path)

    (options, logan_args) = parser.parse_args()

    config_path = options.config

    if not os.path.exists(config_path):
        raise ValueError("Configuration file does not exist. Use '%s init' to initialize the file." % runner_name)

    if default_settings:
        settings_mod = import_module(default_settings)
        management.setup_environ(settings_mod)

    load_settings(config_path)

    if initializer is not None:
        initializer({
            'project': project,
            'config_path': config_path,
        })

    management.execute_from_command_line([runner_name, command] + command_args)

    sys.exit(0)

if __name__ == '__main__':
    run_app()
