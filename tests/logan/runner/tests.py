from unittest2 import TestCase

from logan.runner import sanitize_name, parse_args


class SanitizeNameTestCase(TestCase):
    def test_simple(self):
        self.assertEquals(sanitize_name('foo bar'), 'foo-bar')


class ParseArgsTestCase(TestCase):
    def test_no_args(self):
        result = parse_args([])
        self.assertEquals(result, ([], None, []))

    def test_no_command(self):
        result = parse_args(['--foo', '--bar'])
        self.assertEquals(result, (['--foo', '--bar'], None, []))

    def test_no_command_args(self):
        result = parse_args(['--foo', '--bar', 'foo'])
        self.assertEquals(result, (['--foo', '--bar'], 'foo', []))

    def test_no_base_args(self):
        result = parse_args(['foo', '--foo', '--bar'])
        self.assertEquals(result, ([], 'foo', ['--foo', '--bar']))

    def test_mixed_args(self):
        result = parse_args(['-f', 'foo', '--foo', '--bar'])
        self.assertEquals(result, (['-f'], 'foo', ['--foo', '--bar']))
