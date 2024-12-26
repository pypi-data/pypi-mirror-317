# breeze/utils/yaml_utils.py

from typing import List, Optional
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedSeq
from breeze.utils.dbt_utils import get_entity_paths_from_dbt_project
import os

def load_yaml_file(file_path: str) -> dict:
    """
    Load the YAML file and return its content as a dictionary.
    
    Args:
    - file_path: The path of the YAML file to load.

    Returns:
    - A dictionary containing the contents of the YAML file.
    """
    yaml = YAML()
    try:
        with open(file_path, "r") as yml_file:
            return yaml.load(yml_file) or {}
    except FileNotFoundError as e:
        raise FileNotFoundError(f"No such file or directory: '{file_path}'") from e


def write_yaml_file(file_path: str, data: dict) -> None:
    """
    Write the given data to a YAML file.
    
    Args:
    - file_path: The path of the YAML file to write to.
    - data: A dictionary containing the contents to write to the YAML file.
    """
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)
    with open(file_path, "w") as yml_file:
        yaml.dump(data, yml_file)

def find_yaml_path(entity_name: str, resource_type: str) -> Optional[str]:
    """
    Find the path to the YAML file for the given entity (model or source).
    
    Args:
    - entity_name: The name of the model or source to find.
    - resource_tyoe: The type of entity to find ("model", "seed", "snapshot", or "source").
    
    Returns:
    - The path to the YAML file containing the entity, if found; otherwise, None.
    """

    if resource_type == "source":
        resource_paths = "models"
    else:
        resource_paths = get_entity_paths_from_dbt_project(resource_type)
        resource_paths = resource_paths[0]

    if not resource_paths:
        raise Exception(f"No {resource_type} paths defined in dbt_project.yml.")    

    for root, dirs, files in os.walk(resource_paths):
        for file in files:
            if file.endswith(".yml") or file.endswith(".yaml"):
                yml_path = os.path.join(root, file)
                with open(yml_path, "r") as yml_file:
                    yaml = YAML()
                    yml_data = yaml.load(yml_file)
                
                # Check for models or sources in the YAML data
                if resource_type != "source" and yml_data and resource_type + "s" in yml_data:
                    for model in yml_data[resource_type + "s"]:
                        if model.get("name") == entity_name:
                            return yml_path
                elif resource_type == "source" and yml_data and resource_type + "s" in yml_data:
                    for source in yml_data[resource_type + "s"]:
                        for table in source.get("tables", []):
                            if table.get("name") == entity_name:
                                return yml_path
    return None

def add_tests_to_yaml(
    yaml_entity: dict, 
    test_names: List[str], 
    columns: Optional[List[str]] = None,
    test_params: Optional[dict] = None
) -> bool:
    """
    Add one or more tests to a YAML entity (e.g., model or source).
    If columns are specified, the tests are added to those columns.
    If no columns are specified, the tests are added at the entity level.
    Returns True if changes were made, False otherwise.

    Args:
    - yaml_entity: The YAML entity to which tests will be added (e.g., model or source table).
    - test_names: A list of test names to add.
    - columns: An optional list of column names to add the tests to.
    - test_params: Optional dictionary with parameters for specific tests.

    Returns:
    - bool: True if changes were made, False otherwise.
    """
    changes_made = False
    test_params = test_params or {}

    if columns:
        # Ensure 'columns' key exists
        if "columns" not in yaml_entity or not yaml_entity["columns"]:
            yaml_entity["columns"] = []
        # Get existing columns
        existing_columns = {col["name"]: col for col in yaml_entity["columns"]}
        for col_name in columns:
            if col_name not in existing_columns:
                raise Exception(
                    f"Column '{col_name}' not found in entity '{yaml_entity.get('name', 'unknown')}'."
                )
            column = existing_columns[col_name]
            tests = column.get("tests")
            if tests is None:
                column["tests"] = CommentedSeq()
                tests = column["tests"]
            for test_name in test_names:
                test_entry = create_test_entry(test_name)
                if test_name not in tests:
                    tests.append(test_entry)
                    changes_made = True
    else:
        # Add tests at the entity level
        tests = yaml_entity.get("tests")
        if tests is None:
            yaml_entity["tests"] = CommentedSeq()
            tests = yaml_entity["tests"]
        for test_name in test_names:
            test_entry = create_test_entry(test_name)
            if test_name not in tests:
                tests.append(test_entry)
                changes_made = True

    return changes_made


def create_test_entry(test_name: str) -> dict:
    """
    Create a test entry with parameters for predefined tests.
    
    Args:
    - test_name: The name of the test.

    Returns:
    - A dictionary or string representing the test entry.
    """
    if test_name == "accepted_values":
        return {test_name: {"values": ["add_values_here"]}}
    elif test_name == "relationships":
        return {test_name: {"to": "ref('model_name')", "field": "column_name"}}
    else:
        return test_name  # Regular test name without parameters
    
def format_description(description: str, line_length: int = 80) -> str:
    """
    Format a description to use the YAML block-style `>` with wrapped lines.

    Args:
    - description: The description text to format.
    - line_length: Maximum length of each line.

    Returns:
    - str: The formatted description.
    """
    if not description:
        return ""

    words = description.split()
    formatted_lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 > line_length:  # +1 for space
            formatted_lines.append(current_line)
            current_line = word
        else:
            current_line += (" " + word) if current_line else word

    if current_line:
        formatted_lines.append(current_line)

    # Construct the formatted YAML block manually
    formatted_description = "> \n"  # Start with the block style marker
    for line in formatted_lines:
        formatted_description += f"      {line}\n"  # Add 6 spaces for indentation

    return formatted_description.strip()
