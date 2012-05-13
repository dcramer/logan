"""
logan.settings
~~~~~~~~~~~~~~

:copyright: (c) 2012 David Cramer.
:license: Apache License 2.0, see LICENSE for more details.
"""

from __future__ import absolute_import
from __future__ import with_statement

import errno
import imp
import os
from django.conf import settings as _settings

__all__ = ('create_default_settings', 'load_settings')

TUPLE_SETTINGS = ('INSTALLED_APPS', 'TEMPLATE_DIRS')


def create_default_settings(filepath, settings_initializer):
    if settings_initializer is not None:
        output = settings_initializer()
    else:
        output = ''

    dirname = os.path.dirname(filepath)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(filepath, 'w') as fp:
        fp.write(output)


def load_settings(filename, silent=False, allow_extras=True, settings=_settings):
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

    add_settings(mod, allow_extras=allow_extras, settings=settings)


def add_settings(mod, allow_extras=True, settings=_settings):
    """
    Adds all settings that are part of ``mod`` to the global settings object.

    Special cases ``EXTRA_APPS`` to append the specified applications to the
    list of ``INSTALLED_APPS``.
    """
    extras = {}

    for setting in dir(mod):
        if setting == setting.upper():
            setting_value = getattr(mod, setting)
            if setting in TUPLE_SETTINGS and type(setting_value) == str:
                setting_value = (setting_value,)  # In case the user forgot the comma.

            # Any setting that starts with EXTRA_ and matches a setting that is a list or tuple
            # will automatically append the values to the current setting.
            # It might make sense to make this less magical
            if setting.startswith('EXTRA_'):
                base_setting = setting.split('EXTRA_', 1)[-1]
                if isinstance(getattr(settings, base_setting), (list, tuple)):
                    extras[base_setting] = setting_value
                    continue

            setattr(settings, setting, setting_value)

    for key, value in extras.iteritems():
        curval = getattr(settings, key)
        setattr(settings, key, curval + type(curval)(value))
