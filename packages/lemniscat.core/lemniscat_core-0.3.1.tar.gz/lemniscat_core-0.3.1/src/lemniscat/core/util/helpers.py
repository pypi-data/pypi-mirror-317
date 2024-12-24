import logging
import os
import re
import sys
from logging import Logger, StreamHandler, DEBUG
from typing import Union, Optional
import yaml
from simpleeval import simple_eval

from lemniscat.core.model import VariableValue

_REGEX_CAPTURE_VARIABLE = r"(?:\${{(?P<var>[^}]+)}})"
_REGEX_CAPTURE_VARIABLE_CONVERTSTR = r"(?:\W*str\((?P<var>[^)]+)\)\W*)"

class Interpreter:
    _logger: Logger
    _variables: dict
    
    def __init__(self, logger: Logger, variables: dict) -> None:
        self._logger = logger
        self._variables = variables
    
    def __interpretDict(self, value: dict, type: str = "variable", excludeInterpret: list = []) -> VariableValue:
        isSensitive = False
        for key in value:
            if key in excludeInterpret:
                return VariableValue(value, isSensitive)
            if(isinstance(value[key], str)):
                tmp = self.__intepretString(value[key], type)
            elif(isinstance(value[key], dict)):
                tmp = self.__interpretDict(value[key], type, excludeInterpret)
            elif(isinstance(value[key], list)):
                tmp = self.__interpretList(value[key], type, excludeInterpret)
            else:
                tmp = VariableValue(value[key])
            if(tmp.sensitive):
                isSensitive = True
            value[key] = tmp.value
        return VariableValue(value, isSensitive)

    def __interpretList(self, value: list, type: str = "variable", excludeInterpret: list = []) -> VariableValue:
        isSensitive = False
        for val in value:
            if(isinstance(val, str)):
                tmp = self.__intepretString(val, type)
            elif(isinstance(val, dict)):
                tmp = self.__interpretDict(val, type, excludeInterpret)
            elif(isinstance(val, list)):
                tmp = self.__interpretList(val, type, excludeInterpret)
            else:
                tmp = VariableValue(val)
            if(tmp.sensitive):
                isSensitive = True
            val = tmp.value
        return VariableValue(value, isSensitive)    

    def __intepretString(self, value: str, type: str = "variable") -> VariableValue:
        isSensitive = False
        matches = re.findall(_REGEX_CAPTURE_VARIABLE, value)
        if(len(matches) > 0):
            for match in matches:
                convertStrMatches = re.findall(_REGEX_CAPTURE_VARIABLE_CONVERTSTR, match)
                if(len(convertStrMatches) > 0):
                    for convertStrMatch in convertStrMatches:
                        convertStrVar = str.strip(convertStrMatch)
                        if(convertStrVar in self._variables):
                            if(self._variables[convertStrVar].sensitive):
                                isSensitive = True
                            if(value == f'${{{{{match}}}}}'):
                                value = str(self._variables[convertStrVar].value)
                            else:
                                value = value.replace(f'${{{{{match}}}}}', str(self._variables[convertStrVar].value))
                            self._logger.debug(f"Interpreting and converting to string {type}: {convertStrVar} -> {str(self._variables[convertStrVar].value)}")
                else:
                    var = str.strip(match)
                    if(var in self._variables):
                        if(self._variables[var].sensitive):
                            isSensitive = True
                        if(value == f'${{{{{match}}}}}'):
                            value = self._variables[var].value
                        else:
                            value = value.replace(f'${{{{{match}}}}}', self._variables[var].value)
                        self._logger.debug(f"Interpreting {type}: {var} -> {self._variables[var]}")
        return VariableValue(value, isSensitive)        

    def __interpretEvalCondition(self, condition) -> bool:
        select_variables = re.findall(_REGEX_CAPTURE_VARIABLE, condition)
        select_variables = [var.strip() for var in select_variables]
        filtered_variables = {key: self._variables[key] for key in select_variables if key in self._variables}
        variables = {}
        for key, value in filtered_variables.items():
            variables[key] = value.value if isinstance(value, VariableValue) else value
        clean_condition = re.sub(_REGEX_CAPTURE_VARIABLE, r"\1", condition)
        self._logger.debug(f"Interpreting condition: {clean_condition}")
        self._logger.debug(f"Variables: {variables}")
        return simple_eval(
            clean_condition,
            names=variables
        )

    def __interpret(self, variable: VariableValue, type: str = "variable", excludeInterpret: list = []) -> VariableValue:
        isSensitive = variable.sensitive
        if(variable is None):
            return None
        if(isinstance(variable.value, str)):
            tmp = self.__intepretString(variable.value, type)
        elif(isinstance(variable.value, dict)):
            tmp = self.__interpretDict(variable.value, type, excludeInterpret)
        elif(isinstance(variable.value, list)):
            tmp = self.__interpretList(variable.value, type, excludeInterpret)
        else:
            tmp = variable
        if(tmp.sensitive):
            isSensitive = True
        variable.value = tmp.value
        return VariableValue(variable.value, isSensitive)    
        
    def interpret(self, excludeInterpret: list = []) -> None:
        for key in self._variables:
            self._variables[key] = self.__interpret(self._variables[key], excludeInterpret)
            
    def interpretParameters(self, parameters: dict, excludeInterpret: list = []) -> dict:
        for key in parameters:
            parameters[key] = self.__interpret(VariableValue(parameters[key]), "parameter", excludeInterpret).value
        return parameters
            
    def interpretDict(self, data: dict, type: str="undefined", excludeInterpret: list = []) -> dict:
        return self.__interpretDict(data, type, excludeInterpret).value
            
    def interpretString(self, data: str, type: str="undefined") -> str:
        return self.__intepretString(data, type).value

    def interpretEvalCondition(self, condition) -> bool:
        return self.__interpretEvalCondition(condition)

    def interpretList(self, data: list, type: str="undefined", excludeInterpret: list = []) -> list:
        return self.__interpretList(data, type, excludeInterpret).value
    
