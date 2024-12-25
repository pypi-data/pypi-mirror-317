## cyberCore

cyberCore is a high-performance and secure framework designed for building scalable applications. It provides developers with essential tools and libraries to streamline development, enhance security, and improve code maintainability. With support for modern programming paradigms, cyberCore aims to empower developers to focus on delivering robust solutions quickly.

Key Features:
- Security-First Approach: Built-in security measures to prevent common vulnerabilities.
- Scalability: Optimized to handle high loads and large-scale applications.
- Modularity: Highly modular architecture, allowing seamless integration and customization.
- Ease of Use: Developer-friendly APIs and comprehensive documentation.

Goals:
- Accelerate development time while maintaining high code quality.
- Provide a flexible foundation to meet diverse application needs.
- Ensure application security without compromising performance.

---

## Installation

To install `cyberCore`, use pip:

 ```bash
 pip install cyberCore
 ```

---

### **_CustomLogging:_**

```python
from cyberCore.CustomLogging import logger

if __name__ == '__main__':
    """Logs a message using the specified log level."""
    logger.debug(f'Provides detailed information that’s valuable to you as a developer.')
    logger.info(f'Provides general information about what’s going on with your program.')
    logger.warning(f'Indicates that there’s something you should look into.')
    logger.error(f'Alerts you to an unexpected problem that’s occured in your program.')
    logger.critical(f'Tells you that a serious error has occurred and may have crashed your app.')
```

#### **_output_**

```shell
cyberCore | DEBUG    | Provides detailed information that’s valuable to you as a developer.
cyberCore | INFO     | Provides general information about what’s going on with your program.
cyberCore | WARNING  | Indicates that there’s something you should look into.
cyberCore | ERROR    | Alerts you to an unexpected problem that’s occured in your program.
cyberCore | CRITICAL | Tells you that a serious error has occurred and may have crashed your app.
```

---

### **_ConfigSettings:_**

```python
import json
from cyberCore.ConfigSettings import settings, settings_not_set
from cyberCore.CustomLogging import logger

# Constants
FORMAT_PADDING = 25
FORMAT_LOG_MESSAGE = '{setting:>{padding}}: {value}'
SEPARATOR_LINE = "-" * 160

def log_sorted_settings(system_settings):
    """Logs the key-value pairs of sorted settings."""
    for setting_name, setting_value in system_settings:
        logger.info(f'{setting_name:>{FORMAT_PADDING}}: {setting_value}')

def log_unset_settings(system_settings):
    """Logs unset settings with different log levels based on their required level."""
    for setting in system_settings:
        setting_value = json.loads(settings_not_set[setting])
        message = FORMAT_LOG_MESSAGE.format(setting=setting, value=setting_value, padding=FORMAT_PADDING)
        match setting_value["settingRequired"]["level"]:
            case "CRITICAL":
                logger.critical(message)
            case "ERROR":
                logger.error(message)
            case "WARNING":
                logger.warning(message)
            case _:
                logger.info(message)

if __name__ == '__main__':
    # Log sorted settings
    sorted_settings = sorted(settings)
    log_sorted_settings(sorted_settings)

    # Log unset settings
    sorted_keys = sorted(settings_not_set)
    log_unset_settings(sorted_keys)
```

#### **_output_**

```shell
cyberCore | INFO     |          ENVIRONMENT: Local
cyberCore | INFO     |               FN_KEY: {key}
cyberCore | INFO     |          LOG_APPNAME: cyberCore
cyberCore | INFO     |           LOG_FORMAT: {extra[app]} | <level>{level: <8}</level> | <cyan><level>{message}</level></cyan>
cyberCore | INFO     |    LOG_INC_RESP_BODY: f
cyberCore | INFO     |            LOG_LEVEL: DEBUG
cyberCore | INFO     |       MSSQL_DATABASE: {default_database}
cyberCore | INFO     |       MSSQL_HOSTNAME: {hostname}
cyberCore | INFO     |       MSSQL_PASSWORD: {password}
cyberCore | INFO     |           MSSQL_PORT: {port}
cyberCore | INFO     |          MSSQL_TRUST: {trust}
cyberCore | INFO     |       MSSQL_USERNAME: {username}
cyberCore | INFO     |         PROJECT_ROOT: /Users/rjd/GitHub/PyCharm/testCyberCore
cyberCore | INFO     |            SETTING_1: value_1
cyberCore | INFO     |            SETTING_2: value_2
```

---

### **_Encryption:_**

