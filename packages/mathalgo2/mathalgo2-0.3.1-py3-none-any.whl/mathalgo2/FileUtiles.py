import os
from pathlib import Path
from mathalgo2.logger import setup_logger, logging

"""
# 檔案工具模組

提供檔案讀寫相關的工具函數。

## 主要功能
- 讀取檔案內容
- 寫入檔案內容
- 檔案操作日誌記錄
"""

# 獲取當前文件所在目錄的根目錄
ROOT_DIR = Path(__file__).parent.parent

# 設置日誌文件路徑
log_file = os.path.join(ROOT_DIR, "__log__", "file_utiles.log")
logger = setup_logger("file_utiles", log_file, level=logging.INFO)

class FileUtils:
    """檔案工具類別，提供檔案讀寫功能"""
    
    @staticmethod
    def read_file(file_path: str) -> str:
        """
        # 讀取檔案內容
        
        ## 參數
        * file_path: 檔案路徑
        
        ## 返回
        * str: 檔案內容字串
        
        ## 異常
        * FileNotFoundError: 當檔案不存在時拋出
        """
        logger.info(f"嘗試讀取檔案: {file_path}")
        
        if not os.path.exists(file_path):
            logger.error(f"檔案未找到: {file_path}")
            raise FileNotFoundError(f"檔案未找到: {file_path}")
            
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                logger.info(f"成功讀取檔案: {file_path}")
                return content
        except Exception as e:
            logger.error(f"讀取檔案時發生錯誤: {str(e)}")
            raise
    
    @staticmethod
    def write_file(file_path: str, content: str) -> None:
        """
        # 將內容寫入檔案
        
        ## 參數
        * file_path: 檔案路徑
        * content: 要寫入的內容
        
        ## 異常
        * IOError: 當寫入失敗時拋出
        """
        logger.info(f"嘗試寫入檔案: {file_path}")
        
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
                logger.info(f"成功寫入檔案: {file_path}")
        except Exception as e:
            logger.error(f"寫入檔案時發生錯誤: {str(e)}")
            raise

__all__ = [
    "FileUtils"
]

