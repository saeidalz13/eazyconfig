import unittest
from eazyconfig.ezcfg import ConfigureText


PATH_CONFIG_FILE = r"eazyconfig\test\config_text.cfg"

PARAMS = {
    'file': 'path/to/dir',
    'integer': 3,
    'unit': 'm',
    "list": ["f", "g", 'g'],
    "space": ["g", "h", 'gs'],
    "float": 234.51,
    "boolean": False,
    "optional":""
}


class TestEazyConfigText(unittest.TestCase):
    def setUp(self) -> None:
        self._obj = ConfigureText(
            path_config_file=PATH_CONFIG_FILE,
            int_vars=["integer"],
            comma_delimited_vars=["list"],
            space_delimited_vars=["space"],
            float_vars=["float"],
            boolean_vars=["boolean"],
            optional_vars=["optional"]
        )

    def test_get_params(self) -> None:
        self.assertEquals(self._obj.get_params(), PARAMS)


if __name__ == "__main__":
    unittest.main()
