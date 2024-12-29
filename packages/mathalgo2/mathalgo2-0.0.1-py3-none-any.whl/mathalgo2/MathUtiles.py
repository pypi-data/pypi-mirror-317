from typing import Union, List
from mathalgo2.Structure import Stack
from mathalgo2.logger import setup_logger, logging
import numpy as np
import os
from pathlib import Path

# 獲取當前文件所在目錄的根目錄
ROOT_DIR = Path(__file__).parent.parent

# 設置日誌文件路徑
log_file = os.path.join(ROOT_DIR, "__log__", "math_utiles.log")
logger = setup_logger("math_utiles", log_file, level=logging.INFO)

class MathUtils:
    @staticmethod
    def convert_input_to_int_list(input_string: str) -> List[int]:
        """返回運算符的優先級。
        
        Args:
            op: 運算符
            
        Returns:
            int: 優先級（0-3）
        """
        precedences = {
            '+': 1, '-': 1,
            '*': 2, '/': 2,
            '^': 3
        }
        return precedences.get(op, 0)

    @staticmethod
    def infix_to_postfix(expression: str) -> List[str]:
        """將中綴表達式轉換成後綴表達式。
        
        Args:
            expression: 中綴表達式字符串
            
        Returns:
            List[str]: 後綴表達式列表
            
        Raises:
            ValueError: 當表達式格式不正確時
        """
        logger.info(f"Converting infix expression: {expression}")
        out = Stack()
        stack = Stack()
        
        for ch in expression:
            if ch.isspace():
                continue
            if ch.isalnum():
                out.push(ch)
            elif ch == "(":
                stack.push(ch)
            elif ch == ")":
                try:
                    while stack.peek() != "(":
                        out.push(stack.pop())
                    stack.pop()  # 弹出 '('
                except:
                    raise ValueError("括號不匹配")
            else:
                while (not stack.is_empty() and 
                       stack.peek() != "(" and 
                       MathUtils.precedence(stack.peek()) >= MathUtils.precedence(ch)):
                    out.push(stack.pop())
                stack.push(ch)
                
        while not stack.is_empty():
            if stack.peek() == "(":
                raise ValueError("括號不匹配")
            out.push(stack.pop())

        logger.info(f"Converted to postfix: {out.items}")
        return out.items

    @staticmethod
    def is_almost_equal(a: float, b: float, tolerance: float = 1e-9) -> bool:
        """檢查兩個浮點數是否幾乎相等。
        
        Args:
            a: 第一個浮點數
            b: 第二個浮點數
            tolerance: 容許誤差
            
        Returns:
            bool: 是否幾乎相等
        """
        return abs(a - b) < tolerance

    @staticmethod
    def evaluate_postfix(expression: List[str]) -> float:
        """計算後綴表達式的值。
        
        Args:
            expression: 後綴表達式的元素列表
            
        Returns:
            float: 計算結果
            
        Raises:
            ValueError: 當表達式不合法時
        """
        logger.info(f"Evaluating postfix expression: {expression}")
        stack = Stack()
        operators = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b if b != 0 else float('inf'),
            '^': lambda a, b: a ** b
        }

        try:
            for token in expression:
                if token.replace('.', '', 1).lstrip('-').isdigit():
                    stack.push(float(token))
                elif token in operators:
                    if stack.__size__() < 2:
                        raise ValueError("表達式不合法，操作數不足")
                    b = stack.pop()
                    a = stack.pop()
                    result = operators[token](a, b)
                    stack.push(result)
                else:
                    raise ValueError(f"不支援的符號: {token}")

            if stack.__size__() != 1:
                raise ValueError("表達式不合法，結果堆疊有多於一個值")

            result = stack.pop()
            logger.info(f"Evaluation result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error evaluating postfix expression: {str(e)}")
            raise ValueError(f"計算錯誤: {str(e)}")
    
    @staticmethod
    def prime_factorization(n: int) -> List[int]:
        """將一個正整數分解為質因數。
        
        Args:
            n: 要分解的正整數
            
        Returns:
            List[int]: 質因數列表
            
        Raises:
            ValueError: 當輸入不是正整數時
        """
        logger.info(f"Calculating prime factors for: {n}")
        
        try:
            if not isinstance(n, int) or n <= 0:
                logger.error(f"Invalid input: {n}")
                raise ValueError("輸入必須是正整數")
                
            factors = []
            divisor = 2
            
            while n > 1:
                while n % divisor == 0:
                    factors.append(divisor)
                    n //= divisor
                divisor += 1 if divisor == 2 else 2
                
                # 最佳化: 如果除數的平方大於n，則n本身就是質數
                if divisor * divisor > n and n > 1:
                    factors.append(n)
                    break
                
            logger.info(f"Prime factors: {factors}")
            return factors
        except Exception as e:
            logger.error(f"Error in prime factorization: {str(e)}")
            raise
    
    @staticmethod
    def factorization(n: int) -> List[List[int]]:
        """將一個正整數分解為因數對。
        
        Args:
            n: 要分解的正整數
            
        Returns:
            List[List[int]]: 因數對列表，每個元素為 [因數1, 因數2]
            
        Raises:
            ValueError: 當輸入不是正整數時
        """
        logger.info(f"開始對 {n} 進行因數分解")
        
        try:
            if not isinstance(n, int) or n <= 0:
                logger.error(f"無效的輸入類型或數值: {n}")
                raise ValueError("輸入必須是正整數")
                
            factors = []
            sqrt_n = int(n**0.5)
            logger.debug(f"計算 {n} 的平方根: {sqrt_n}")
            
            for i in range(1, sqrt_n + 1):
                if n % i == 0:
                    pair = [i, n // i]
                    factors.append(pair)
                    logger.debug(f"找到因數對: {pair}")
                    
                    if i != n // i:
                        reverse_pair = [n // i, i]
                        factors.append(reverse_pair)
                        logger.debug(f"添加反向因數對: {reverse_pair}")
            
            factors.sort()
            logger.info(f"最終排序後的因數對: {factors}")
            return factors
            
        except Exception as e:
            logger.error(f"因數分解過程發生錯誤: {str(e)}")
            raise
    
    @staticmethod
    def convert_to_matrix(data: str) -> np.ndarray:
        """將輸入的數列轉換為矩陣。
        
        Returns:
            numpy.ndarray: 轉換後的矩陣
        """
        logger.info(f"開始將數據轉換為矩陣。輸入數據: {data}")
        try:
            if isinstance(data, str):
                logger.debug("輸入為字符串，開始分割數字")
                data = data.split()
                logger.debug(f"分割結果: {data}")
                
                data = [int(i) for i in data]
                logger.debug(f"轉換為整數列表: {data}")
                
                data = np.array(data)
                logger.debug(f"轉換為numpy數組: {data}")
                
                size = data.size
                logger.info(f"數組大小: {size}")
                
                ft = MathUtils.factorization(size)
                logger.debug(f"因數分解結果: {ft}")
                
                middle_index = int(len(ft)/2)
                Msize = ft[middle_index]
                logger.info(f"選擇的矩陣維度: {Msize}")
                
                data = data.reshape(Msize[0], Msize[1])
                logger.info(f"重塑後的矩陣:\n{data}")
                
            return data
        except Exception as e:
            logger.error(f"矩陣轉換過程發生錯誤: {str(e)}")
            raise

    @staticmethod
    def convert_input_to_int_list(input_string: str) -> List[int]:
        """將使用者輸入的數列字串轉換為整數列表。
        
        # 參數
        - input_string: 包含數字的字串，數字間可用空格或逗號分隔
            
        # 返回值
        - List[int]: 轉換後的整數列表
            
        # 異常
        - ValueError: 當輸入包含非數字字符時
        
        # 範例
        ```python
        input_str = "1 2,3 4, 5"
        result = MathUtils.convert_input_to_int_list(input_str)
        print(result)  # [1, 2, 3, 4, 5]
        ```
        """
        logger.info(f"Converting input string to integer list: {input_string}")
        try:
            # 移除多餘空白並根據空格或逗號分割
            numbers = input_string.strip().replace(',', ' ').split()
            
            # 轉換為整數列表
            int_list = [int(num) for num in numbers]
            
            logger.info(f"Converted to integer list: {int_list}")
            return int_list
            
        except ValueError as e:
            logger.error(f"Error converting string to integers: {str(e)}")
            raise ValueError("輸入必須是數字，可用空格或逗號分隔")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise

__all__ = [
    "MathUtils"
]
