import re

from abc import ABC, abstractmethod
from configparser import ConfigParser
from pathlib import Path
from typing import  Dict, List
from .assets import trim_path_string, get_config_file
from colorama import just_fix_windows_console
from io import TextIOWrapper
just_fix_windows_console()


class Configure(ABC):
    def __init__(
        self,
        path_config_file: str | Path = None,
        float_vars: List[str] = None,
        int_vars: List[str] = None,
        boolean_vars: List[str] = None,
        comma_delimited_vars: List[str] = None,
        space_delimited_vars: List[str] = None,
        optional_vars: List[str] = None
    ) -> None:
        super().__init__()
        self.path_config_file = path_config_file
        self.float_vars = float_vars
        self.int_vars = int_vars
        self.boolean_vars = boolean_vars
        self.comma_delimited_vars = comma_delimited_vars
        self.space_delimited_vars = space_delimited_vars
        self.optional_vars = optional_vars
        self.config_settings = {}
        self.params = {}
        self.config = None

    @abstractmethod
    def get_params(self) -> Dict: ...

    @abstractmethod
    def _prepare_input_params(self) -> None: ...

    def _check_if_path_config_file_exists(self) -> None:
        if not Path(self.path_config_file).exists():
            raise FileNotFoundError("path_config_file does NOT exist!")

    def _fetch_path_config_file(self) -> None:
        if self.path_config_file is None:
            self.path_config_file = get_config_file()

    def _is_optional_variable(self, option: str, variable: str) -> bool:
        if self.optional_vars is not None and option in self.optional_vars:
            self.params[option] = variable
            return True
        return False

    def _check_if_option_has_value(self, option: str, variable: str) -> None:
        if not variable:
            raise Exception(f"Please provide information for {option}\n")

    def _check_if_params_is_empty(self) -> None:
        if not self.params:
            raise ValueError("params output is empty! something is wrong")

    def _handle_floats(self):
        try:
            self.params = {key: float(
                value) if key in self.float_vars else value for key, value in self.params.items()}
        except ValueError as ve:
            raise ValueError(
                f"Failed to execute float conversions for float_vars\n", ve)

    def _handle_ints(self):
        try:
            self.params = {key: int(
                value) if key in self.int_vars else value for key, value in self.params.items()}
        except ValueError as ve:
            raise ValueError(
                f"Failed to execute int conversions for int_vars\n", ve)

    def _handle_booleans(self):
        try:
            self.params = {key: eval(value.capitalize(
            )) if key in self.boolean_vars else value for key, value in self.params.items()}
        except ValueError as ve:
            raise ValueError(
                f"Failed to execute boolean conversions for boolean_vars\n", ve)

    def _handle_comma_delimited(self):
        try:
            for key, value in self.params.items():
                if key in self.comma_delimited_vars:
                    _values = value.strip().split(",")
                    _values = [_value.strip() for _value in _values if _value]
                    self.params[key] = _values

        except ValueError as ve:
            raise ValueError(
                f"Failed to separate the variable into a list for comma_delimited_vars\n", ve)

    def _handle_space_delimited(self):
        try:
            for key, value in self.params.items():
                if key in self.space_delimited_vars:
                    _values = re.split(r"\s+", value.strip())
                    _values = [_value.strip() for _value in _values if _value]
                    self.params[key] = _values

        except ValueError as ve:
            raise ValueError(
                f"Failed to separate the variable into a list for space_delimited_vars\n", ve)

    def _handle_special_operations(self) -> None:
        if self.float_vars is not None:
            self._handle_floats()
        if self.int_vars is not None:
            self._handle_ints()
        if self.boolean_vars is not None:
            self._handle_booleans()
        if self.comma_delimited_vars is not None:
            self._handle_comma_delimited()
        if self.space_delimited_vars is not None:
            self._handle_space_delimited()


class ConfigureCfg(Configure):
    """
    This class parse the data of a config file which has the format below:\n
    [section]\n
    option1 =\n
    option2 =\n
    option values are read in as a string by default. In case of other data types, specify
    them as the input arguments in a list. e.g: int_vars, float_vars
    """

    def _init_config(self) -> None:
        self.config = ConfigParser()
        self.config.read(self.path_config_file)

    def _prepare_config_settings(self) -> None:
        for section in self.config.sections():
            each_section_options = []
            for option in self.config.options(section):
                each_section_options.append(option)
            self.config_settings[section] = each_section_options

    def _prepare_input_params(self) -> Dict:
        try:
            for section, options in self.config_settings.items():
                for option in options:
                    variable = trim_path_string(
                        self.config.get(section, option))
                    if self._is_optional_variable(option, variable):
                        continue
                    self._check_if_option_has_value(option, variable)
                    self.params[option] = variable

        except Exception as e:
            raise Exception(f"Failed to extract input parameters\n", e)

    def get_params(self) -> Dict:
        self._fetch_path_config_file()
        self._check_if_path_config_file_exists()
        self._init_config()
        self._prepare_config_settings()
        self._prepare_input_params()
        self._handle_special_operations()
        self._check_if_params_is_empty()
        return self.params


class ConfigureText(Configure):
    """
    This class is to prepare the inputs without the conventional .cfg file (no headers)
    The parameters and the value should be separated by "="
    "#" counts as comments in the text file and will NOT be processed
    """

    def __init__(self, path_config_file: str | Path = None, float_vars: List[str] = None, int_vars: List[str] = None, boolean_vars: List[str] = None, comma_delimited_vars: List[str] = None, space_delimited_vars: List[str] = None, optional_vars: List[str] = None) -> None:
        super().__init__(path_config_file, float_vars, int_vars, boolean_vars,
                         comma_delimited_vars, space_delimited_vars, optional_vars)
        self.reader: TextIOWrapper = None

    def _open_config_file(self) -> None:
        try:
            self.reader = open(self.path_config_file, mode="r")
        except (PermissionError, IOError) as e:
            raise RuntimeError("Failed to open the config file", e)

    def _prepare_input_params(self) -> None:
        try:
            for line in self.reader:
                # These lines are comment, not considering them
                if re.search(r"^#", line) or not line.strip():
                    continue

                key, var = line.strip().split("=")
                key, var = trim_path_string(key), trim_path_string(var)

                if self._is_optional_variable(option=key, variable=var):
                    continue

                self._check_if_option_has_value(option=key, variable=var)
                self.params[key] = var

        except Exception as e:
            raise Exception("Failed to extract input parameters", e)

    def _close_config_file(self) -> None:
        try:
            self.reader.close()
        except (PermissionError, IOError) as e:
            raise RuntimeError("Failed to open the config file", e)
        
    def get_params(self) -> Dict:
        try:
            self._fetch_path_config_file()
            self._check_if_path_config_file_exists()
            self._open_config_file()
            self._prepare_input_params()
            self._handle_special_operations()
            self._check_if_params_is_empty()
            return self.params

        except Exception as e:
            raise RuntimeError("params were not extracted", e)
    
        finally:
            if self.reader is not None:
                self._close_config_file()