import argparse
import os
import re

import yaml

from e2e_cli.faas.constants import (LANGUAGE_REQUIREMENT_MAPPING,
                                    SOURCE_CODE_FILE_NAME)


class HelperService:
    @classmethod
    def create_file_with_template_code(cls, file_path, boiler_code):
        with open(file_path, "w") as file:
            file.writelines(boiler_code)
    
    @classmethod 
    def create_yaml_file_with_template_code(cls, file_path, function_config):
        with open(file_path, 'w') as file:
            yaml.dump(function_config, file, default_flow_style=False)

    @classmethod
    def get_function_details(cls, function_path, language):
        if not os.path.exists(function_path):
            print("CLI can not locate function. kindly check weather this function exists in current directory.")
            return
        code = None; requirement = None

        with open(f"{function_path}/{SOURCE_CODE_FILE_NAME.get(language)}",'r') as code_file:
            code = code_file.read()

        with open(f"{function_path}/{LANGUAGE_REQUIREMENT_MAPPING.get(language)}", 'r') as requirement_file:
            requirement = requirement_file.read()

        return code, requirement

def regex_type(pattern):
    def validate(value):
        if not re.match(pattern, value):
            raise argparse.ArgumentTypeError(f"Invalid format: '{value}'")
        return value
    return validate

def timeout_range(value):
    try:
        timeout_value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("Timeout must be an integer")
    if timeout_value < 1 or timeout_value > 600:
        raise argparse.ArgumentTypeError("Timeout must be between 1 and 600 seconds")
    return timeout_value
    