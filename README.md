# Pytest Automation Framework

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Pytest](https://img.shields.io/badge/pytest-8.0-green)
![License](https://img.shields.io/badge/license-MIT-blue)

A comprehensive, scalable test automation framework built with Pytest for Web (Selenium) and API testing using industry-standard design patterns.

## 🎯 Features

- **Page Object Model (POM)**: Structured web test automation
- **API Testing**: RESTful API test support with request/response validation
- **Multiple Environments**: Dev, QA, Staging, Production configurations
- **Parallel Execution**: Run tests in parallel with pytest-xdist
- **Rich Reporting**: HTML, Allure, and JSON reports
- **Data-Driven Testing**: YAML/JSON test data support
- **Retry Mechanism**: Auto-retry failed tests
- **CI/CD Ready**: GitHub Actions, Jenkins integration
- **Logging**: Comprehensive logging with colored output
- **Screenshot on Failure**: Automatic screenshot capture
- **Cross-Browser Support**: Chrome, Firefox, Edge, Safari

## 📁 Project Structure

```
pytest-automation-framework/
│
├── config/                     # Configuration files
│   ├── __init__.py
│   ├── config.py              # Environment configurations
│   └── .env.example           # Environment variables template
│
├── pages/                      # Page Object Models (Web)
│   ├── __init__.py
│   ├── base_page.py           # Base page class
│   ├── login_page.py          # Example: Login page
│   └── dashboard_page.py      # Example: Dashboard page
│
├── api/                        # API clients and models
│   ├── __init__.py
│   ├── base_api.py            # Base API client
│   ├── auth_api.py            # Authentication endpoints
│   └── users_api.py           # User management endpoints
│
├── tests/                      # Test files
│   ├── __init__.py
│   ├── web/                   # Web UI tests
│   │   ├── __init__.py
│   │   ├── test_login.py
│   │   └── test_dashboard.py
│   ├── api/                   # API tests
│   │   ├── __init__.py
│   │   ├── test_auth_api.py
│   │   └── test_users_api.py
│   └── conftest.py            # Shared fixtures
│
├── utils/                      # Utility modules
│   ├── __init__.py
│   ├── logger.py              # Logging configuration
│   ├── helpers.py             # Helper functions
│   ├── data_reader.py         # Test data readers
│   └── driver_factory.py      # WebDriver factory
│
├── test_data/                  # Test data files
│   ├── users.yaml
│   ├── test_data.json
│   └── api_payloads/
│
├── reports/                    # Test reports
│   ├── html/
│   ├── allure-results/
│   └── screenshots/
│
├── logs/                       # Log files
│   └── pytest.log
│
├── .github/                    # CI/CD workflows
│   └── workflows/
│       └── test.yml
│
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (git-ignored)
├── .gitignore                 # Git ignore file
├── README.md                  # This file
└── LICENSE                     # MIT License
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Chrome/Firefox browser

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YuvarajNeelagandan/pytest-automation-framework.git
cd pytest-automation-framework
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp config/.env.example .env
# Edit .env file with your configurations
```

## 📚 Framework Design Patterns

### 1. Page Object Model (POM)

The Page Object Model is implemented to separate test logic from page-specific code:

```python
# pages/base_page.py
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
    
    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

# pages/login_page.py
class LoginPage(BasePage):
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    
    def login(self, username, password):
        self.find_element(self.USERNAME_FIELD).send_keys(username)
        self.find_element(self.PASSWORD_FIELD).send_keys(password)
        self.find_element(self.LOGIN_BUTTON).click()
```

### 2. Factory Pattern

Used for WebDriver initialization supporting multiple browsers:

```python
# utils/driver_factory.py
class DriverFactory:
    @staticmethod
    def get_driver(browser="chrome", headless=False):
        if browser.lower() == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Chrome(options=options)
        elif browser.lower() == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Firefox(options=options)
        return driver
```

### 3. Singleton Pattern

Configuration management uses singleton to ensure single instance:

```python
# config/config.py
class Config:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### 4. Strategy Pattern

Different environment configurations:

```python
CONFIG_MAP = {
    'dev': DevConfig,
    'qa': QAConfig,
    'staging': StagingConfig,
    'prod': ProdConfig
}
```

## ⚡ Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test Categories
```bash
# Run only web tests
pytest tests/web/ -v

# Run only API tests
pytest tests/api/ -v

# Run tests by marker
pytest -m smoke
pytest -m "api and regression"
```

### Run Tests in Parallel
```bash
# Auto-detect number of CPUs
pytest -n auto

# Specify number of workers
pytest -n 4
```

### Run with Different Browsers
```bash
pytest --browser=chrome
pytest --browser=firefox --headless
```

### Run with Environment
```bash
ENVIRONMENT=qa pytest
ENVIRONMENT=prod pytest -m smoke
```

### Generate Reports
```bash
# HTML Report
pytest --html=reports/report.html --self-contained-html

# Allure Report
pytest --alluredir=reports/allure-results
allure serve reports/allure-results

# JSON Report
pytest --json-report --json-report-file=reports/report.json
```

## 📋 Test Examples

### Web UI Test Example

```python
# tests/web/test_login.py
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@pytest.mark.ui
@pytest.mark.smoke
class TestLogin:
    
    def test_successful_login(self, driver, test_data):
        """Test successful login with valid credentials"""
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        
        login_page.navigate_to()
        login_page.login(
            test_data['valid_user']['username'],
            test_data['valid_user']['password']
        )
        
        assert dashboard_page.is_logged_in()
        assert dashboard_page.get_welcome_message() == f"Welcome, {test_data['valid_user']['name']}"
    
    @pytest.mark.negative
    def test_invalid_login(self, driver):
        """Test login with invalid credentials"""
        login_page = LoginPage(driver)
        
        login_page.navigate_to()
        login_page.login("invalid@email.com", "wrongpassword")
        
        assert login_page.is_error_displayed()
        assert "Invalid credentials" in login_page.get_error_message()
```

### API Test Example

```python
# tests/api/test_users_api.py
import pytest
from api.users_api import UsersAPI

@pytest.mark.api
@pytest.mark.regression
class TestUsersAPI:
    
    def test_get_all_users(self, api_client):
        """Test retrieving all users"""
        users_api = UsersAPI(api_client)
        response = users_api.get_all_users()
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) > 0
    
    def test_create_user(self, api_client, user_payload):
        """Test creating a new user"""
        users_api = UsersAPI(api_client)
        response = users_api.create_user(user_payload)
        
        assert response.status_code == 201
        assert response.json()['email'] == user_payload['email']
        assert 'id' in response.json()
    
    def test_update_user(self, api_client, existing_user):
        """Test updating user information"""
        users_api = UsersAPI(api_client)
        update_data = {"name": "Updated Name"}
        
        response = users_api.update_user(existing_user['id'], update_data)
        
        assert response.status_code == 200
        assert response.json()['name'] == update_data['name']
```

## ⚙️ Configuration

### Environment Variables (.env)

```bash
# Environment
ENVIRONMENT=qa

# Browser Settings
BROWSER=chrome
HEADLESS=False
BROWSER_WIDTH=1920
BROWSER_HEIGHT=1080

# Timeouts
IMPLICIT_WAIT=10
EXPLICIT_WAIT=20
PAGE_LOAD_TIMEOUT=30

# API Settings
API_BASE_URL=https://qa-api.example.com
API_TIMEOUT=30
API_RETRY_COUNT=3

# Test Execution
PARALLEL_WORKERS=4
RETRY_FAILED_TESTS=True
RETRY_COUNT=2
```

### Pytest Markers

Available test markers defined in `pytest.ini`:

- `@pytest.mark.smoke` - Critical smoke tests
- `@pytest.mark.regression` - Full regression suite
- `@pytest.mark.api` - API tests
- `@pytest.mark.ui` - Web UI tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Slow running tests
- `@pytest.mark.fast` - Fast tests
- `@pytest.mark.critical` - Critical priority

## 🎯 Best Practices

### 1. Test Organization
- One test class per page/feature
- Clear, descriptive test names
- Use fixtures for setup/teardown
- Group related tests using classes

### 2. Page Objects
- Keep locators in page classes
- Use meaningful locator names
- Implement waits in base page
- Return page objects for chaining

### 3. Data Management
- Store test data in YAML/JSON files
- Use fixtures for test data
- Separate env-specific data
- Never hardcode sensitive data

### 4. Assertions
- Use explicit assertions
- Add meaningful assertion messages
- Use soft assertions for multiple checks

### 5. Logging
- Log important test steps
- Include screenshots for failures
- Use appropriate log levels

## 🔧 Utilities

### Logger
```python
from utils.logger import get_logger

logger = get_logger(__name__)
logger.info("Test started")
logger.error("Test failed", exc_info=True)
```

### Data Reader
```python
from utils.data_reader import DataReader

# Read YAML
data = DataReader.read_yaml('test_data/users.yaml')

# Read JSON
data = DataReader.read_json('test_data/api_payloads/create_user.json')
```

## 🔄 CI/CD Integration

### GitHub Actions

Sample workflow file (`.github/workflows/test.yml`):

```yaml
name: Test Automation

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      env:
        ENVIRONMENT: qa
        HEADLESS: true
      run: |
        pytest -n auto -m smoke --html=reports/report.html --self-contained-html
    
    - name: Upload test report
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-report
        path: reports/
```

## 📚 Additional Documentation

### Complete File Creation Guide

To complete the framework setup, create the following files with the implementations:

#### 1. Base Page (pages/base_page.py)
- Implement common page methods (find_element, click, send_keys)
- Add explicit waits
- Screenshot capture on failure
- Page load verification

#### 2. API Base Client (api/base_api.py)
- HTTP methods (GET, POST, PUT, DELETE)
- Request/Response logging
- Authentication handling
- Error handling and retries

#### 3. Driver Factory (utils/driver_factory.py)
- Multi-browser support
- WebDriverManager integration
- Custom browser options
- Remote WebDriver support

#### 4. Logger Setup (utils/logger.py)
- Console and file logging
- Colored output
- Log rotation
- Different log levels per module

#### 5. Test Fixtures (tests/conftest.py)
- Browser fixture with cleanup
- API client fixture
- Test data fixtures
- Screenshot on failure hook

#### 6. Data Readers (utils/data_reader.py)
- YAML file reader
- JSON file reader
- CSV file reader
- Environment-specific data loading

#### 7. Helpers (utils/helpers.py)
- Random data generators
- Date/Time utilities
- String manipulation
- File operations

## 🛠️ Troubleshooting

### Common Issues

**Issue**: WebDriver not found
```bash
# Solution: Install webdriver-manager
pip install webdriver-manager
```

**Issue**: Tests failing in headless mode
```bash
# Solution: Increase window size
BROWSER_WIDTH=1920 BROWSER_HEIGHT=1080 pytest
```

**Issue**: Element not found
- Check if element is in iframe
- Verify locator strategy
- Add explicit waits
- Check for dynamic content

## 📊 Scalability Features

1. **Parallel Execution**: Tests run in parallel using pytest-xdist
2. **Distributed Testing**: Support for Selenium Grid
3. **Cloud Integration**: BrowserStack, Sauce Labs support
4. **Docker Support**: Containerized test execution
5. **Database Pooling**: Efficient database connections
6. **Caching**: Response caching for repeated API calls
7. **Modular Design**: Easy to extend and maintain

## 📝 Test Reporting

### Available Report Types

1. **HTML Report**: pytest-html
2. **Allure Report**: Rich interactive reports
3. **JSON Report**: Machine-readable results
4. **JUnit XML**: CI/CD integration
5. **Custom Reports**: Extend reporting as needed

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact & Support

- **Author**: Yuvraj Neelagandan
- **GitHub**: [@yuvaraj-neelagandan](https://github.com/yuvaraj-neelagandan)
- **Repository**: [pytest-automation-framework](https://github.com/YuvarajNeelagandan/pytest-automation-framework)

For issues and questions, please use the [GitHub Issues](https://github.com/YuvarajNeelagandan/pytest-automation-framework/issues) page.

## ⭐ Star this Repository

If you find this framework helpful, please give it a star! ⭐

---

**Happy Testing!** 🚀
