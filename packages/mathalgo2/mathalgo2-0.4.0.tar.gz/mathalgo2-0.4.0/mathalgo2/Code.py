from typing import List, Union, Dict, Set, Any, Optional
import numpy as np
import random
from mathalgo2.Logger import Logger, logging
import os
from pathlib import Path
from Crypto.Cipher import AES, DES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
from tqdm import tqdm
import logging

"""
# 密碼加密解密模組

提供各種密碼加密和解密的功能。

## 主要功能

### 基礎編碼
- 摩斯密碼編解碼
- ASCII編碼解碼
- Base64編碼解碼 (待實現)

### 古典密碼
- 凱薩密碼加解密
- 柵欄密碼加解密
- 維吉尼亞密碼加解密 (待實現)

### 現代密碼
- RSA加解密 (待實現)
- AES加解密 (待實現)
- DES加解密 (待實現)

"""

# 設置根目錄和日誌
ROOT_DIR = Path(__file__).parent.parent
log_file = ROOT_DIR / "__log__" / "Code.log"

# 初始化日誌管理器
logger_manager = Logger(
    name="Code",
    log_file=str(log_file),
    level=logging.INFO
)

# 密碼表配置
class CodeMaps:
    """密碼表配置類"""
    
    # 摩斯密碼對照表
    MORSE_CODE = {
        "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".",
        "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
        "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---",
        "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
        "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--",
        "Z": "--."
    }
    
    # 凱薩密碼設置
    CAESAR_MIN = random.randint(1, 45)
    CAESAR_MAX = random.randint(1, 32)
    CAESAR_RECORD: List[int] = []

    # 維吉尼亞密碼表
    VIGENERE_TABLE = {
        chr(i): {chr(j): chr((i + j - 130) % 26 + 65) for j in range(65, 91)}
        for i in range(65, 91)
    }

class CodeBase:
    """基礎編碼類"""
    
    @staticmethod
    def morse_encode(text: str) -> str:
        """
        # 將文字轉換為摩斯密碼
        
        ## 參數
        - text: 要轉換的文字
        
        ## 回傳
        - 摩斯密碼字串
        
        ## 異常
        - ValueError: 當轉換過程發生錯誤時
        
        ## 範例
        ```python
        result = CodeBase.morse_encode("HELLO")
        print(result)  # .... . .-.. .-.. ---
        ```
        """
        try:
            result = ' '.join(CodeMaps.MORSE_CODE.get(char, char) for char in text.upper())
            logger_manager.info(f"摩斯密碼轉換成功: {text} -> {result}")
            return result
        except Exception as e:
            logger_manager.error(f"摩斯密碼轉換失敗: {str(e)}")
            raise ValueError("摩斯密碼轉換錯誤")

    @staticmethod
    def ascii_encode(text: str) -> str:
        """
        # 將文字轉換為ASCII碼
        
        ## 參數
        - text: 要轉換的文字
        
        ## 回傳
        - ASCII碼字串（以空格分隔）
        
        ## 異常
        - ValueError: 當轉換過程發生錯誤時
        
        ## 範例
        ```python
        result = CodeBase.ascii_encode("Hello")
        print(result)  # 72 101 108 108 111
        ```
        """
        try:
            result = ' '.join(str(ord(char)) for char in text)
            logger_manager.info(f"ASCII編碼轉換成功: {text} -> {result}")
            return result
        except Exception as e:
            logger_manager.error(f"ASCII編碼轉換失敗: {str(e)}")
            raise ValueError("ASCII編碼轉換錯誤")

    @staticmethod
    def ascii_decode(ascii_str: str) -> str:
        """
        # 將ASCII碼轉換回文字
        
        ## 參數
        - ascii_str: ASCII碼字串（以空格分隔）
        
        ## 回傳
        - 解碼後的文字
        
        ## 異常
        - ValueError: 當解碼過程發生錯誤時
        
        ## 範例
        ```python
        result = CodeBase.ascii_decode("72 101 108 108 111")
        print(result)  # Hello
        ```
        """
        try:
            result = ''.join(chr(int(code)) for code in ascii_str.split() if code.strip())
            logger_manager.info(f"ASCII解碼成功: {ascii_str} -> {result}")
            return result
        except Exception as e:
            logger_manager.error(f"ASCII解碼失敗: {str(e)}")
            raise ValueError("ASCII解碼錯誤")

    @staticmethod
    def base64_encode(text: str) -> str:
        """
        # 將文字轉換為Base64編碼
        
        ## 參數
        - text: 要編碼的文字
        
        ## 回傳
        - Base64編碼字串
        """
        try:
            import base64
            result = base64.b64encode(text.encode()).decode()
            logger_manager.info(f"Base64編碼成功: {text} -> {result}")
            return result
        except Exception as e:
            logger_manager.error(f"Base64編碼失敗: {str(e)}")
            raise ValueError("Base64編碼錯誤")

    @staticmethod
    def base64_decode(encoded_text: str) -> str:
        """
        # 將Base64編碼轉換回文字
        
        ## 參數
        - encoded_text: Base64編碼字串
        
        ## 回傳
        - 解碼後的文字
        """
        try:
            import base64
            result = base64.b64decode(encoded_text).decode()
            logger_manager.info(f"Base64解碼成功: {encoded_text} -> {result}")
            return result
        except Exception as e:
            logger_manager.error(f"Base64解碼失敗: {str(e)}")
            raise ValueError("Base64解碼錯誤")

