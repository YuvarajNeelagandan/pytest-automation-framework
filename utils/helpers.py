import os
import json
import yaml
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
import random
import string


def wait_for_condition(condition_func, timeout=10, poll_interval=0.5):
    """
    Wait for a condition to be true within a timeout period.
    
    Args:
        condition_func: Function that returns True when condition is met
        timeout: Maximum time to wait in seconds
        poll_interval: Time between condition checks
    
    Returns:
        bool: True if condition met, False if timeout
    """
    end_time = time.time() + timeout
    while time.time() < end_time:
        if condition_func():
            return True
        time.sleep(poll_interval)
    return False


def generate_random_string(length=10, include_digits=True, include_special=False):
    """
    Generate a random string of specified length.
    
    Args:
        length: Length of string to generate
        include_digits: Include numbers in string
        include_special: Include special characters
    
    Returns:
        str: Random string
    """
    chars = string.ascii_letters
    if include_digits:
        chars += string.digits
    if include_special:
        chars += string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))


def generate_random_email(domain='test.com'):
    """
    Generate a random email address.
    
    Args:
        domain: Email domain
    
    Returns:
        str: Random email address
    """
    username = generate_random_string(8, include_digits=True)
    return f"{username}@{domain}"


def get_timestamp(format_string='%Y%m%d_%H%M%S'):
    """
    Get current timestamp in specified format.
    
    Args:
        format_string: strftime format string
    
    Returns:
        str: Formatted timestamp
    """
    return datetime.now().strftime(format_string)


def ensure_directory_exists(directory_path):
    """
    Ensure a directory exists, create if it doesn't.
    
    Args:
        directory_path: Path to directory
    
    Returns:
        Path: Path object of the directory
    """
    path = Path(directory_path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_json_file(file_path):
    """
    Read and parse a JSON file.
    
    Args:
        file_path: Path to JSON file
    
    Returns:
        dict: Parsed JSON data
    """
    with open(file_path, 'r') as f:
        return json.load(f)


def write_json_file(file_path, data, indent=2):
    """
    Write data to a JSON file.
    
    Args:
        file_path: Path to JSON file
        data: Data to write
        indent: Indentation level for pretty printing
    """
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=indent)


def read_yaml_file(file_path):
    """
    Read and parse a YAML file.
    
    Args:
        file_path: Path to YAML file
    
    Returns:
        dict: Parsed YAML data
    """
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)


def write_yaml_file(file_path, data):
    """
    Write data to a YAML file.
    
    Args:
        file_path: Path to YAML file
        data: Data to write
    """
    with open(file_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)


def retry_on_exception(max_attempts=3, delay=1, exceptions=(Exception,)):
    """
    Decorator to retry a function on exception.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Delay between retries in seconds
        exceptions: Tuple of exception types to catch
    
    Returns:
        Decorated function
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise
                    time.sleep(delay)
            return None
        return wrapper
    return decorator


def sanitize_filename(filename):
    """
    Sanitize a string to be used as a filename.
    
    Args:
        filename: String to sanitize
    
    Returns:
        str: Sanitized filename
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def get_project_root():
    """
    Get the project root directory.
    
    Returns:
        Path: Project root path
    """
    current_file = Path(__file__)
    return current_file.parent.parent


def merge_dicts(*dicts):
    """
    Merge multiple dictionaries, later dicts override earlier ones.
    
    Args:
        *dicts: Variable number of dictionaries to merge
    
    Returns:
        dict: Merged dictionary
    """
    result = {}
    for d in dicts:
        if d:
            result.update(d)
    return result
