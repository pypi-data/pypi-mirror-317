import pytest
from mathalgo2.Code import CodeBase, ClassicalCipher, ModernCipher
import os
from pathlib import Path
import base64

# 測試用的固定數據
@pytest.fixture
def sample_text():
    return "Hello World"

@pytest.fixture
def sample_chinese():
    return "你好世界"

@pytest.fixture
def sample_key():
    return "SECRET"

@pytest.fixture
def temp_file(tmp_path):
    file_path = tmp_path / "test.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("Test Content")
    return file_path

class TestCodeBase:
    """基礎編碼測試類"""

    def test_morse_encode_basic(self, sample_text):
        """測試基本的摩斯密碼編碼"""
        result = CodeBase.morse_encode("HELLO")
        assert result == ".... . .-.. .-.. ---"

    def test_morse_encode_special(self):
        """測試特殊情況的摩斯密碼編碼"""
        assert CodeBase.morse_encode("SOS") == "... --- ..."
        with pytest.raises(ValueError):
            CodeBase.morse_encode(None)

    def test_ascii_encode_decode(self, sample_text):
        """測試ASCII編碼和解碼的完整流程"""
        encoded = CodeBase.ascii_encode(sample_text)
        decoded = CodeBase.ascii_decode(encoded)
        assert decoded == sample_text

    def test_ascii_encode_chinese(self, sample_chinese):
        """測試中文ASCII編碼"""
        encoded = CodeBase.ascii_encode(sample_chinese)
        decoded = CodeBase.ascii_decode(encoded)
        assert decoded == sample_chinese

    def test_base64_encode_decode(self, sample_text):
        """測試Base64編碼和解碼"""
        encoded = CodeBase.base64_encode(sample_text)
        decoded = CodeBase.base64_decode(encoded)
        assert decoded == sample_text

    def test_base64_chinese(self, sample_chinese):
        """測試中文Base64編碼"""
        encoded = CodeBase.base64_encode(sample_chinese)
        decoded = CodeBase.base64_decode(encoded)
        assert decoded == sample_chinese

class TestClassicalCipher:
    """古典密碼測試類"""

    def test_caesar_basic(self, sample_text):
        """測試基本的凱薩密碼加解密"""
        encrypted = ClassicalCipher.caesar_encode(sample_text)
        decrypted = ClassicalCipher.caesar_decode(encrypted)
        assert decrypted == sample_text

    def test_caesar_chinese(self, sample_chinese):
        """測試中文凱薩密碼"""
        encrypted = ClassicalCipher.caesar_encode(sample_chinese)
        decrypted = ClassicalCipher.caesar_decode(encrypted)
        assert decrypted == sample_chinese

    @pytest.mark.parametrize("rails", [2, 3, 4])
    def test_rail_fence_different_rails(self, sample_text, rails):
        """測試不同柵欄數的柵欄密碼"""
        encrypted = ClassicalCipher.rail_fence_encode(sample_text, rails)
        decrypted = ClassicalCipher.rail_fence_decode(encrypted, rails)
        assert decrypted == sample_text

    def test_rail_fence_error(self):
        """測試柵欄密碼的錯誤處理"""
        with pytest.raises(ValueError):
            ClassicalCipher.rail_fence_encode("test", 1)

    def test_vigenere_basic(self, sample_text, sample_key):
        """測試基本的維吉尼亞密碼"""
        encrypted = ClassicalCipher.vigenere_encode(sample_text, sample_key)
        decrypted = ClassicalCipher.vigenere_decode(encrypted, sample_key)
        assert decrypted.upper() == sample_text.upper()

class TestModernCipher:
    """現代密碼測試類"""

    @pytest.fixture
    def rsa_keys(self):
        """生成RSA測試密鑰對"""
        return ModernCipher.generate_rsa_keys(1024)  # 使用較小的密鑰加快測試

    def test_rsa_basic(self, sample_text, rsa_keys):
        """測試基本的RSA加解密"""
        public_key, private_key = rsa_keys
        encrypted = ModernCipher.rsa_encrypt(sample_text, public_key, show_progress=False)
        decrypted = ModernCipher.rsa_decrypt(encrypted, private_key)
        assert decrypted == sample_text

    def test_aes_basic(self, sample_text):
        """測試基本的AES加解密"""
        encrypted, key = ModernCipher.aes_encrypt(sample_text, show_progress=False)
        decrypted = ModernCipher.aes_decrypt(encrypted, key)
        assert decrypted == sample_text

    def test_des_basic(self, sample_text):
        """測試基本的DES加解密"""
        encrypted, key = ModernCipher.des_encrypt(sample_text, show_progress=False)
        decrypted = ModernCipher.des_decrypt(encrypted, key)
        assert decrypted == sample_text

    def test_file_operations(self, temp_file, tmp_path):
        """測試檔案加密操作"""
        # 準備測試數據
        test_data = "Test encryption data"
        output_path = tmp_path / "encrypted.txt"
        key_path = tmp_path / "key.txt"

        # 測試保存加密檔案
        test_key = os.urandom(32)
        ModernCipher.save_encrypted_file(test_data, str(output_path), test_key)

        # 測試讀取加密檔案
        loaded_data, loaded_key = ModernCipher.load_encrypted_file(
            str(output_path),
            str(key_path)
        )
        assert loaded_data == test_data

    @pytest.mark.parametrize("cipher_type", ["aes", "des", "rsa"])
    def test_file_encryption(self, temp_file, tmp_path, cipher_type, rsa_keys):
        """測試不同加密方式的檔案加密"""
        output_path = tmp_path / f"encrypted_{cipher_type}.txt"
        
        if cipher_type == "rsa":
            public_key, _ = rsa_keys
            ModernCipher.rsa_encrypt_file(str(temp_file), public_key, str(output_path))
        elif cipher_type == "aes":
            ModernCipher.aes_encrypt_file(str(temp_file), output_file=str(output_path))
        else:  # des
            ModernCipher.des_encrypt_file(str(temp_file), output_file=str(output_path))
        
        assert output_path.exists()

@pytest.mark.slow
class TestPerformance:
    """性能測試類"""

    @pytest.mark.parametrize("size", [100, 1000, 10000])
    def test_encryption_performance(self, size):
        """測試不同大小數據的加密性能"""
        data = "A" * size
        
        # 測試各種加密方法的性能
        ClassicalCipher.caesar_encode(data)
        ClassicalCipher.rail_fence_encode(data, 3)
        ModernCipher.aes_encrypt(data, show_progress=False)

if __name__ == "__main__":
    pytest.main(["-v"]) 