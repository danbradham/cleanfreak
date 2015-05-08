# -*- coding: utf-8 -*-
import os
import sys
import yaml
from PySide import QtCore
from . import package_path
from .messages import ConfigChanged
from .shout import shout


def on_config_changed(config):
    '''Used to update a Config object when its source file changes.'''
    def do_refresh():
        config.refresh()
        shout(ConfigChanged)
    return do_refresh


class Config(dict):
    '''Configs are concatenated from defaults and a yaml config file stored
    in a cleanfreak config folder. We first see if the CLEANFREAK_CFG
    environment variable points to a cleanfreak config folder, if it does we
    load the config from the config.yml file within it. If not, we copy the
    default cleanfreak config from within this package to your user home
    directory, and use that instead.
    '''

    env_var = 'CLEANFREAK_CFG'
    default_config_name = 'config.yml'

    def __init__(self, *args, **defaults):
        self.defaults = defaults
        self.watcher = QtCore.QFileSystemWatcher()
        self.watcher.fileChanged.connect(on_config_changed(self))
        self.refresh()

    def __getattr__(self, attr):
        if attr.upper() in self: # Redirect attribute lookup to dict keys
            return self[attr.upper()]
        raise AttributeError

    def refresh(self):
        '''Refresh config from defaults and load the yaml config again.'''
        self.clear()
        self.update(self.defaults)
        self.load()

    def load(self):
        '''Load config from config file'''

        root = os.environ.get(self.env_var)

        if not os.path.exists(root):
            package_path('conf').copy(root)

        self.root = root
        sys.path.insert(1, self.root)
        self.path = os.path.join(self.root, self.default_config_name)
        self.watcher.addPath(self.path)

        try:
            with open(self.path) as yml_file:
                data = yaml.load(yml_file)
        except KeyError:
            raise EnvironmentError('Could not load: ' + self.path)

        self.update(data)

    def relative_path(self, *args):
        '''Returns a path relative to config root.'''

        return os.path.join(self.root, *args)
