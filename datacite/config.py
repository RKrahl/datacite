"""Manage configuration for the datacite package.
"""

import argparse
import configparser
import getpass
from pathlib import Path


cfgdirs = [ Path("/etc/datacite"), 
            Path.home() / ".config" / "datacite",
            Path(""), ]
"""Default search path for the configuration file"""
cfgfname = "datacite.cfg"
"""Default configuration file name"""


class ConfigError(Exception):
    """Error getting configuration options."""
    pass

class Configuration():
    """Provide a name space to store the configuration.
    """
    def __init__(self, opts):
        self._opts = opts

    def __str__(self):
        typename = type(self).__name__
        arg_strings = []
        for f in self._opts:
            if hasattr(self, f):
                arg_strings.append('%s=%r' % (f, getattr(self, f)))
        return '%s(%s)' % (typename, ', '.join(arg_strings))


def add_cli_arguments(argparser, *, login=True):
    argparser.add_argument('-c', '--configfile', help="config file")
    argparser.add_argument('-s', '--configsection',
                           help="section in the config file", metavar="SECTION")
    argparser.add_argument('-w', '--apiurl',
                           help="URL of the dois API endpoint")
    if login:
        argparser.add_argument('-u', '--username', help="username")
        argparser.add_argument('-p', '--password', help="password")

def get_config(args=None, *, login=True, **kwargs):

    def _get_arg(opt, kwargs, args):
        v = kwargs.pop(opt, None)
        if v is not None:
            return v
        if args is not None:
            return getattr(args, opt)
        return None

    if login:
        opts = ['configfile', 'configsection', 'apiurl', 'username', 'password']
    else:
        opts = ['configfile', 'configsection', 'apiurl']
    config = Configuration(opts)

    c_section_arg = _get_arg('configsection', kwargs, args)
    c_file_arg = _get_arg('configfile', kwargs, args)
    if c_section_arg:
        configfile = configparser.ConfigParser()
        fnames = c_file_arg or [str(d / cfgfname) for d in cfgdirs]
        config.configfile = configfile.read(fnames)
        config.configsection = c_section_arg
        if not config.configfile:
            raise ConfigError("Could not read config file.")
        if not configfile.has_section(config.configsection):
            raise ConfigError("Could not read config section '%s'."
                              % config.configsection)
    else:
        config.configfile = None
        config.configsection = None
    for opt in opts[2:]:
        value = _get_arg(opt, kwargs, args)
        if value is not None:
            setattr(config, opt, value)
            continue
        if config.configsection:
            try:
                value = configfile.get(config.configsection, opt)
            except configparser.NoOptionError:
                pass
            else:
                setattr(config, opt, value)
                continue
        if opt == 'password':
            setattr(config, opt, getpass.getpass())
            continue
        raise ConfigError("Config option '%s' not given." % opt)
    if kwargs:
        inv_args = ",".join("'%s'" % k for k in kwargs)
        raise TypeError("invalid keyword argument(s) %s" % inv_args)
    if not config.apiurl.endswith('/'):
        config.apiurl += '/'
    return config
