import pytest
import logging
import os
import time
from pathlib import Path
from mathalgo2.Logger import Logger

class TestLogger:
    @pytest.fixture
    def test_log_file(self, tmp_path):
        """創建臨時日誌文件路徑"""
        return str(tmp_path / "test.log")
    
    @pytest.fixture
    def logger(self, test_log_file):
        """創建測試用 Logger 實例"""
        return Logger(
            name="test_logger",
            log_file=test_log_file,
            level=logging.DEBUG,
            console_output=False
        )
    
    def test_logger_initialization(self, logger, test_log_file):
        """測試 Logger 初始化"""
        assert logger.name == "test_logger"
        assert logger.log_file == test_log_file
        assert logger.level == logging.DEBUG
        assert isinstance(logger.logger, logging.Logger)
        
    def test_log_directory_creation(self, tmp_path):
        """測試日誌目錄創建"""
        log_dir = tmp_path / "logs"
        log_file = str(log_dir / "test.log")
        
        logger = Logger("test", log_file)
        assert log_dir.exists()
        
    def test_logging_levels(self, logger, test_log_file):
        """測試不同日誌級別"""
        messages = {
            'debug': 'Debug message',
            'info': 'Info message',
            'warning': 'Warning message',
            'error': 'Error message',
            'critical': 'Critical message'
        }
        
        # 寫入不同級別的日誌
        for level, message in messages.items():
            getattr(logger, level)(message)
            
        # 檢查日誌文件內容
        with open(test_log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            for message in messages.values():
                assert message in content
                
    def test_set_level(self, logger):
        """測試設置日誌級別"""
        # 使用字符串設置
        logger.set_level('ERROR')
        assert logger.level == logging.ERROR
        
        # 使用整數設置
        logger.set_level(logging.DEBUG)
        assert logger.level == logging.DEBUG
        
    def test_custom_level(self, logger):
        """測試自定義日誌級別"""
        # 添加自定義級別
        custom_level = 15  # 在 DEBUG(10) 和 INFO(20) 之間
        logger.add_custom_level('TRACE', custom_level)
        
        # 創建測試消息
        test_message = "This is a trace message"
        
        # 確保日誌級別足夠低
        logger.set_level(logging.DEBUG)
        
        # 使用自定義級別記錄消息
        if hasattr(logger.logger, 'trace'):
            logger.logger.trace(test_message)
        
        # 確保所有處理器都刷新緩衝區
        for handler in logger.logger.handlers:
            handler.flush()
        
        # 給文件系統一些時間來寫入
        import time
        time.sleep(0.1)
        
        # 讀取並驗證日誌內容
        with open(logger.log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"Log file content: {content}")  # 調試輸出
            print(f"Log file exists: {os.path.exists(logger.log_file)}")  # 檢查文件是否存在
            print(f"Log file size: {os.path.getsize(logger.log_file)}")   # 檢查文件大小
            
            assert test_message in content, "消息未被寫入日誌文件"
            assert 'TRACE' in content, "TRACE 級別標記未出現在日誌中"
            
    def test_log_rotation(self, tmp_path):
        """測試日誌輪轉"""
        log_file = str(tmp_path / "rotation_test.log")
        small_size = 100  # 設置較小的輪轉大小用於測試
        
        logger = Logger(
            name="rotation_test",
            log_file=log_file,
            rotation_size=small_size,
            backup_count=2
        )
        
        # 寫入足夠大的日誌觸發輪轉
        long_message = "x" * 50
        for _ in range(10):
            logger.info(long_message)
            
        # 檢查是否創建了備份文件
        log_dir = Path(log_file).parent
        backup_files = list(log_dir.glob("rotation_test.log.*"))
        assert len(backup_files) > 0
        
    def test_log_exception(self, logger, test_log_file):
        """測試異常日誌記錄"""
        try:
            raise ValueError("Test exception")
        except ValueError as e:
            logger.log_exception(e, {"context": "test"})
            
        with open(test_log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "Test exception" in content
            assert "context" in content
            assert "Traceback" in content
            
    def test_performance_stats(self, logger):
        """測試性能統計"""
        time.sleep(0.1)  # 確保有一些運行時間
        stats = logger.get_performance_stats()
        
        assert 'start_time' in stats
        assert 'uptime' in stats
        assert 'log_file_size' in stats
        assert stats['log_file_size'] >= 0
        
    def test_detailed_format(self, tmp_path):
        """測試詳細日誌格式"""
        log_file = str(tmp_path / "detailed.log")
        logger = Logger(
            name="detailed_test",
            log_file=log_file,
            format_string=Logger.DETAILED_FORMAT
        )
        
        logger.info("Test message")
        
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "test_logger.py" in content
            assert "Test message" in content
            
    def test_console_output(self, capsys, tmp_path):
        """測試控制台輸出"""
        log_file = str(tmp_path / "console_test.log")
        logger = Logger(
            name="console_test",
            log_file=log_file,
            console_output=True
        )
        
        test_message = "Console test message"
        logger.info(test_message)
        
        captured = capsys.readouterr()
        assert test_message in captured.out 