```python
from cyberCore.CustomLogging import logger
from cyberCore.Encryption import Encryption

# Constants
FORMAT_PADDING = 20
WELCOME_MESSAGE = "Welcome to the cyberCore!"

def log_formatted(key, value):
    """Helper to standardize log output."""
    logger.info(f'{key:>{FORMAT_PADDING}}: {value}')

if __name__ == '__main__':
    encryption_service = Encryption()

    # Log encryption key
    encryption_key = encryption_service.key.decode()
    log_formatted("Key", encryption_key)

    # Encrypt and log
    encrypted_message = encryption_service.encrypt(WELCOME_MESSAGE).decode()
    log_formatted("Encrypt", f"{WELCOME_MESSAGE} -> {encrypted_message}")

    # Decrypt and log
    decrypted_message = encryption_service.decrypt(encrypted_message)
    log_formatted("Decrypt", f"{encrypted_message} -> {decrypted_message}")
```

#### **_output_**
```shell
cyberCore | INFO     |                  Key: l911...UbP4=
cyberCore | INFO     |              Encrypt: Welcome to the cyberCore! -> gAAAAABna04F3P6S6eARPSEHgiCSPmixKnergtRf75SyDPVXd8tMOeBv5m02buuT3cP0-1MNDP_OY5pEEuFIRn9MJiePZgESBpKzS5HD_R-rVYb7g_cbnmQ=
cyberCore | INFO     |              Decrypt: gAAAAABna04F3P6S6eARPSEHgiCSPmixKnergtRf75SyDPVXd8tMOeBv5m02buuT3cP0-1MNDP_OY5pEEuFIRn9MJiePZgESBpKzS5HD_R-rVYb7g_cbnmQ= -> Welcome to the cyberCore!
```

---

## **_HttpRest:_**
```python
from cyberCore.CustomLogging import logger
from cyberCore.HttpRest import HttpRest, HttpAction

# Constants
FORMAT_PADDING = 15
INDENTATION_LEVEL = 4
DEFAULT_HEADERS = {"Custom-Header": "value"}


def make_request_and_log(http_rest, action, url):
    """Make an HTTP request and log the result."""
    result, status_code = http_rest.http_request(action, url, DEFAULT_HEADERS)
    logger.info(f'{status_code} - {result}')


if __name__ == '__main__':
    rest_api = HttpRest()

    # List of requests to perform
    requests = [
        (HttpAction.GET, "https://httpbin.org/get"),
        (HttpAction.POST, "https://httpbin.org/post"),
        (HttpAction.PATCH, "https://httpbin.org/patch"),
    ]

    # Process request
    for action, url in requests:
        make_request_and_log(rest_api, action, url)
```

### **_output_**

```shell
cyberCore | INFO     | 200 - {
  "args": {}, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Custom-Header": "value", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.32.3", 
    "X-Amzn-Trace-Id": "Root=1-676b6675-79001edf69c8245a0128421a"
  }, 
  "origin": "185.187.171.99", 
  "url": "https://httpbin.org/get"
}

cyberCore | INFO     | 200 - {
  "args": {}, 
  "data": "", 
  "files": {}, 
  "form": {}, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Content-Length": "0", 
    "Custom-Header": "value", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.32.3", 
    "X-Amzn-Trace-Id": "Root=1-676b6675-58c7fe7b1527fa04719687ac"
  }, 
  "json": null, 
  "origin": "185.187.171.99", 
  "url": "https://httpbin.org/post"
}

cyberCore | INFO     | 200 - {
  "args": {}, 
  "data": "", 
  "files": {}, 
  "form": {}, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Content-Length": "0", 
    "Custom-Header": "value", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.32.3", 
    "X-Amzn-Trace-Id": "Root=1-676b6675-3460a1cb5653a05d127a7b93"
  }, 
  "json": null, 
  "origin": "185.187.171.99", 
  "url": "https://httpbin.org/patch"
}
```
---

### **_PyVersions:_**

```python
import json
from cyberCore.CustomLogging import logger
from cyberCore.PyVersions import PyVersions

# Constants
FORMAT_PADDING = 15
INDENTATION_LEVEL = 4

def log_formatted(key, value):
    """Standardize log output."""
    logger.info(f'{key:>{FORMAT_PADDING}}: {value}')

def log_json(key, data):
    """Log JSON formatted data."""
    formatted_data = json.dumps(data, indent=INDENTATION_LEVEL)
    log_formatted(key, formatted_data)

def log_py_versions(py_versions):
    """Log Python versions and releases."""
    log_json("pyVersions", py_versions.versions)
    log_json("pyReleases", py_versions.releases)

if __name__ == '__main__':
    try:
        py_versions = PyVersions()
        log_py_versions(py_versions)
    except Exception as e:
        logger.error(f'{"pyVersions":>{FORMAT_PADDING}}: {e}')
```

#### **_output_**

```shell
cyberCore | INFO     |      pyVersions: [
    {
        "version": "3.13",
        "status": "bugfix",
        "released": "2024-10-07",
    }
]
cyberCore | INFO     |     pyReleases: [
    {
        "version": "3.13.1",
        "released": "2024-12-15",
    }
]
```



