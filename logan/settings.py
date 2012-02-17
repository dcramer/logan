"""
logan.settings
~~~~~~~~~~~~~~

:copyright: (c) 2012 David Cramer.
:license: Apache License 2.0, see LICENSE for more details.
"""

from __future__ import absolute_import

import errno
import imp
import os
from django.conf import settings

__all__ = ('create_default_settings', 'load_settings')


def create_default_settings(filepath, settings_initializer):
    if settings_initializer is not None:
        output = settings_initializer()
    else:
        output = ''

    dirname = os.path.dirname(filepath)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(filepath, 'w') as fp:
        fp.write(output)


def load_settings(filename, silent=False):
    """
    Configures django settings from an arbitrary (non sys.path) filename.
    """
    mod = imp.new_module('config')
    mod.__file__ = filename
    try:
        execfile(filename, mod.__dict__)
    except IOError, e:
        if silent and e.errno in (errno.ENOENT, errno.EISDIR):
            return False
        e.strerror = 'Unable to load configuration file (%s)' % e.strerror
        raise

    if not settings.configured:
        settings.configure()

    add_settings(mod)


def add_settings(mod):
    tuple_settings = ('INSTALLED_APPS', 'TEMPLATE_DIRS')

    for setting in dir(mod):
        if setting == setting.upper():
            setting_value = getattr(mod, setting)
            if setting in tuple_settings and type(setting_value) == str:
                setting_value = (setting_value,)  # In case the user forgot the comma.
            setattr(settings, setting, setting_value)
