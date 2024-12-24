import re
from pathlib import Path
from typing import Dict, List, Tuple

import yaml
from black import format_file_in_place, FileMode, WriteBack

from .errors import InvalidNameError, DuplicateNameError


class ClassBuilder:
    """
    Base class for generate files from YAML file
    """

    def __init__(self, yaml_file: Path, output_dir: str):
        """
        :param yaml_file: YAML file path
        :param output_dir: Final path for generated files
        """
        self.yaml_file = yaml_file
        self.output_dir = output_dir
        self.class_names = set()
        self.classes_stack: List[Tuple[str, Dict, List[str]]] = []
        self.class_name_map = {}

    def load_yaml(self):
        """
        Load YAML file
        :return: YAML file content
        """
        with open(self.yaml_file, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    indent = "    "

    @staticmethod
    def is_valid_identifier(name: str) -> bool:
        """
        Check if the name is a valid Python identifier
        :param name: The name of the variable
        :return: True if the name is a valid Python identifier, False otherwise
        """
        return re.match(r"^[^\d\W]\w*\Z", name) is not None

    @staticmethod
    def sanitize_name(name: str) -> str:
        """
        Replace hyphens with underscores and convert to lowercase
        :param name: The name of the variable
        :return: The name of the variable in snake_case
        """
        return name.replace("-", "_").lower()

    @staticmethod
    def to_camel_case(name: str) -> str:
        """
        Convert snake_case to CamelCase
        :param name: The name of the class
        :return: The name of the class in CamelCase
        """
        parts = name.split("_")
        return "".join(part.capitalize() for part in parts)

    def generate_unique_class_name(self, path: List[str]) -> str:
        """
        Generate a unique class name from the path
        :param path: Full path to the class
        :return: Unique class name
        """
        sanitized_path = [self.sanitize_name(p) for p in path]
        return self.to_camel_case("_".join(sanitized_path))

    def validate_name(self, name: str) -> None:
        """
        Checks whether the class symbols match and whether a duplicate of the given key exists
        :param name: Verify the name of the class
        :return: None
        """
        if not self.is_valid_identifier(name):
            raise InvalidNameError(name)
        if name in self.class_names:
            raise DuplicateNameError(name)
        self.class_names.add(name)

    def collect_classes(self, data: Dict, path: List[str] = None) -> None:
        """
        Collect classes from YAML data
        :param data:
        :param path:
        :return:
        """
        if path is None:
            path = ["Root"]

        class_name = self.generate_unique_class_name(path)
        self.classes_stack.append((class_name, data, path))
        self.class_name_map[class_name] = class_name

        for key, value in data.items():
            if isinstance(value, dict):
                sanitized_key = self.sanitize_name(key)
                new_path = path + [sanitized_key]
                self.collect_classes(value, new_path)

    def process_class_stack(
        self, class_code: str, class_name: str, data: Dict, path: List[str]
    ) -> str:
        class_code += f"class {class_name}:\n"
        if not data:
            class_code += f"{self.indent}pass\n"

        for key, value in data.items():
            sanitized_key = self.sanitize_name(key)

            if isinstance(value, dict):
                sub_class_name = self.generate_unique_class_name(path + [sanitized_key])
                class_code += f"{self.indent}{sanitized_key} = {self.class_name_map[sub_class_name]}\n"
                continue

            value_type = type(value).__name__

            if value_type == "NoneType":
                value_type = "None"

            if value_type == "str":
                value = "'" + value.replace("\n", "\\n") + "'"
            else:
                value = str(value)

            class_code += f"{self.indent}{sanitized_key}: {value_type} = {value}\n"

        class_code += "\n"
        return class_code

    def generate_class_code(self) -> str:
        """
        Generate Python class code from collected data
        :return: The code of the class
        """
        class_code = ""

        while self.classes_stack:
            class_name, data, path = self.classes_stack.pop()
            class_code = self.process_class_stack(class_code, class_name, data, path)

        return class_code

    def save_class_to_file(self, class_code: str, file_name: str) -> None:
        """
        Save generated class to file
        :param class_code: The code of the class
        :param file_name: The name of the file to save
        :return: None
        """
        output_file = Path(self.output_dir) / f"{file_name}.py"

        with open(output_file, "w", encoding="utf-8") as file:
            file.write("# This is an autogenerated file. Do not modify it!.\n\n")
            file.write(class_code)

        format_file_in_place(
            output_file, fast=True, mode=FileMode(), write_back=WriteBack.YES
        )
        print(f"Generated and formatted: {output_file}")

    def generate(self) -> None:
        """
        Generate Python class from YAML file
        :return: None
        """
        yaml_data = self.load_yaml()
        yaml_file_name = Path(self.yaml_file).stem

        self.collect_classes(yaml_data)

        class_code = self.generate_class_code()

        py_file_name = f"{yaml_file_name.lower()}_tg"
        self.save_class_to_file(class_code, py_file_name)
