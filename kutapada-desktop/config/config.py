""" Configuration file """
import json
import os


class Config: # pylint: disable=R0903
    """Main configuration file"""
    _file_name = "config.json"

    def __init__(self):
        full_config_path = os.path.join(os.getcwd(), Config._file_name)
        with open(full_config_path, "r", encoding="utf-8") as config_file:
            self.config_json = json.load(config_file)

    @property
    def data_file_path(self) -> str:
        """Path for data file"""
        return self.config_json["data_file_path"]

    @property
    def font_size(self) -> int:
        """ Font size """
        return self.config_json["font_size"]

    @property
    def prime_width(self) -> int:
        """ Width """
        return self.config_json["prime_width"]

    @property
    def prime_height(self) -> int:
        """ Height """
        return self.config_json["prime_height"]


class ConfigFactory: # pylint: disable=R0903
    """Singleton based factory"""
    _singleton: Config = None

    @staticmethod
    def get_instance() -> Config:
        """Returns singleton instance"""
        if ConfigFactory._singleton is None:
            ConfigFactory._singleton = Config()
        return ConfigFactory._singleton
