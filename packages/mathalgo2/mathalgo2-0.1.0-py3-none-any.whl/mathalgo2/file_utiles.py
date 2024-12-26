import os

class FileUtils:
    @staticmethod
    def read_file(file_path: str) -> str:
        """讀取檔案內容，返回為字串。"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"檔案未找到: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    @staticmethod
    def write_file(file_path: str, content: str) -> None:
        """將內容寫入檔案。"""
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)


