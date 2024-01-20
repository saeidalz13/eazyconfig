import unittest
from eazyconfig.ezcfg import ConfigureCfg

PATH_CONFIG_FILE = r"eazyconfig\test\config.cfg"
CONFIG_SETTINGS = {
    "path": ['input_csv', 'output'],
    "column_number": ["x", "y", "base_elevation", "flagpole_height"],
    "specs": ["unit", "list", "space", "float", "boolean", "optional"]
}
PARAMS = {
    'input_csv': 'C:\\Air Quality - Local\\100 AQTools Software\\All Receptors Combined negative elevations removed.csv',
    'output': 'C:\\Air Quality - Local\\100 AQTools Software',
    'x': 1,
    'y': 2,
    'base_elevation': 3,
    'flagpole_height': 4,
    'unit': 'm',
    "list": ["f", "g", 'g'],
    "space": ["g", "h", 'gs'],
    "float": 234.51,
    "boolean": False,
    "optional":""
}


class TestEazyConfigCfg(unittest.TestCase):
    def setUp(self) -> None:
        _obj = ConfigureCfg(path_config_file=PATH_CONFIG_FILE)
        _obj._fetch_path_config_file()
        _obj._check_if_path_config_file_exists()
        _obj._init_config()
        _obj._prepare_config_settings()
        self.config_settings = _obj.config_settings

    def test_initialize_configurecfg(self) -> None:
        self.assertIsNotNone(ConfigureCfg())

    def test_config_settings(self) -> None:
        self.assertIsNotNone(self.config_settings.get("path"))
        self.assertIsNotNone(self.config_settings.get("column_number"))
        self.assertIsNotNone(self.config_settings.get("specs"))

        self.assertEquals(self.config_settings.get(
            "path"), CONFIG_SETTINGS["path"])
        self.assertEquals(self.config_settings.get(
            "column_number"), CONFIG_SETTINGS["column_number"])
        self.assertEquals(self.config_settings.get(
            "specs"), CONFIG_SETTINGS["specs"])

    def test_get_params(self) -> None:
        self.params = ConfigureCfg(
            path_config_file=PATH_CONFIG_FILE,
            int_vars=["x", "y", "base_elevation", "flagpole_height"],
            comma_delimited_vars=["list"],
            space_delimited_vars=["space"],
            float_vars=["float"],
            boolean_vars=["boolean"],
            optional_vars=["optional"]
        ).get_params()
        self.assertEquals(self.params, PARAMS)


if __name__ == "__main__":
    unittest.main()
