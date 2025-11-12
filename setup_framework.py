#!/usr/bin/env python3
"""Setup script to create remaining framework files"""
import os
from pathlib import Path

# Define folder structure
FOLDERS = [
    "pages",
    "api",
    "tests/web",
    "tests/api",
    "utils",
    "test_data",
    "reports",
    "logs",
    ".github/workflows"
]

# Define files with content
FILES = {
    "pages/__init__.py": "",
    "pages/base_page.py": '''"""Base Page Object Model class"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config.config import config

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.EXPLICIT_WAIT)
    
    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def click(self, locator):
        element = self.find_element(locator)
        element.click()
    
    def send_keys(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
''',
    "api/__init__.py": "",
    "api/base_api.py": '''"""Base API client"""
import requests
from config.config import config

class BaseAPI:
    def __init__(self):
        self.base_url = config.API_BASE_URL
        self.timeout = config.API_TIMEOUT
        self.session = requests.Session()
    
    def get(self, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint}"
        return self.session.get(url, timeout=self.timeout, **kwargs)
    
    def post(self, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint}"
        return self.session.post(url, timeout=self.timeout, **kwargs)
''',
    "tests/__init__.py": "",
    "tests/web/__init__.py": "",
    "tests/api/__init__.py": "",
    "utils/__init__.py": "",
    "utils/logger.py": '''"""Logging configuration"""
import logging
import coloredlogs

def get_logger(name):
    logger = logging.getLogger(name)
    coloredlogs.install(level='INFO', logger=logger)
    return logger
'''
}

print("Creating pytest framework structure...")

# Create folders
for folder in FOLDERS:
    Path(folder).mkdir(parents=True, exist_ok=True)
    print(f"[+] Created: {folder}/")

# Create files
for filepath, content in FILES.items():
    file_path = Path(filepath)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content)
    print(f"[+] Created: {filepath}")

print("\n[SUCCESS] Framework structure created successfully!")
print("\nNext steps:")
print("1. pip install -r requirements.txt")
print("2. cp config/.env.example .env")
print("3. Edit .env with your settings")
print("4. pytest tests/")