class ClassicalCipher:
    """古典密碼類"""
    
    @staticmethod
    def caesar_encode(text: str) -> str:
        """
        # 凱薩密碼加密
        
        ## 參數
        - text: 要加密的文字
        
        ## 回傳
        - 加密後的文字
        
        ## 異常
        - ValueError: 當加密過程發生錯誤時
        
        ## 說明
        使用動態偏移量進行加密：
        - ASCII碼 <= 80 時使用 CAESAR_MIN 進行正向偏移
        - ASCII碼 > 80 時使用 CAESAR_MAX 進行負向偏移
        
        ## 範例
        ```python
        encrypted = ClassicalCipher.caesar_encode("Hello")
        print(encrypted)  # 加密後的文字
        ```
        """
        try:
            ascii_codes = [int(x) for x in CodeBase.ascii_encode(text).split()]
            CodeMaps.CAESAR_RECORD.clear()
            
            result = ''
            for code in ascii_codes:
                if code <= 80:
                    new_code = code + CodeMaps.CAESAR_MIN
                    CodeMaps.CAESAR_RECORD.append(0)
                else:
                    new_code = code - CodeMaps.CAESAR_MAX
                    CodeMaps.CAESAR_RECORD.append(1)
                result += chr(new_code)
                
            logger_manager.info(f"凱薩密碼加密成功: {text} -> {result}")
            return result
        except Exception as e:
            logger_manager.error(f"凱薩密碼加密失敗: {str(e)}")
            raise ValueError("凱薩密碼加密錯誤")

    @staticmethod
    def caesar_decode(encrypted_text: str) -> str:
        """
        # 凱薩密碼解密
        
        ## 參數
        - encrypted_text: 加密後的文字
        
        ## 回傳
        - 解密後的文字
        """
        try:
            result = ''
            for i, char in enumerate(encrypted_text):
                code = ord(char)
                if CodeMaps.CAESAR_RECORD[i] == 0:
                    new_code = code - CodeMaps.CAESAR_MIN
                else:
                    new_code = code + CodeMaps.CAESAR_MAX
                result += chr(new_code)
                
            logger_manager.info(f"凱薩密碼解密成功: {encrypted_text} -> {result}")
            return result
        except Exception as e:
            logger_manager.error(f"凱薩密碼解密失敗: {str(e)}")
            raise ValueError("凱薩密碼解密錯誤")

    @staticmethod
    def rail_fence_encode(text: str, rails: int = 3) -> str:
        """
        # 柵欄密碼加密
        
        ## 參數
        - text: 要加密的文字
        - rails: 柵欄行數（預設為3）
        
        ## 回傳
        - 加密後的文字
        """
        try:
            if rails < 2:
                raise ValueError("柵欄行數必須大於1")
                
            fence = [[] for _ in range(rails)]
            rail = 0
            direction = 1
            
            for char in text:
                fence[rail].append(char)
                rail += direction
                if rail == rails - 1 or rail == 0:
                    direction = -direction
                    
            result = ''.join([''.join(rail) for rail in fence])
            logger_manager.info(f"柵欄密碼加密成功: {text} -> {result}")
            return result
        except Exception as e:
            logger_manager.error(f"柵欄密碼加密失敗: {str(e)}")
            raise ValueError("柵欄密碼加密錯誤")

    @staticmethod
    def rail_fence_decode(encrypted_text: str, rails: int = 3) -> str:
        """
        # 柵欄密碼解密
        
        ## 參數
        - encrypted_text: 加密後的文字
        - rails: 柵欄行數（預設為3）
        
        ## 回傳
        - 解密後的文字
        """
        try:
            if rails < 2:
                raise ValueError("柵欄行數必須大於1")
                
            fence = [[] for _ in range(rails)]
            length = len(encrypted_text)
            
            # 計算每行應該有的字符數
            counts = [0] * rails
            rail = 0
            direction = 1
            for i in range(length):
                counts[rail] += 1
                rail += direction
                if rail == rails - 1 or rail == 0:
                    direction = -direction
            
            # 將加密文字分配到柵欄中
            index = 0
            for i in range(rails):
                fence[i] = list(encrypted_text[index:index + counts[i]])
                index += counts[i]
            
            # 重建原始文字
            result = ''
            rail = 0
            direction = 1
            for _ in range(length):
                result += fence[rail].pop(0)
                rail += direction
                if rail == rails - 1 or rail == 0:
                    direction = -direction
                    
            logger_manager.info(f"柵欄密碼解密成功: {encrypted_text} -> {result}")
            return result
        except Exception as e:
            logger_manager.error(f"柵欄密碼解密失敗: {str(e)}")
            raise ValueError("柵欄密碼解密錯誤")

    @staticmethod
    def vigenere_encode(text: str, key: str) -> str:
        """
        # 維吉尼亞密碼加密
        
        ## 參數
        - text: 要加密的文字
        - key: 加密金鑰
        
        ## 回傳
        - 加密後的文字
        
        ## 異常
        - ValueError: 當加密過程發生錯誤時
        
        ## 範例
        ```python
        encrypted = ClassicalCipher.vigenere_encode("HELLO", "KEY")
        print(encrypted)  # 加密後的文字
        ```
        """
        try:
            # 將文字和金鑰轉換為大寫
            text = text.upper()
            key = key.upper()
            
            # 生成完整長度的金鑰
            full_key = (key * (len(text) // len(key) + 1))[:len(text)]
            
            # 加密
            result = ''
            for t, k in zip(text, full_key):
                if not t.isalpha():
                    result += t
                    continue
                result += CodeMaps.VIGENERE_TABLE[k][t]
            
            logger_manager.info(f"維吉尼亞密碼加密成功: {text} -> {result}")
            return result
        except Exception as e:
            logger_manager.error(f"維吉尼亞密碼加密失敗: {str(e)}")
            raise ValueError("維吉尼亞密碼加密錯誤")

    @staticmethod
    def vigenere_decode(encrypted_text: str, key: str) -> str:
        """
        # 維吉尼亞密碼解密
        
        ## 參數
        - encrypted_text: 加密後的文字
        - key: 解密金鑰
        
        ## 回傳
        - 解密後的文字
        
        ## 異常
        - ValueError: 當解密過程發生錯誤時
        
        ## 範例
        ```python
        decrypted = ClassicalCipher.vigenere_decode("RIJVS", "KEY")
        print(decrypted)  # HELLO
        ```
        """
        try:
            # 將文字和金鑰轉換為大寫
            encrypted_text = encrypted_text.upper()
            key = key.upper()
            
            # 生成完整長度的金鑰
            full_key = (key * (len(encrypted_text) // len(key) + 1))[:len(encrypted_text)]
            
            # 解密
            result = ''
            for e, k in zip(encrypted_text, full_key):
                if not e.isalpha():
                    result += e
                    continue
                # 在維吉尼亞表中找到對應的原文字符
                for original in range(65, 91):
                    if CodeMaps.VIGENERE_TABLE[k][chr(original)] == e:
                        result += chr(original)
                        break
            
            logger_manager.info(f"維吉尼亞密碼解密成功: {encrypted_text} -> {result}")
            return result
        except Exception as e:
            logger_manager.error(f"維吉尼亞密碼解密失敗: {str(e)}")
            raise ValueError("維吉尼亞密碼解密錯誤")

class ModernCipher:
    """
    現代密碼類
    
    提供 RSA、AES、DES 等現代加密算法的實現
    包含檔案加密、進度顯示等功能
    
    主要功能：
    1. RSA 非對稱加密
    2. AES 對稱加密
    3. DES 對稱加密
    4. 檔案加密與保存
    5. 加密進度顯示
    """

    @staticmethod
    def generate_rsa_keys(bits: int = 2048) -> tuple:
        """
        # 生成 RSA 密鑰對
        
        ## 參數
        - bits: 密鑰位數，預設 2048
        
        ## 回傳
        - (public_key, private_key): RSA 公鑰和私鑰的元組
        """
        try:
            key = RSA.generate(bits)
            public_key = key.publickey().export_key()
            private_key = key.export_key()
            logger_manager.info(f"RSA密鑰對生成成功: {bits}位")
            return public_key, private_key
        except Exception as e:
            logger_manager.error(f"RSA密鑰對生成失敗: {str(e)}")
            raise ValueError("RSA密鑰對生成錯誤")

    @staticmethod
    def rsa_encrypt(message: str, public_key: bytes, show_progress: bool = True) -> str:
        """
        RSA 加密方法
        
        工作流程：
        1. 導入公鑰
        2. 初始化 PKCS1_OAEP 加密器
        3. 將消息分塊處理（避免超出 RSA 限制）
        4. 使用進度條顯示加密進度
        5. 合併加密結果並轉為 Base64
        
        Args:
            message: 要加密的訊息
            public_key: RSA 公鑰
            show_progress: 是否顯示進度條
        
        Returns:
            str: Base64 編碼的加密結果
        
        Raises:
            ValueError: 加密過程出錯時拋出
        """
        try:
            logger_manager.debug(f"開始 RSA 加密，消息長度：{len(message)}")
            
            # 導入公鑰
            key = RSA.import_key(public_key)
            cipher = PKCS1_OAEP.new(key)
            logger_manager.debug("RSA 公鑰導入成功")
            
            # 計算分塊大小（RSA 加密長度限制）
            chunk_size = 200
            message_bytes = message.encode()
            chunks = [message_bytes[i:i+chunk_size] 
                     for i in range(0, len(message_bytes), chunk_size)]
            
            logger_manager.debug(f"消息已分割為 {len(chunks)} 個區塊")
            
            # 加密每個分塊
            encrypted_chunks = []
            for chunk in tqdm(chunks, desc="RSA 加密進度", disable=not show_progress):
                encrypted_chunk = cipher.encrypt(chunk)
                encrypted_chunks.append(encrypted_chunk)
                logger_manager.debug(f"完成區塊加密，大小：{len(encrypted_chunk)} bytes")
            
            # 合併結果並轉為 Base64
            encrypted = b''.join(encrypted_chunks)
            result = base64.b64encode(encrypted).decode()
            
            logger_manager.info(f"RSA 加密完成，原始長度：{len(message)}，"
                              f"加密後長度：{len(result)}")
            return result
            
        except Exception as e:
            logger_manager.error(f"RSA 加密失敗：{str(e)}", exc_info=True)
            raise ValueError(f"RSA 加密錯誤：{str(e)}")

    @staticmethod
    def rsa_decrypt(encrypted_message: str, private_key: bytes) -> str:
        """
        # RSA 解密
        
        ## 參數
        - encrypted_message: Base64 編碼的加密訊息
        - private_key: RSA 私鑰
        
        ## 回傳
        - 解密後的訊息
        """
        try:
            key = RSA.import_key(private_key)
            cipher = PKCS1_OAEP.new(key)
            encrypted = base64.b64decode(encrypted_message)
            result = cipher.decrypt(encrypted).decode()
            logger_manager.info(f"RSA解密成功: {encrypted_message[:20]}... -> {result[:20]}...")
            return result
        except Exception as e:
            logger_manager.error(f"RSA解密失敗: {str(e)}")
            raise ValueError("RSA解密錯誤")

    @staticmethod
    def aes_encrypt(message: str, key: bytes = None, show_progress: bool = True) -> tuple:
        """
        # AES 加密
        
        ## 參數
        - message: 要加密的訊息
        - key: 16, 24 或 32 位元組的密鑰，若未提供則自動生成
        - show_progress: 是否顯示進度條
        
        ## 回傳
        - (encrypted_message, key): 加密後的Base64字串和密鑰的元組
        """
        try:
            if key is None:
                key = get_random_bytes(32)  # AES-256
            
            cipher = AES.new(key, AES.MODE_CBC)
            
            # 分塊處理大型數據
            chunk_size = 1024 * 1024  # 1MB
            message_bytes = message.encode()
            chunks = [message_bytes[i:i+chunk_size] for i in range(0, len(message_bytes), chunk_size)]
            
            encrypted_chunks = []
            # 使用 tqdm 顯示進度
            for chunk in tqdm(chunks, desc="AES 加密中", disable=not show_progress):
                padded_chunk = pad(chunk, AES.block_size)
                encrypted_chunk = cipher.encrypt(padded_chunk)
                encrypted_chunks.append(encrypted_chunk)
            
            # 合併加密結果
            encrypted = cipher.iv + b''.join(encrypted_chunks)
            result = base64.b64encode(encrypted).decode()
            
            logger_manager.info(f"AES加密成功: {message[:20]}... -> {result[:20]}...")
            return result, key
        except Exception as e:
            logger_manager.error(f"AES加密失敗: {str(e)}")
            raise ValueError("AES加密錯誤")

    @staticmethod
    def aes_decrypt(encrypted_message: str, key: bytes) -> str:
        """
        # AES 解密
        
        ## 參數
        - encrypted_message: Base64 編碼的加密訊息
        - key: AES 密鑰
        
        ## 回傳
        - 解密後的訊息
        """
        try:
            encrypted = base64.b64decode(encrypted_message)
            iv = encrypted[:16]
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = unpad(cipher.decrypt(encrypted[16:]), AES.block_size)
            result = decrypted.decode()
            logger_manager.info(f"AES解密成功: {encrypted_message[:20]}... -> {result[:20]}...")
            return result
        except Exception as e:
            logger_manager.error(f"AES解密失敗: {str(e)}")
            raise ValueError("AES解密錯誤")

    @staticmethod
    def des_encrypt(message: str, key: bytes = None, show_progress: bool = True) -> tuple:
        """
        # DES 加密
        
        ## 參數
        - message: 要加密的訊息
        - key: 8 位元組的密鑰，若未提供則自動生成
        - show_progress: 是否顯示進度條
        
        ## 回傳
        - (encrypted_message, key): 加密後的Base64字串和密鑰的元組
        """
        try:
            if key is None:
                key = get_random_bytes(8)
            
            cipher = DES.new(key, DES.MODE_CBC)
            
            # 分塊處理大型數據
            chunk_size = 1024 * 1024  # 1MB
            message_bytes = message.encode()
            chunks = [message_bytes[i:i+chunk_size] for i in range(0, len(message_bytes), chunk_size)]
            
            encrypted_chunks = []
            # 使用 tqdm 顯示進度
            for chunk in tqdm(chunks, desc="DES 加密中", disable=not show_progress):
                padded_chunk = pad(chunk, DES.block_size)
                encrypted_chunk = cipher.encrypt(padded_chunk)
                encrypted_chunks.append(encrypted_chunk)
            
            # 合併加密結果
            encrypted = cipher.iv + b''.join(encrypted_chunks)
            result = base64.b64encode(encrypted).decode()
            
            logger_manager.info(f"DES加密成功: {message[:20]}... -> {result[:20]}...")
            return result, key
        except Exception as e:
            logger_manager.error(f"DES加密失敗: {str(e)}")
            raise ValueError("DES加密錯誤")

    @staticmethod
    def des_decrypt(encrypted_message: str, key: bytes) -> str:
        """
        # DES 解密
        
        ## 參數
        - encrypted_message: Base64 編碼的加密訊息
        - key: DES 密鑰
        
        ## 回傳
        - 解密後的訊息
        """
        try:
            encrypted = base64.b64decode(encrypted_message)
            iv = encrypted[:8]
            cipher = DES.new(key, DES.MODE_CBC, iv)
            decrypted = unpad(cipher.decrypt(encrypted[8:]), DES.block_size)
            result = decrypted.decode()
            logger_manager.info(f"DES解密成功: {encrypted_message[:20]}... -> {result[:20]}...")
            return result
        except Exception as e:
            logger_manager.error(f"DES解密失敗: {str(e)}")
            raise ValueError("DES解密錯誤")

    @staticmethod
    def save_encrypted_file(encrypted_data: str, output_path: str, 
                          key: bytes = None, overwrite: bool = False) -> None:
        """
        保存加密數據到檔案
        
        工作流程：
        1. 檢查輸出路徑
        2. 創建必要的目錄
        3. 保存加密數據
        4. 可選保存密鑰
        
        Args:
            encrypted_data: 加密後的數據
            output_path: 輸出檔案路徑
            key: 加密密鑰（可選）
            overwrite: 是否覆蓋現有檔案
        
        Raises:
            ValueError: 檔案操作出錯時拋出
            FileExistsError: 檔案已存在且不允許覆蓋時拋出
        """
        try:
            # 檢查輸出路徑
            output_path = Path(output_path)
            if output_path.exists() and not overwrite:
                logger_manager.warning(f"檔案已存在且不允許覆蓋：{output_path}")
                raise FileExistsError(f"檔案已存在：{output_path}")
            
            # 創建目錄
            output_path.parent.mkdir(parents=True, exist_ok=True)
            logger_manager.debug(f"確保目錄存在：{output_path.parent}")
            
            # 保存加密數據
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(encrypted_data)
            logger_manager.debug(f"加密數據已保存，大小：{len(encrypted_data)} bytes")
            
            # 保存密鑰（如果有）
            if key:
                key_path = output_path.with_suffix('.key')
                with open(key_path, 'wb') as f:
                    f.write(key)
                logger_manager.debug(f"密鑰已保存：{key_path}")
            
            logger_manager.info(f"加密檔案保存成功：{output_path}")
            
        except Exception as e:
            logger_manager.error(f"保存加密檔案失敗：{str(e)}", exc_info=True)
            raise ValueError(f"檔案保存錯誤：{str(e)}")

    @staticmethod
    def load_encrypted_file(file_path: str, key_path: str = None) -> tuple:
        """
        # 從檔案讀取加密數據
        
        ## 參數
        - file_path: 加密檔案路徑
        - key_path: 密鑰檔案路徑（可選）
        
        ## 回傳
        - (encrypted_data, key): 加密數據和密鑰的元組
        """
        try:
            # 讀取加密數據
            with open(file_path, 'r', encoding='utf-8') as f:
                encrypted_data = f.read()
            
            # 如果提供了密鑰路徑，讀取密鑰
            key = None
            if key_path and os.path.exists(key_path):
                with open(key_path, 'rb') as f:
                    key = f.read()
            
            logger_manager.info(f"加密檔案讀取成功: {file_path}")
            return encrypted_data, key
        except Exception as e:
            logger_manager.error(f"加密檔案讀取失敗: {str(e)}")
            raise ValueError("檔案讀取錯誤")

    # 修改現有的加密方法，添加檔案輸出功能
    @staticmethod
    def rsa_encrypt_file(input_file: str, public_key: bytes, output_file: str = None) -> str:
        """
        # RSA 檔案加密
        
        ## 參數
        - input_file: 輸入檔案路徑
        - public_key: RSA 公鑰
        - output_file: 輸出檔案路徑（可選）
        
        ## 回傳
        - 加密後的 Base64 字串
        """
        try:
            # 讀取檔案內容
            with open(input_file, 'r', encoding='utf-8') as f:
                message = f.read()
            
            # 加密
            encrypted = ModernCipher.rsa_encrypt(message, public_key)
            
            # 如果指定了輸出檔案，保存結果
            if output_file:
                ModernCipher.save_encrypted_file(encrypted, output_file)
            
            return encrypted
        except Exception as e:
            logger_manager.error(f"RSA檔案加密失敗: {str(e)}")
            raise ValueError("RSA檔案加密錯誤")

    @staticmethod
    def aes_encrypt_file(input_file: str, key: bytes = None, 
                        output_file: str = None, show_progress: bool = True) -> tuple:
        """
        AES 檔案加密
        
        ## 參數
        - input_file: 輸入檔案路徑
        - key: AES 密鑰（可選）
        - output_file: 輸出檔案路徑（可選）
        - show_progress: 是否顯示進度條
        
        ## 回傳
        - (encrypted_data, key): 加密數據和密鑰的元組
        
        ## 異常
        - ValueError: 加密過程出錯時拋出
        """
        try:
            logger_manager.debug(f"開始處理檔案：{input_file}")
            
            # 檢查輸入檔案
            if not os.path.exists(input_file):
                raise FileNotFoundError(f"找不到輸入檔案：{input_file}")
            
            # 讀取檔案
            with open(input_file, 'r', encoding='utf-8') as f:
                message = f.read()
            logger_manager.debug(f"檔案讀取完成，大小：{len(message)} bytes")
            
            # 加密
            encrypted, key = ModernCipher.aes_encrypt(
                message, key, show_progress=show_progress
            )
            logger_manager.debug("AES 加密完成")
            
            # 保存結果（如果需要）
            if output_file:
                ModernCipher.save_encrypted_file(encrypted, output_file, key)
                logger_manager.debug(f"加密結果已保存：{output_file}")
            
            logger_manager.info(f"檔案加密完成：{input_file} -> {output_file or '未保存'}")
            return encrypted, key
            
        except Exception as e:
            logger_manager.error(f"AES 檔案加密失敗：{str(e)}", exc_info=True)
            raise ValueError(f"AES 檔案加密錯誤：{str(e)}")

    @staticmethod
    def des_encrypt_file(input_file: str, key: bytes = None, output_file: str = None) -> tuple:
        """
        # DES 檔案加密
        
        ## 參數
        - input_file: 輸入檔案路徑
        - key: DES 密鑰（可選）
        - output_file: 輸出檔案路徑（可選）
        
        ## 回傳
        - (encrypted_data, key): 加密數據和密鑰的元組
        """
        try:
            # 讀取檔案內容
            with open(input_file, 'r', encoding='utf-8') as f:
                message = f.read()
            
            # 加密
            encrypted, key = ModernCipher.des_encrypt(message, key)
            
            # 如果指定了輸出檔案，保存結果
            if output_file:
                ModernCipher.save_encrypted_file(encrypted, output_file, key)
            
            return encrypted, key
        except Exception as e:
            logger_manager.error(f"DES檔案加密失敗: {str(e)}")
            raise ValueError("DES檔案加密錯誤")

__all__ = [
    "CodeBase",
    "ClassicalCipher",
    "ModernCipher"
]
