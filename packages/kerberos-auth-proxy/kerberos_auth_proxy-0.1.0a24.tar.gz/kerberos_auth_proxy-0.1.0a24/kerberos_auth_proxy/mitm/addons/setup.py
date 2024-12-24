import importlib
import os

from ruamel.yaml import YAML

conf_file = os.getenv('CONFIG_FILE') or 'config.yaml'

yaml = YAML(typ='safe', pure=True)
with open(conf_file) as fp:
    conf = yaml.load(fp)

addons = []

for addon_conf in (conf.get('addons') or []):
    module_name, _, cls_name = addon_conf['type'].partition(':')
    module = importlib.import_module(module_name)
    cls = getattr(module, cls_name)

    kwargs = addon_conf.get('kwargs') or {}
    instance = cls.create(**kwargs)

    addons.append(instance)
