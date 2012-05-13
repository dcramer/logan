Logan
=====

Logan is a toolkit for running standalone Django applications. It provides you
with tools to create a CLI runner, manage settings, and the ability to bootstrap
the process.

Let's take the Sentry project for example, it specifies that it wants to use logan
for running the application::

    setup(
        name='sentry',
        install_requires=['logan'],
        entry_points={
            'console_scripts': [
                'sentry = logan.runner:run_app',
            ],
        },
    )

It then defines several Django Management Commands as part of it's project, via the
standard structure of sentry/management/commands/<command name>.py.

Now when we call sentry. it's actually piping that to the logan runner. Logan simply
loads the predefined settings file (which defaults to PROJECT_CONF, or ~/.project/project.conf.py)
and then passes the command off to Django's internal representation of django-admin.py. In this case,
PROJECT is determined by the caller of logan.runner, which is "sentry". If it were "foo-bar", PROJECT
would be FOO_BAR, and "project" would still be "foo-bar".

In most cases, you're also going to want to provide a default configuration to inherit from,
as well as a template to generate for the user if their configuration does not exist.

To do this, within our sentry project we create a simple script, lets call put it in ``sentry/logan_runner.py``::

    from logan.runner import run_app

    def generate_settings():
        """
        This command is run when ``default_path`` doesn't exist, or ``init`` is
        run and returns a string representing the default data to put into their
        settings file.
        """
        return ""

    def main():
        run_app(
            project='sentry',
            default_config_path='~/.sentry/',
            default_settings='sentry.conf.defaults',
            settings_initializer='sentry.logan_runner.generate_settings',
            settings_envvar='SENTRY_CONF',
        )

    if __name__ == '__main__':
        main()

We'd then slightly adjust our entry point in our ``setup.py``::

    setup(
        name='sentry',
        install_requires=['logan'],
        entry_points={
            'console_scripts': [
                'sentry = sentry.logan_runner:main',
            ],
        },
    )

You'll now be able to access the ``sentry`` command as if it were django-admin.py. Even better, it will
be configurable via an arbitrary settings file, and inherit any default settings you've specified::

    # Note: run_gunicorn is provided by the gunicorn package
    sentry run_gunicorn 0.0.0.0:8000 -w 3

Extra Applications
------------------

A need might come up to allow the user to register additional settings. These will automatically apply
based on keynames prefixed with ``EXTRA_`` assuming the base key (the latter part of the setting name) is
of type list or tuple.

For example, to register additional ``INSTALLED_APPS``, you would simply specify this in your custom
(user) configuration::

    EXTRA_INSTALLED_APPS = (
        'foo.bar',
    )

This will ensure your default setting's ``INSTALLED_APPS`` do not have to be modified, and the user
can specify additional apps with ease.

If you wish to disable this functionality, simply pass ``allow_extra=False`` to ``run_app``::

    run_app(
        # ...,
        allow_extras=False,
    )
