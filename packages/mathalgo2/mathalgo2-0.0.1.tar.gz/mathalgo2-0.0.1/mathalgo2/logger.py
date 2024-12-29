import logging
import os
from pathlib import Path

def setup_logger(name: str, log_file: str, level=logging.INFO) -> logging.Logger:
    """Setup and return a logger instance"""
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Add handlers only if they don't exist
    if not logger.handlers:
        # File handler
        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setLevel(level)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger 