"""
Logging utilities for advanced honeypot system
"""

import logging
import sys
from datetime import datetime
from typing import Optional


def setup_logger(
    name: str = "honeypot",
    level: int = logging.INFO,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Setup logger with consistent formatting
    
    Args:
        name: Logger name
        level: Logging level
        log_file: Optional log file path
    
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers = []
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get existing logger or create new one
    
    Args:
        name: Logger name
    
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class StructuredLogger:
    """
    Structured logging with context
    """
    
    def __init__(self, name: str):
        """Initialize structured logger"""
        self.logger = get_logger(name)
        self.context = {}
    
    def set_context(self, **kwargs):
        """Set logging context"""
        self.context.update(kwargs)
    
    def clear_context(self):
        """Clear logging context"""
        self.context = {}
    
    def _format_message(self, message: str) -> str:
        """Format message with context"""
        if self.context:
            context_str = " | ".join(f"{k}={v}" for k, v in self.context.items())
            return f"{message} | {context_str}"
        return message
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        self.logger.info(self._format_message(message), **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self.logger.warning(self._format_message(message), **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        self.logger.error(self._format_message(message), **kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self.logger.debug(self._format_message(message), **kwargs)


# Example usage
if __name__ == "__main__":
    # Basic logger
    logger = setup_logger("test", level=logging.DEBUG)
    logger.info("Test info message")
    logger.warning("Test warning message")
    logger.error("Test error message")
    
    # Structured logger
    struct_logger = StructuredLogger("test_struct")
    struct_logger.set_context(session_id="123", user="test")
    struct_logger.info("Processing request")
    struct_logger.clear_context()
