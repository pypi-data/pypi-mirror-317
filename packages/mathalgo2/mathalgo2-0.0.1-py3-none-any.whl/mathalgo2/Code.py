from typing import List, Union, Dict, Set, Any, Optional
import numpy as np
import random
from mathalgo2.logger import setup_logger, logging
import os
from pathlib import Path

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

## 使用說明
每個功能都有詳細的文檔說明和使用範例。
詳細使用方式請參考各個方法的文檔。

## 版本記錄
- v1.0.0: 基礎功能實現
- v1.1.0: 增加詳細註釋和日誌
- v1.2.0: 優化代碼結構，為擴展做準備
"""

# 設置根目錄和日誌
ROOT_DIR = Path(__file__).parent.parent
log_file = os.path.join(ROOT_DIR, "__log__", "code.log")
logger = setup_logger("code", log_file, level=logging.INFO)

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
            logger.info(f"摩斯密碼轉換成功: {text} -> {result}")
            return result
        except Exception as e:
            logger.error(f"摩斯密碼轉換失敗: {str(e)}")
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
            logger.info(f"ASCII編碼轉換成功: {text} -> {result}")
            return result
        except Exception as e:
            logger.error(f"ASCII編碼轉換失敗: {str(e)}")
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
            logger.info(f"ASCII解碼成功: {ascii_str} -> {result}")
            return result
        except Exception as e:
            logger.error(f"ASCII解碼失敗: {str(e)}")
            raise ValueError("ASCII解碼錯誤")

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
                
            logger.info(f"凱薩密碼加密成功: {text} -> {result}")
            return result
        except Exception as e:
            logger.error(f"凱薩密碼加密失敗: {str(e)}")
            raise ValueError("凱薩密碼加密錯誤")

__all__ = [
    "CodeBase",
    "ClassicalCipher"
]
