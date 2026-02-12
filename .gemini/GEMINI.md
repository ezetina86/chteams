# CHTEAMS Project Standards and Guidelines

This document outlines the architectural patterns, coding styles, and best practices established for the chteams utility. Adherence to these standards ensures maintainability, stability, and high quality.

## Code Style

1. Modular Architecture: All core logic resides within the src/chteams directory. Each module must have a single, well-defined responsibility (e.g., macos.py for system interactions, ui.py for presentation).
2. Type Hinting: Mandatory use of Python type hints for all function signatures and class attributes to improve clarity and catch potential errors early.
3. Docstrings: All classes and functions must include Google-style docstrings. They should describe purpose, arguments, return values, and any raised exceptions.
4. Linting and Formatting: The project uses ruff for consistency. Code must pass ruff check and ruff format before being committed.
5. Naming Conventions: Use snake_case for functions and variables, and PascalCase for classes. Internal methods should be prefixed with a single underscore.

## Best Practices

1. Non-blocking Operations: Time-consuming or blocking operations (like waiting for user input) must be handled in dedicated threads to prevent the main execution loop from hanging.
2. Separation of Concerns: Keep platform-specific commands (AppleScript, subprocess) isolated from the core engine logic to facilitate future cross-platform support.
3. Resource Management: Always ensure system resources are released. Use try/finally blocks or context managers to stop background processes like caffeinate and input threads.
4. Command Line Interface: Use argparse for robust handling of flags and arguments.

## Testing

1. Framework: The project uses pytest.
2. Mocking: System-level interactions (subprocess, threads, standard input) must be mocked using unittest.mock to ensure tests are fast, deterministic, and environment-independent.
3. Coverage: Aim for high test coverage (minimum 80%). Use pytest-cov to monitor coverage metrics.
4. Test Structure: Mirror the src directory structure in the tests directory. Each source module should have a corresponding test_*.py file.
5. Hanging Prevention: When testing threads or infinite loops, ensure that termination events are correctly triggered and that no blocking calls like input() are executed without mocking.

## Logging

1. Standard Library: Use the standard logging module.
2. Levels:
    - INFO: For general progress and user-facing status updates.
    - DEBUG: For detailed execution flow and diagnostic information (enabled via --debug).
    - WARNING/ERROR: For recoverable issues and failed operations.
    - CRITICAL: For fatal errors that require application shutdown.
3. Formatting: Logs must include timestamps and severity levels for easier troubleshooting.
4. UI Compatibility: In live mode, use the rich library for visual feedback. In debug mode, revert to a standard log stream to prevent UI refreshes from hiding diagnostic data.

## Security

1. Principle of Least Privilege: Only request the permissions necessary for operation. Document any manual security steps (like macOS Accessibility permissions) clearly in the README.
2. System Interactions: Use capture_output=True and check=True when running subprocesses to handle errors safely and prevent unexpected output leaks.
3. Privacy and User Experience: When stealing focus for an automated action, always restore focus to the previously active application immediately to minimize disruption to the user.
4. Data Handling: Avoid logging any sensitive information. The project should never store or commit secrets or personal data.
