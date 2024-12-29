# 🐾 ColorPaws

A powerful, flexible logging component that enhances Python's built-in logging with colored output and automated file organization. Perfect for both console applications and services requiring detailed logging.

## 🌟 Key Features

- 🎨 Colored console output with intuitive level-based colors
- 🖥️ Cross-platform support (Windows and Unix-like systems)
- 📁 Automatic date-based log file organization
- 🔄 Smart handler management (no duplicates)
- ⚙️ Configurable dual-output (console and/or file)
- 🕒 Timestamp-based log file naming

## 🎨 Color Scheme

| Log Level | Color    | Use Case |
|-----------|----------|----------|
| DEBUG     | Blue     | Detailed information for debugging |
| INFO      | Green    | General operational messages |
| WARNING   | Yellow   | Warning messages for potential issues |
| ERROR     | Red      | Error messages for serious problems |
| CRITICAL  | Magenta  | Critical failures requiring immediate attention |

## 📘 Usage Examples

### Basic Console Logging

```python
from colorpaws import setup_logger

# Initialize with console output only
logger = setup_logger(
    name="MyApp",
    log_on=True
)

# Example usage
logger.info("Application started")
logger.debug("Configuration loaded successfully")
logger.warning("Resource usage above 80%")
```

### Advanced File and Console Logging

```python
from colorpaws import setup_logger

# Initialize with both console and file logging
logger = setup_logger(
name="MyApp",
log_on=True,
log_to="logs"
)

# Comprehensive logging example
try:
    # Your code here
    logger.info("Processing started")
    logger.debug("Loading configuration...")

    # Simulate an error condition
    raise ValueError("Invalid input detected")

except Exception as e:
    logger.error(f"Process failed: {str(e)}")
    logger.debug("Stack trace:", exc_info=True)
```

## 📁 Log File Organization

The component automatically organizes log files by date:

```
logs/
├── 2024-01-01/
│   ├── 20240101_12000000_MyApp.log
│   ├── 20240101_12000001_MyApp.log
│   └── ...
```

## ⚙️ Configuration

### setup_logger() Parameters

| Parameter    | Type    | Default | Description |
|-------------|---------|---------|-------------|
| name        | str     | Required| Logger instance name |
| log_on      | bool    | False   | Enable/disable logging |
| log_to      | str     | None    | Log file directory path |

## 🛠️ Installation

```bash
pip install colorpaws
```

## 🔍 Advanced Features

### Handler Management
- Automatic prevention of duplicate handlers
- Smart console color detection
- Windows-specific color handling via colorama

### Log File Naming
- Timestamp-based unique file names
- Date-based directory structure
- Append mode for continuous logging

### Format Customization
Default format: `YYYY-MM-DD HH:MM:SS - LEVEL - Message`

## 💡 Best Practices

1. **Logger Naming**
   ```python
   # Use meaningful, hierarchical names
   logger = setup_logger("MyApp.SubModule")
   ```

2. **Log Level Usage**
   ```python
   logger.debug("Detailed debugging information")
   logger.info("General operational messages")
   logger.warning("Warning messages")
   logger.error("Error messages")
   logger.critical("Critical failures")
   ```

3. **Exception Handling**
   ```python
   try:
       # Your code
   except Exception as e:
       logger.error("Operation failed", exc_info=True)
   ```

## ⚠️ Important Notes

- Log files are created with unique timestamps to prevent overwrites
- Console colors automatically adjust based on terminal capabilities
- Windows color support is handled transparently
- Logger instances are singleton per name
- All timestamps use local system time

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This component is available under the MIT License.
