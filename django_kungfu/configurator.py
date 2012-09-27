"""
    django_kungfu.configurator
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implements the `Configurator` class used to hook in settings overrides.

    This class is basically the same class as in flask.config but was adapted
    to work with Django. The main differences are:
        * not a dict subclass (would be useless with Django)
        * all the paths are threated as absolute (no root_path argument)

    The original implementation can be found here::
    https://github.com/mitsuhiko/flask/blob/master/flask/config.py

    :license: BSD, see LICENSE for more details.
"""
import imp
import errno
import os


class Configurator(object):
    """Wrap a dictionary container and provide the ability to load configuration
    options from files or any kind of objects.

    Regardless of the method you use to load the configuration options, only the
    uppercase keys ar loaded into the settings container.
    
    :param container: the container where the loaded configuration options are
                      stored
    :type container: dict
    """

    def __init__(self, container):
        assert isinstance(container, dict)
        self.container = container

    def from_envvar(self, variable_name, silent=True):
        """Loads a configuration from an environment variable pointing to
        a configuration file.  This is basically just a shortcut with nicer
        error messages for this line of code::

            config.from_pyfile(os.environ['DJANGO_SETTINGS_OVERRIDE'])

        :param variable_name: name of the environment variable
        :param silent: set to `True` if you want silent failure for missing
                       files.
        :return: bool. `True` if able to load config, `False` otherwise.
        """
        rv = os.environ.get(variable_name)
        if not rv:
            if silent:
                return False
            raise RuntimeError('The environment variable %r is not set '
                               'and as such configuration could not be '
                               'loaded.  Set this variable and make it '
                               'point to a configuration file' %
                               variable_name)

        return self.from_pyfile(rv, silent=silent)

    def from_pyfile(self, filename, silent=True):
        """Updates the values in the config from a Python file. This function
        behaves as if the file was imported as module with the
        :meth:`from_object` function.

        :param filename: the filename of the config.  This can either be an
                         absolute filename or a filename relative to the
                         root path.
        :param silent: set to `True` if you want silent failure for missing
                       files.
        """
        module = imp.new_module('config')
        module.__file__ = filename
        try:
            execfile(filename, module.__dict__)
        except IOError, e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise

        self.from_object(module)
        return True

    def from_object(self, obj):
        """Updates the values from the given object (usually either
        modules or classes).

        Just the uppercase variables in that object are stored in the config.
        Example usage::

            from yourapplication import default_config
            config.from_object(default_config)

        You should not use this function to load the actual configuration but
        rather configuration defaults.  The actual config should be loaded
        with :meth:`from_pyfile` and ideally from a location not within the
        package because the package might be installed system wide.

        :param obj: an import name or object
        """
        for key in dir(obj):
            if key.isupper():
                self.container[key] = getattr(obj, key)
