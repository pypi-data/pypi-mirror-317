import logging
import os
from pathlib import Path

def setup_logger(name: str, log_file: str, level=logging.INFO) -> logging.Logger:
    """
    設置 logger
    
    Parameters:
        name (str): logger 名稱
        log_file (str): 日誌文件路徑
        level: 日誌等級
    """
    # 確保日誌目錄存在
    log_dir = os.path.dirname(log_file)
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    # 創建 logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 如果 logger 已經有處理器，則不添加新的處理器
    if not logger.handlers:
        # 創建 file handler
        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setLevel(level)
        
        # 創建 console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        
        # 創建 formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # 設置 formatter
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加 handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger
