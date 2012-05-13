from unittest2 import TestCase

import mock
from logan.settings import add_settings


class AddSettingsTestCase(TestCase):
    def test_does_add_settings(self):
        class NewSettings(object):
            FOO = 'bar'
            BAR = 'baz'

        settings = mock.Mock()
        new_settings = NewSettings()
        add_settings(new_settings, settings=settings)
        self.assertEquals(getattr(settings, 'FOO', None), 'bar')
        self.assertEquals(getattr(settings, 'BAR', None), 'baz')

    def test_extra_settings_dont_get_set(self):
        class NewSettings(object):
            EXTRA_FOO = ('lulz',)

        settings = mock.Mock()
        settings.FOO = ('foo', 'bar')
        new_settings = NewSettings()
        add_settings(new_settings, settings=settings)
        self.assertFalse(settings.EXTRA_FOO.called)

    def test_extra_settings_work_on_tuple(self):
        class NewSettings(object):
            EXTRA_FOO = ('lulz',)

        settings = mock.Mock()
        settings.FOO = ('foo', 'bar')
        new_settings = NewSettings()
        add_settings(new_settings, settings=settings)
        self.assertEquals(getattr(settings, 'FOO', None), ('foo', 'bar', 'lulz'))

    def test_extra_settings_work_on_list(self):
        class NewSettings(object):
            EXTRA_FOO = ['lulz']

        settings = mock.Mock()
        settings.FOO = ['foo', 'bar']
        new_settings = NewSettings()
        add_settings(new_settings, settings=settings)
        self.assertEquals(getattr(settings, 'FOO', None), ['foo', 'bar', 'lulz'])

    def test_extra_settings_work_on_mixed_iterables(self):
        class NewSettings(object):
            EXTRA_FOO = ('lulz',)

        settings = mock.Mock()
        settings.FOO = ['foo', 'bar']
        new_settings = NewSettings()
        add_settings(new_settings, settings=settings)
        self.assertEquals(getattr(settings, 'FOO', None), ['foo', 'bar', 'lulz'])
