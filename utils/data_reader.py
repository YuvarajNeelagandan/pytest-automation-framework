from pathlib import Path
import json
import yaml
import csv
from typing import Dict, List, Any, Optional
from utils.helpers import read_json_file, read_yaml_file
from utils.logger import get_logger

logger = get_logger(__name__)


class DataReader:
    """
    Utility class for reading test data from various file formats.
    Supports JSON, YAML, and CSV formats.
    """

    def __init__(self, base_path='test_data'):
        self.base_path = Path(base_path)
        logger.info(f"Initialized DataReader with base path: {self.base_path}")

    def read_json(self, filename):
        """
        Read data from a JSON file.
        
        Args:
            filename: Name of the JSON file
        
        Returns:
            dict: Parsed JSON data
        """
        file_path = self.base_path / filename
        logger.debug(f"Reading JSON file: {file_path}")
        try:
            data = read_json_file(file_path)
            logger.info(f"Successfully read JSON file: {filename}")
            return data
        except Exception as e:
            logger.error(f"Failed to read JSON file {filename}: {str(e)}")
            raise

    def read_yaml(self, filename):
        """
        Read data from a YAML file.
        
        Args:
            filename: Name of the YAML file
        
        Returns:
            dict: Parsed YAML data
        """
        file_path = self.base_path / filename
        logger.debug(f"Reading YAML file: {file_path}")
        try:
            data = read_yaml_file(file_path)
            logger.info(f"Successfully read YAML file: {filename}")
            return data
        except Exception as e:
            logger.error(f"Failed to read YAML file {filename}: {str(e)}")
            raise

    def read_csv(self, filename):
        """
        Read data from a CSV file.
        
        Args:
            filename: Name of the CSV file
        
        Returns:
            list: List of dictionaries with CSV data
        """
        file_path = self.base_path / filename
        logger.debug(f"Reading CSV file: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            logger.info(f"Successfully read CSV file: {filename}")
            return data
        except Exception as e:
            logger.error(f"Failed to read CSV file {filename}: {str(e)}")
            raise

    def get_test_data(self, filename):
        """
        Automatically detect file type and read data.
        
        Args:
            filename: Name of the file with extension
        
        Returns:
            Data from the file
        """
        file_path = Path(filename)
        extension = file_path.suffix.lower()
        
        if extension == '.json':
            return self.read_json(filename)
        elif extension in ['.yaml', '.yml']:
            return self.read_yaml(filename)
        elif extension == '.csv':
            return self.read_csv(filename)
        else:
            logger.error(f"Unsupported file extension: {extension}")
            raise ValueError(f"Unsupported file extension: {extension}")

    def get_user_data(self, username=None):
        """
        Get user test data from users.yaml file.
        
        Args:
            username: Optional username to filter
        
        Returns:
            dict or list: User data
        """
        users = self.read_yaml('users.yaml')
        if username:
            return users.get('users', {}).get(username)
        return users.get('users', {})

    def get_booking_data(self, booking_type='default'):
        """
        Get booking test data from booking_data.json file.
        
        Args:
            booking_type: Type of booking data to retrieve
        
        Returns:
            dict: Booking data
        """
        bookings = self.read_json('booking_data.json')
        return bookings.get(booking_type, {})
