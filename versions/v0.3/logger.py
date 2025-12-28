"""
Logging configuration for MZ
"""
import logging
import os
from config import load_config

def setup_logging():
    """
    Setup logging system based on config.
    
    Returns:
        Configured logger object
    """
    # Load config
    config = load_config()
    log_config = config['logging']
    
    # Get log level from config
    log_level_str = log_config['level']
    
    # Get log format from config
    log_format = log_config['format']

    # Get log file path from config
    log_file = log_config['file']

    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file) # Gets "logs" from "logs/mz.log"
    os.makedirs(log_dir, exist_ok=True) # Creates logs/ folder if doesn't exist 

    # Configure logging with:
    # - level
    # - format
    # - handlers (file and console)
    log_level = getattr(logging, log_level_str) # Converts "INFO" to logging.INFO

    logging .basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file), # Write to file
            logging.StreamHandler()        # Also print to console
        ]
    )
    
    # Create and return logger
    logger = logging.getLogger('MZ')
    return logger
    