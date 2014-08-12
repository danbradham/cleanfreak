

class Config(dict):

    def __init__(self, defaults=None):
        super(Config, self).__init__(defaults or {})


    def from_file(self, f):
        ext = f.split(".")[-1]

        cfg_loaders = {
            "yaml": load_yaml,
            "yml": load_yaml,
            "son": load_json,
            "json": load_json,
            "jsn": load_json,
            "cfg": load_cfg,
            "ini": load_cfg
        }

        try:
            data = cfg_loaders[ext](f)
        except KeyError:
            raise OSError("Config files can be json, yaml, cfg, or ini.")

        self.update(data)


def load_yaml(yml_filepath):
    import yaml

    with open(yml_filepath) as yml_file:
        data = yaml.load(yml_file)

    return data


def load_json(json_filepath):
    import json

    with open(json_filepath) as json_file:
        data = json.loads(json_file.read())

    return data


def load_cfg(cfg_file):
    try:
        from ConfigParser import SafeConfigParser
    except ImportError:
        from configparser import SafeConfigParser

    parser = SafeConfigParser()
    parser.read(cfg_file)
    data = dict(parser.items('db'))

    return data

