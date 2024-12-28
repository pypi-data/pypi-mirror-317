# print_helper_logger

`print_helper_logger` provides a `Print_Helper` class for printing messages to the console and the system logger, with options for using timestamps, colored messages, and different severity levels.

## Features

- Print messages with different severity levels: CRITICAL, ERROR, WARNING, INFO, DEBUG.
- Options to include timestamps in messages.
- Colored messages for better visual clarity.
- Log messages to a log file.
- print` function that automatically determines the severity level of the message based on tags included in the message text: <crt>, <err>, <wrn>, <inf> and <dbg>.

## Installation

You can install the package using pip once it's published on PyPI:
git
```bash
pip install print_helper_logger
```

## Usage

```python
from print_helper_logger import Print_Helper, Severity_Level

# Create an instance of Print_Helper
ph = Print_Helper(
    severity_level=Severity_Level.INFO, 
    show_color=True, 
    show_timestamp=True, 
    show_logger=True, 
    filename_logger="log.txt"
)

# Print messages with different severity levels
ph.print_crt("This is a critical message")
ph.print_err("This is an error message")
ph.print_wrn("This is a warning message")
ph.print_inf("This is an informational message")
ph.print_dbg("This is a debug message")
```
