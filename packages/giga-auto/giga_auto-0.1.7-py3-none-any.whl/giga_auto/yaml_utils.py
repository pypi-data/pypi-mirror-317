import os

import yaml
from string import Template


def yaml_data(yaml_file):
    if not os.path.exists(yaml_file):
        raise FileNotFoundError(f"{yaml_file} : not exits")
    with open(yaml_file, "rb") as f:
        return yaml.safe_load(f)


def write_to_yaml(data, filename):
    with open(filename, 'w') as file:
        yaml.dump(data, file)


def yaml_variable_data(yaml_file, data):
    #data： replace ‘$’ sign data
    with open(yaml_file, encoding="utf-8") as f:
        re = Template(f.read()).substitute(data)
        content = yaml.safe_load(stream=re), type(yaml.safe_load(stream=re))
        print(content)
        return  yaml.safe_load(stream=re)