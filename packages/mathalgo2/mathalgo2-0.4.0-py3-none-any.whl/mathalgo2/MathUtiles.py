from typing import Union, List
from mathalgo2.Structure import Stack
from mathalgo2.Logger import Logger, logging
import numpy as np
import os
from pathlib import Path

# 設置根目錄和日誌
ROOT_DIR = Path(__file__).parent.parent
log_file = ROOT_DIR / "__log__" / "math_utiles.log"

# 初始化日誌管理器
logger_manager = Logger(
    name="math_utiles",
    log_file=str(log_file),
    level=logging.INFO
)

class MathUtils:
    @staticmethod
    def precedence(operator):
        """
        返回運算符的優先級
        """
        if operator in ['+', '-']:
            return 1
        if operator in ['*', '/']:
            return 2
        if operator == '^':
            return 3
        return 0

    @staticmethod
    def infix_to_postfix(expression):
        """
        將中綴表達式轉換為後綴表達式
        """
        # 初始化一個空棧和結果列表
        stack = []
        output = []
        
        # 移除表達式中的空格
        expression = expression.replace(" ", "")
        
        # 遍歷表達式中的每個字符
        i = 0
        while i < len(expression):
            char = expression[i]
            
            # 如果是數字，收集完整的數字
            if char.isdigit():
                num = ""
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num += expression[i]
                    i += 1
                output.append(num)
                i -= 1
            
            # 如果是左括號，壓入棧中
            elif char == '(':
                stack.append(char)
            
            # 如果是右括號，彈出棧中的運算符直到遇到左括號
            elif char == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack and stack[-1] == '(':
                    stack.pop()
                else:
                    raise ValueError("括號不匹配")
            
            # 如果是運算符
            elif char in '+-*/^':
                while (stack and stack[-1] != '(' and 
                       MathUtils.precedence(stack[-1]) >= MathUtils.precedence(char)):
                    output.append(stack.pop())
                stack.append(char)
            
            i += 1
        
        # 將棧中剩餘的運算符加入到輸出中
        while stack:
            if stack[-1] == '(':
                raise ValueError("括號不匹配")
            output.append(stack.pop())
        
        return output

    @staticmethod
    def convert_input_to_int_list(input_string: str) -> List[int]:
        """將使用者輸入的數列字串轉換為整數列表"""
        precedences = {
            '+': 1, '-': 1,
            '*': 2, '/': 2,
            '^': 3
        }
        
        try:
            # 移除多餘空白並根據空格或逗號分割
            numbers = input_string.strip().replace(',', ' ').split()
            
            # 轉換為整數列表
            return [int(num) for num in numbers]
            
        except ValueError as e:
            raise ValueError("輸入必須是數字，可用空格或逗號分隔")

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
        logger_manager.info(f"Evaluating postfix expression: {expression}")
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
            logger_manager.info(f"Evaluation result: {result}")
            return result
        except Exception as e:
            logger_manager.error(f"Error evaluating postfix expression: {str(e)}")
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
        logger_manager.info(f"Calculating prime factors for: {n}")
        
        try:
            if not isinstance(n, int) or n <= 0:
                logger_manager.error(f"Invalid input: {n}")
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
                
            logger_manager.info(f"Prime factors: {factors}")
            return factors
        except Exception as e:
            logger_manager.error(f"Error in prime factorization: {str(e)}")
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
        logger_manager.info(f"開始對 {n} 進行因數分解")
        
        try:
            if not isinstance(n, int) or n <= 0:
                logger_manager.error(f"無效的輸入類型或數值: {n}")
                raise ValueError("輸入必須是正整數")
                
            factors = []
            sqrt_n = int(n**0.5)
            logger_manager.debug(f"計算 {n} 的平方根: {sqrt_n}")
            
            for i in range(1, sqrt_n + 1):
                if n % i == 0:
                    pair = [i, n // i]
                    factors.append(pair)
                    logger_manager.debug(f"找到因數對: {pair}")
                    
                    if i != n // i:
                        reverse_pair = [n // i, i]
                        factors.append(reverse_pair)
                        logger_manager.debug(f"添加反向因數對: {reverse_pair}")
            
            factors.sort()
            logger_manager.info(f"最終排序後的因數對: {factors}")
            return factors
            
        except Exception as e:
            logger_manager.error(f"因數分解過程發生錯誤: {str(e)}")
            raise
    
    @staticmethod
    def convert_to_matrix(data: str) -> np.ndarray:
        """將輸入的數列轉換為矩陣。
        
        Returns:
            numpy.ndarray: 轉換後的矩陣
        """
        logger_manager.info(f"開始將數據轉換為矩陣。輸入數據: {data}")
        try:
            if isinstance(data, str):
                logger_manager.debug("輸入為字符串，開始分割數字")
                data = data.split()
                logger_manager.debug(f"分割結果: {data}")
                
                data = [int(i) for i in data]
                logger_manager.debug(f"轉換為整數列表: {data}")
                
                data = np.array(data)
                logger_manager.debug(f"轉換為numpy數組: {data}")
                
                size = data.size
                logger_manager.info(f"數組大小: {size}")
                
                ft = MathUtils.factorization(size)
                logger_manager.debug(f"因數分解結果: {ft}")
                
                middle_index = int(len(ft)/2)
                Msize = ft[middle_index]
                logger_manager.info(f"選擇的矩陣維度: {Msize}")
                
                data = data.reshape(Msize[0], Msize[1])
                logger_manager.info(f"重塑後的矩陣:\n{data}")
                
            return data
        except Exception as e:
            logger_manager.error(f"矩陣轉換過程發生錯誤: {str(e)}")
            raise

    @staticmethod
    def combination(n: int, r: int) -> int:
        """計算組合數 C(n,r)。
        
        計算從n個不同元素中取出r個元素的組合數。
        使用公式：C(n,r) = n! / (r! * (n-r)!)
        為了避免大數計算，使用優化算法。
        
        Args:
            n: 總元素數量
            r: 要選取的元素數量
            
        Returns:
            int: 組合數結果
            
        Examples:
            >>> MathUtils.combination(5, 2)
            10  # 表示從5個元素中取出2個的組合方式有10種
        """
        logger_manager.info(f"計算組合數 C({n},{r})")
        
        try:
            if r > n:
                logger_manager.debug(f"r({r}) > n({n})，返回0")
                return 0
                
            # 優化：使用較小的r來減少計算量
            r = min(r, n-r)
            logger_manager.debug(f"優化後的r值: {r}")
            
            numerator = 1    # 分子
            denominator = 1  # 分母
            
            # 計算組合數
            for i in range(r):
                numerator *= (n - i)
                denominator *= (i + 1)
                logger_manager.debug(f"第{i+1}次迭代: 分子={numerator}, 分母={denominator}")
            
            result = numerator // denominator
            logger_manager.info(f"組合數計算結果: C({n},{r}) = {result}")
            return result
            
        except Exception as e:
            logger_manager.error(f"計算組合數時發生錯誤: {str(e)}")
            raise

    @staticmethod
    def permutation(n: int, r: int) -> int:
        """計算排列數 P(n,r)。
        
        計算從n個不同元素中取出r個元素的排列數。
        使用公式：P(n,r) = n!/(n-r)!
        
        Args:
            n: 總元素數量
            r: 要選取的元素數量
            
        Returns:
            int: 排列數結果
            
        Examples:
            >>> MathUtils.permutation(5, 2)
            20  # 表示從5個元素中取出2個的排列方式有20種
        """
        logger_manager.info(f"計算排列數 P({n},{r})")
        
        try:
            if r > n:
                logger_manager.debug(f"r({r}) > n({n})，返回0")
                return 0
                
            result = 1
            # 計算 n * (n-1) * ... * (n-r+1)
            for i in range(n, n-r, -1):
                result *= i
                logger_manager.debug(f"當前計算值: {result}")
            
            logger_manager.info(f"排列數計算結果: P({n},{r}) = {result}")
            return result
            
        except Exception as e:
            logger_manager.error(f"計算排列數時發生錯誤: {str(e)}")
            raise

    @staticmethod
    def factorial(n: int) -> int:
        """計算階乘 n!。
        
        計算正整數n的階乘，定義為所有小於等於n的正整數的乘積。
        特殊情況：0! = 1
        
        Args:
            n: 要計算階乘的非負整數
            
        Returns:
            int: 階乘結果
            
        Raises:
            ValueError: 當輸入為負數時
            
        Examples:
            >>> MathUtils.factorial(5)
            120  # 5! = 5 * 4 * 3 * 2 * 1 = 120
        """
        logger_manager.info(f"計算階乘: {n}!")
        
        try:
            if n < 0:
                logger_manager.error(f"嘗試計算負數的階乘: {n}")
                raise ValueError("階乘不能用於負數")
                
            if n == 0:
                logger_manager.debug("0的階乘為1")
                return 1
                
            result = 1
            for i in range(1, n + 1):
                result *= i
                logger_manager.debug(f"階乘計算中: {i}! = {result}")
            
            logger_manager.info(f"階乘計算結果: {n}! = {result}")
            return result
            
        except Exception as e:
            logger_manager.error(f"計算階乘時發生錯誤: {str(e)}")
            raise

    @staticmethod
    def gcd(a: int, b: int) -> int:
        """計算兩個數的最大公約數。
        
        Args:
            a: 第一個整數
            b: 第二個整數
            
        Returns:
            int: 最大公約數
        """
        while b:
            a, b = b, a % b
        return abs(a)

    @staticmethod
    def lcm(a: int, b: int) -> int:
        """計算兩個數的最小公倍數。
        
        Args:
            a: 第一個整數
            b: 第二個整數
            
        Returns:
            int: 最小公倍數
        """
        return abs(a * b) // MathUtils.gcd(a, b)

    @staticmethod
    def is_prime(n: int) -> bool:
        """判斷一個數是否為質數。
        
        Args:
            n: 要判斷的整數
            
        Returns:
            bool: 是否為質數
        """
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def fibonacci(n: int) -> List[int]:
        """生成斐波那契數列。
        
        Args:
            n: 要生成的項數
            
        Returns:
            List[int]: 斐波那契數列
        """
        if n <= 0:
            return []
        elif n == 1:
            return [0]
        
        fib = [0, 1]
        for i in range(2, n):
            fib.append(fib[i-1] + fib[i-2])
        return fib

    @staticmethod
    def is_perfect_number(n: int) -> bool:
        """判斷是否為完美數。
        
        完美數是指其所有真因數（除了自身以外的因數）的和等於本身的正整數。
        例如：6 = 1 + 2 + 3
        
        Args:
            n: 要判斷的正整數
            
        Returns:
            bool: 是否為完美數
            
        Examples:
            >>> MathUtils.is_perfect_number(6)
            True  # 6的真因數為1,2,3，和為6
        """
        logger_manager.info(f"檢查完美數: {n}")
        
        try:
            if n <= 1:
                logger_manager.debug(f"{n} 小於等於1，不是完美數")
                return False
                
            factors_sum = 1  # 從1開始，1是所有數的因數
            for i in range(2, int(n ** 0.5) + 1):
                if n % i == 0:
                    factors_sum += i
                    if i != n // i:  # 避免平方根重複計算
                        factors_sum += n // i
                    logger_manager.debug(f"找到因數: {i} 和 {n//i}, 當前和為 {factors_sum}")
            
            is_perfect = factors_sum == n
            logger_manager.info(f"{n} {'是' if is_perfect else '不是'}完美數")
            return is_perfect
            
        except Exception as e:
            logger_manager.error(f"檢查完美數時發生錯誤: {str(e)}")
            raise

    @staticmethod
    def euler_totient(n: int) -> int:
        """計算歐拉函數φ(n)。
        
        計算小於n且與n互質的正整數的數量。
        
        Args:
            n: 要計算的正整數
            
        Returns:
            int: 歐拉函數值
            
        Examples:
            >>> MathUtils.euler_totient(10)
            4  # 1,3,7,9 與 10互質
        """
        logger_manager.info(f"計算歐拉函數 φ({n})")
        
        try:
            if n <= 0:
                logger_manager.error(f"輸入必須為正整數: {n}")
                raise ValueError("輸入必須為正整數")
                
            result = n
            # 對n進行質因數分解
            for i in range(2, int(n ** 0.5) + 1):
                if n % i == 0:
                    while n % i == 0:
                        n //= i
                    result *= (1 - 1/i)
                    logger_manager.debug(f"找到質因數 {i}, 當前結果 = {result}")
            
            if n > 1:
                result *= (1 - 1/n)
                logger_manager.debug(f"最後的質因數 {n}, 最終結果 = {result}")
            
            result = int(result)
            logger_manager.info(f"歐拉函數計算結果: φ({n}) = {result}")
            return result
            
        except Exception as e:
            logger_manager.error(f"計算歐拉函數時發生錯誤: {str(e)}")
            raise

    @staticmethod
    def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
        """計算擴展歐幾里得算法。
        
        計算a和b的最大公約數d，並找到x和y使得ax + by = d
        
        Args:
            a: 第一個整數
            b: 第二個整數
            
        Returns:
            tuple: (d, x, y) 其中d是最大公約數，ax + by = d
            
        Examples:
            >>> MathUtils.extended_gcd(35, 15)
            (5, 1, -2)  # 5是最大公約數，且 35*1 + 15*(-2) = 5
        """
        logger_manager.info(f"計算擴展歐幾里得算法: a={a}, b={b}")
        
        try:
            if b == 0:
                logger_manager.debug("b=0，直接返回結果")
                return a, 1, 0
                
            # 遞迴計算
            d, x1, y1 = MathUtils.extended_gcd(b, a % b)
            x = y1
            y = x1 - (a // b) * y1
            
            logger_manager.debug(f"當前步驟: d={d}, x={x}, y={y}")
            logger_manager.info(f"擴展歐幾里得算法結果: d={d}, x={x}, y={y}")
            return d, x, y
            
        except Exception as e:
            logger_manager.error(f"計算擴展歐幾里得算法時發生錯誤: {str(e)}")
            raise

    @staticmethod
    def catalan_number(n: int) -> int:
        """計算卡塔蘭數。
        
        卡塔蘭數是組合數學中的數列，可用於計算多種計數問題。
        第n個卡塔蘭數的計算公式：C(n) = C(2n,n)/(n+1)
        
        Args:
            n: 要計算第幾個卡塔蘭數
            
        Returns:
            int: 第n個卡塔蘭數
            
        Examples:
            >>> MathUtils.catalan_number(4)
            14  # 第4個卡塔蘭數
        """
        logger_manager.info(f"計算第{n}個卡塔蘭數")
        
        try:
            if n < 0:
                logger_manager.error("卡塔蘭數不能為負數")
                raise ValueError("輸入必須為非負整數")
                
            if n == 0:
                logger_manager.debug("n=0，返回1")
                return 1
                
            # 使用組合數公式計算
            numerator = MathUtils.combination(2*n, n)
            result = numerator // (n + 1)
            
            logger_manager.debug(f"計算過程: C(2*{n},{n})/{n+1} = {numerator}/{n+1} = {result}")
            logger_manager.info(f"第{n}個卡塔蘭數為: {result}")
            return result
            
        except Exception as e:
            logger_manager.error(f"計算卡塔蘭數時發生錯誤: {str(e)}")
            raise

__all__ = [
    "MathUtils"
]
