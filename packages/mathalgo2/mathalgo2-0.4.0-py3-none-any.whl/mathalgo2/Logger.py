import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Union, Dict

__all__ = [
    "Logger"
]

class Logger:
    """
    一個全面的日誌管理類，提供進階的日誌記錄功能。
    
    功能特點：
    - 支持多種輸出格式
    - 同時支持文件和控制台日誌
    - 日誌檔案輪轉
    - 自定義日誌級別
    - 異常日誌記錄
    - 性能日誌記錄
    """
    
    # 預設的日誌格式
    DEFAULT_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    # 詳細的日誌格式
    DETAILED_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    
    def __init__(
        self,
        name: str,
        log_file: str,
        level: int = logging.INFO,
        format_string: Optional[str] = None,
        rotation_size: int = 1024 * 1024,  # 1MB
        backup_count: int = 5,
        console_output: bool = True
    ):
        """
        初始化日誌管理器，設置進階配置選項。
        
        參數：
            name (str): 日誌記錄器名稱
            log_file (str): 日誌文件路徑
            level (int): 日誌級別（預設：logging.INFO）
            format_string (str, optional): 自定義日誌消息格式
            rotation_size (int): 觸發日誌輪轉的文件大小（預設：1MB）
            backup_count (int): 保留的備份文件數量
            console_output (bool): 是否輸出到控制台
        """
        self.name = name
        self.log_file = log_file
        self.level = level
        self.format_string = format_string or self.DEFAULT_FORMAT
        self.rotation_size = rotation_size
        self.backup_count = backup_count
        self.console_output = console_output
        self.logger = self._setup_logger()
        self._start_time = datetime.now()
        
        # 添加標準日誌級別方法
        self.debug = self.logger.debug
        self.info = self.logger.info
        self.warning = self.logger.warning
        self.error = self.logger.error
        self.critical = self.logger.critical
        self.exception = self.logger.exception
        
    def _create_log_directory(self) -> None:
        """創建日誌目錄（如果不存在）"""
        log_dir = os.path.dirname(self.log_file)
        Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    def _create_formatter(self, format_string: Optional[str] = None) -> logging.Formatter:
        """
        創建並返回日誌格式化器
        
        參數：
            format_string (str, optional): 自定義格式字符串
        
        返回：
            logging.Formatter: 配置好的格式化器實例
        """
        return logging.Formatter(
            format_string or self.format_string,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    def _setup_handler(
        self,
        handler: logging.Handler,
        format_string: Optional[str] = None
    ) -> logging.Handler:
        """
        設置處理器的格式化器和級別
        
        參數：
            handler (logging.Handler): 要設置的處理器實例
            format_string (str, optional): 此處理器的自定義格式字符串
        
        返回：
            logging.Handler: 配置好的處理器實例
        """
        handler.setLevel(self.level)
        handler.setFormatter(self._create_formatter(format_string))
        return handler
    
    def _setup_logger(self) -> logging.Logger:
        """
        設置並返回帶有所有配置處理器的日誌記錄器實例
        
        返回：
            logging.Logger: 配置好的日誌記錄器實例
        """
        self._create_log_directory()
        
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        
        # 清除現有的處理器
        logger.handlers = []
        
        # 設置輪轉文件處理器
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(
            self.log_file,
            maxBytes=self.rotation_size,
            backupCount=self.backup_count,
            encoding='utf-8'
        )
        logger.addHandler(self._setup_handler(file_handler))
        
        # 如果啟用，設置控制台處理器
        if self.console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            logger.addHandler(self._setup_handler(console_handler))
        
        return logger
    
    def get_logger(self) -> logging.Logger:
        """返回配置好的日誌記錄器實例"""
        return self.logger
    
    def set_level(self, level: Union[int, str]) -> None:
        """
        更改日誌級別
        
        參數：
            level: 新的日誌級別（可以是整數或字符串）
        """
        if isinstance(level, str):
            level = getattr(logging, level.upper())
        self.level = level
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)
    
    def add_custom_level(self, level_name: str, level_num: int) -> None:
        """
        添加自定義日誌級別
        
        參數：
            level_name (str): 自定義級別名稱
            level_num (int): 級別對應的數值
        """
        # 添加新的日誌級別到 logging 模組
        logging.addLevelName(level_num, level_name.upper())
        
        # 創建新的日誌方法
        def custom_log(message, *args, **kwargs):
            if self.logger.isEnabledFor(level_num):
                self.logger._log(level_num, message, args, **kwargs)
        
        # 將新方法添加到 logger 實例
        setattr(self.logger, level_name.lower(), custom_log)
        
        # 確保所有處理器都接受新的級別
        for handler in self.logger.handlers:
            handler.setLevel(min(handler.level, level_num))
    
    def log_exception(self, exc: Exception, additional_info: Dict = None) -> None:
        """
        記錄異常信息及可選的附加上下文
        
        參數：
            exc (Exception): 要記錄的異常
            additional_info (dict, optional): 附加的上下文信息
        """
        error_message = f"發生異常: {str(exc)}"
        if additional_info:
            error_message += f"\n附加信息: {additional_info}"
        self.logger.exception(error_message)
    
    def get_performance_stats(self) -> Dict:
        """
        獲取基本性能統計信息
        
        返回：
            dict: 包含性能指標的字典
        """
        return {
            'start_time': self._start_time,
            'uptime': datetime.now() - self._start_time,
            'log_file_size': os.path.getsize(self.log_file) if os.path.exists(self.log_file) else 0
        } 