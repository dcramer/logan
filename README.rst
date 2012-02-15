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
                'sentry = logan.runner:main',
            ],
        },
    )

It then defines several Django Management Commands as part of it's project, via the
standard structure of sentry/management/commands/<command name>.py.

Now when we call sentry. it's actually piping that to the logan runner. Logan simply
loads the predefined settings file (which defaults to PROJECT_CONF, or ~/.project/project.conf.py)
and then passes the command off to Django's internal representation of django-admin.py.

In most cases, you're also going to want to provide a default configuration to inherit from,
as well as a template to generate for the user if their configuration does not exist.

To do this, within our sentry project we create a simple script, lets call it sentry_logan.py::

    from logan.runner import run_configured

    def generate_settings():
        """
        This command is run when ``default_path`` doesn't exist, or ``init`` is
        run and returns a string representing the default data to put into their
        settings file.
        """
        return ""

    def main():
        run_configured(
            project='sentry',
            default_path='~/.sentry/',
            settings='sentry.conf.settings.defaults',
            settings_initializer='sentry_logan.generate_settings',
        )

    if __name__ == '__main__':
        main()
