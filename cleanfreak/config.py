

class Config(dict):

    def __init__(self, defaults=None):
        super(Config, self).__init__(defaults or {})

    def from_yaml(self, yml_filepath):
        import yaml

        with open(yml_filepath) as yml_file:
            self.update(yaml.load(yml_file))

    def from_json(self, json_filepath):
        import json

        with open(json_filepath) as json_file:
            self.update(json.loads(json_file.read()))
