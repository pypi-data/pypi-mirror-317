from typing import Union, List
from mathalgo2.structure import Stack

class MathUtils:
    @staticmethod
    def precedence(op: str) -> int:
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

            return stack.pop()
        except Exception as e:
            raise ValueError(f"計算錯誤: {str(e)}")