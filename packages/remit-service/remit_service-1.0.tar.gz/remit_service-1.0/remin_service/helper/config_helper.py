import os.path
from remin_service.helper import DataCent
import threading
import yaml


def merge_dicts(*dicts):
    result = {}
    for d in dicts:
        for key, value in d.items():
            if isinstance(value, dict) and key in result:
                result[key] = merge_dicts(result[key], value)
            else:
                result[key] = value
    return result


class ConfigLoad:

    _instance_lock = threading.Lock()

    @classmethod
    def instance(cls, config_file):
        with ConfigLoad._instance_lock:
            if not hasattr(ConfigLoad, "_instance"):
                ConfigLoad._instance = ConfigLoad(config_file)
        return ConfigLoad._instance

    def __init__(self, config_file):
        self.config_file = config_file

    def load(self):

        with open(self.config_file, encoding="utf8") as file:

            DataCent.data = merge_dicts(DataCent.data, yaml.load(file.read(), Loader=yaml.FullLoader))
            # DataCent.data.update(
            #     yaml.load(file.read(), Loader=yaml.FullLoader)
            # )

        active = DataCent.data.get("config", {}).get("active")
        if not active:
            return True

        file_s = self.config_file.split(".")

        new_config_file = file_s[0] + f".{active}." + file_s[1]
        if not os.path.exists(new_config_file):
            raise FileNotFoundError(f"{new_config_file} 不存在")

        with open(new_config_file, encoding="utf8") as file:

            DataCent.data = merge_dicts(DataCent.data, yaml.load(file.read(), Loader=yaml.FullLoader))
            # DataCent.data.update(
            #     yaml.load(file.read(), Loader=yaml.FullLoader)
            # )
        # print(DataCent.data)

        return True


if __name__ == '__main__':
    ConfigLoad.instance("/src/template/resources/config.yaml").load()