class FileSystem:

    @staticmethod
    def __get_base_dir():
        """At most all application packages are just one level deep"""
        current_path = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(current_path, '../..')

    @staticmethod
    def __get_config_directory() -> str:
        base_dir = FileSystem.__get_base_dir()
        return os.path.join(base_dir, 'settings')

    @staticmethod
    def get_plugins_directory() -> str:
        base_dir = FileSystem.__get_base_dir()
        return os.path.join(base_dir, 'plugins')

    @staticmethod
    def load_configuration(name: str = 'configuration.yaml', config_directory: Optional[str] = None) -> dict:
        if config_directory is None:
            config_directory = FileSystem.__get_config_directory()
        with open(os.path.join(config_directory, name)) as file:
            input_data = yaml.safe_load(file)
        return input_data
    
    @staticmethod
    def load_configuration_path(path: str = None) -> dict:
        with open(path) as file:
            input_data = yaml.safe_load(file)
        return input_data

class CustomFormatter(logging.Formatter):
    purple = "\x1b[35;20m"
    green = "\x1b[32;20m"
    blue = "\x1b[34;20m"
    grey = "\x1b[38;20m"
    orange = "\x1b[33;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    _FORMATTER = "%(asctime)s [%(name)s][%(levelname)s] %(message)s"
    _FORMATTER_PLUGIN = "%(asctime)s    [%(name)s][%(levelname)s] %(message)s"

    FORMATS = {
        logging.DEBUG: blue + _FORMATTER + reset,
        logging.INFO: grey + _FORMATTER + reset,
        logging.WARNING: orange + _FORMATTER + reset,
        logging.ERROR: red + _FORMATTER + reset,
        logging.CRITICAL: bold_red + _FORMATTER + reset,
        70: green + _FORMATTER + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        if("plugin." in record.name and (record.levelno == logging.INFO or record.levelno == logging.DEBUG)):
            log_fmt = self.purple + self._FORMATTER_PLUGIN + self.reset
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class LogUtil(Logger):
    
    def __init__(
            self,
            name: str,
            level: Union[int, str] = DEBUG,
            *args,
            **kwargs
    ) -> None:
        super().__init__(name, level)
        logging.SUCCESS = 70
        logging.addLevelName(logging.SUCCESS, 'SUCCESS')
        self.addHandler(self.__get_stream_handler())

    def __get_stream_handler(self) -> StreamHandler:
        handler = StreamHandler(sys.stdout)
        handler.setFormatter(CustomFormatter())
        return handler    
    
    @staticmethod
    def create(log_level: str = 'DEBUG') -> Logger:
        # create logger with 'spam_application'
        logging.setLoggerClass(LogUtil)
        logger = logging.getLogger("lemniscat")
        logger.setLevel(log_level)
        return logger