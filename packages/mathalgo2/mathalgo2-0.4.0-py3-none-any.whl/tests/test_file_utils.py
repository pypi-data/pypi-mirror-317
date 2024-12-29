import pytest
import os
import json
import shutil
import numpy as np
import pandas as pd
from pathlib import Path
from PIL import Image
from mathalgo2.FileUtiles import FileIO, FileProcessor, DataAnalyzer

# ====== Fixtures ======
@pytest.fixture
def test_dir(tmp_path):
    """創建臨時測試目錄"""
    return tmp_path

@pytest.fixture
def test_files(test_dir):
    """創建測試用的檔案"""
    # 創建文本文件
    text_file = test_dir / "test.txt"
    text_file.write_text("Hello, World!")
    
    # 創建 JSON 文件
    json_file = test_dir / "test.json"
    json_file.write_text('{"key": "value"}')
    
    # 創建 CSV 文件
    csv_file = test_dir / "test.csv"
    pd.DataFrame({'A': [1, 2], 'B': ['x', 'y']}).to_csv(csv_file, index=False)
    
    return {
        'text': text_file,
        'json': json_file,
        'csv': csv_file
    }

@pytest.fixture
def sample_df():
    """創建測試用的 DataFrame"""
    np.random.seed(42)
    return pd.DataFrame({
        'numeric': np.random.normal(0, 1, 100),
        'category': np.random.choice(['A', 'B', 'C'], 100),
        'missing': np.random.choice([1, np.nan], 100)
    })

# ====== FileIO Tests ======
class TestFileIO:
    def test_read_file_success(self, test_files):
        """測試成功讀取文本文件"""
        content = FileIO.read_file(str(test_files['text']))
        assert content == "Hello, World!"
        
    def test_read_file_with_encoding(self, test_dir):
        """測試使用不同編碼讀取文件"""
        file_path = test_dir / "encoded.txt"
        content = "測試中文"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        assert FileIO.read_file(str(file_path), encoding='utf-8') == content
        
    def test_read_nonexistent_file(self):
        """測試讀取不存在的文件"""
        with pytest.raises(FileNotFoundError):
            FileIO.read_file("nonexistent.txt")
            
    def test_write_file_success(self, test_dir):
        """測試成功寫入文件"""
        file_path = test_dir / "output.txt"
        content = "Test content"
        FileIO.write_file(str(file_path), content)
        
        assert file_path.read_text() == content
        
    def test_json_operations(self, test_dir):
        """測試 JSON 操作"""
        file_path = test_dir / "test.json"
        test_data = {"name": "test", "values": [1, 2, 3]}
        
        # 測試寫入
        FileIO.write_json(str(file_path), test_data)
        
        # 測試讀取
        loaded_data = FileIO.read_json(str(file_path))
        assert loaded_data == test_data
        
    def test_csv_operations(self, test_dir):
        """測試 CSV 操作"""
        file_path = test_dir / "test.csv"
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': ['x', 'y', 'z']
        })
        
        # 測試寫入
        FileIO.write_csv(str(file_path), df)
        
        # 測試讀取
        loaded_df = FileIO.read_csv(str(file_path))
        pd.testing.assert_frame_equal(loaded_df, df)
        
    def test_list_files(self, test_files):
        """測試列出目錄文件"""
        files = FileIO.list_files(str(test_files['text'].parent))
        assert len(files) == 3  # text, json, csv
        assert any('test.txt' in f for f in files)

# ====== FileProcessor Tests ======
class TestFileProcessor:
    def test_compression_operations(self, test_files, test_dir):
        """測試壓縮和解壓縮操作"""
        processor = FileProcessor()
        zip_path = test_dir / "archive.zip"
        extract_path = test_dir / "extracted"
        
        # 測試壓縮
        processor.compress_files(
            [str(f) for f in test_files.values()],
            str(zip_path)
        )
        assert zip_path.exists()
        
        # 測試解壓縮
        processor.extract_files(str(zip_path), str(extract_path))
        assert (extract_path / "test.txt").exists()
        
    def test_encryption_operations(self, test_files):
        """測試加密和解密操作"""
        processor = FileProcessor()
        encrypted_path = test_files['text'].parent / "encrypted.bin"
        decrypted_path = test_files['text'].parent / "decrypted.txt"
        
        # 測試加密
        processor.encrypt_file(str(test_files['text']), str(encrypted_path))
        assert encrypted_path.exists()
        
        # 測試解密
        processor.decrypt_file(str(encrypted_path), str(decrypted_path))
        assert decrypted_path.read_text() == test_files['text'].read_text()
        
    def test_backup_operations(self, test_files):
        """測試文件備份"""
        processor = FileProcessor()
        backup_path = processor.backup_file(str(test_files['text']))
        assert Path(backup_path).exists()
        
# ====== DataAnalyzer Tests ======
class TestDataAnalyzer:
    def test_analyze_data(self, sample_df):
        """測試數據分析"""
        results = DataAnalyzer.analyze_data(sample_df)
        
        assert 'summary' in results
        assert 'missing' in results
        assert 'shape' in results
        assert results['shape'] == (100, 3)
        
    def test_visualization(self, test_dir, sample_df):
        """測試數據視覺化"""
        plot_path = test_dir / "plot.png"
        
        # 測試直方圖
        DataAnalyzer.create_visualization(
            sample_df,
            'histogram',
            column='numeric',
            save_path=str(plot_path),
            show=False
        )
        assert plot_path.exists()
        
        # 測試散點圖
        plot_path = test_dir / "scatter.png"
        DataAnalyzer.create_visualization(
            sample_df,
            'scatter',
            x='numeric',
            y='numeric',
            save_path=str(plot_path),
            show=False
        )
        assert plot_path.exists()
        
    def test_data_processing(self, sample_df):
        """測試數據處理"""
        # 測試填充缺失值
        filled_df = DataAnalyzer.process_data(sample_df, 'fillna', value=0)
        assert not filled_df['missing'].isnull().any()
        
        # 測試標準化
        normalized_df = DataAnalyzer.process_data(
            sample_df[['numeric']], 
            'normalize'
        )
        assert abs(normalized_df['numeric'].mean()) < 0.01
        assert abs(normalized_df['numeric'].std() - 1) < 0.01
        
        # 測試排序
        sorted_df = DataAnalyzer.process_data(
            sample_df, 
            'sort',
            column='numeric'
        )
        assert sorted_df['numeric'].is_monotonic_increasing 