"""Configuration Management Module

This module manages all configuration settings for the framework.
It supports multiple environments (dev, qa, staging, prod) and loads
configuration from environment variables and .env files.
"""
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')


class Config:
    """Base configuration class"""
    
    # Environment
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'qa')
    
    # Browser Configuration
    BROWSER = os.getenv('BROWSER', 'chrome')
    HEADLESS = os.getenv('HEADLESS', 'False').lower() == 'true'
    BROWSER_WIDTH = int(os.getenv('BROWSER_WIDTH', '1920'))
    BROWSER_HEIGHT = int(os.getenv('BROWSER_HEIGHT', '1080'))
    IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', '10'))
    EXPLICIT_WAIT = int(os.getenv('EXPLICIT_WAIT', '20'))
    PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', '30'))
    
    # API Configuration
    API_BASE_URL = os.getenv('API_BASE_URL', 'https://api.example.com')
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', '30'))
    API_RETRY_COUNT = int(os.getenv('API_RETRY_COUNT', '3'))
    
    # Test Data
    TEST_DATA_DIR = BASE_DIR / 'test_data'
    
    # Reports
    REPORTS_DIR = BASE_DIR / 'reports'
    SCREENSHOTS_DIR = REPORTS_DIR / 'screenshots'
    LOGS_DIR = BASE_DIR / 'logs'
    
    # Database (if needed)
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', '5432'))
    DB_NAME = os.getenv('DB_NAME', 'testdb')
    DB_USER = os.getenv('DB_USER', 'testuser')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'testpass')
    
    # Parallel Execution
    PARALLEL_WORKERS = int(os.getenv('PARALLEL_WORKERS', '4'))
    
    # Retry Configuration
    RETRY_FAILED_TESTS = os.getenv('RETRY_FAILED_TESTS', 'True').lower() == 'true'
    RETRY_COUNT = int(os.getenv('RETRY_COUNT', '2'))
    
    @classmethod
    def get_url(cls, endpoint: str = '') -> str:
        """Get full URL for given endpoint"""
        return f"{cls.API_BASE_URL}/{endpoint}"
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            key: value for key, value in cls.__dict__.items()
            if not key.startswith('_') and not callable(value)
        }


class DevConfig(Config):
    """Development environment configuration"""
    API_BASE_URL = os.getenv('API_BASE_URL', 'https://dev-api.example.com')
    HEADLESS = False


class QAConfig(Config):
    """QA environment configuration"""
    API_BASE_URL = os.getenv('API_BASE_URL', 'https://qa-api.example.com')


class StagingConfig(Config):
    """Staging environment configuration"""
    API_BASE_URL = os.getenv('API_BASE_URL', 'https://staging-api.example.com')


class ProdConfig(Config):
    """Production environment configuration"""
    API_BASE_URL = os.getenv('API_BASE_URL', 'https://api.example.com')
    HEADLESS = True


# Environment mapping
CONFIG_MAP = {
    'dev': DevConfig,
    'qa': QAConfig,
    'staging': StagingConfig,
    'prod': ProdConfig
}


def get_config() -> Config:
    """Get configuration based on environment"""
    env = os.getenv('ENVIRONMENT', 'qa').lower()
    return CONFIG_MAP.get(env, QAConfig)


# Export current configuration
config = get_config()
