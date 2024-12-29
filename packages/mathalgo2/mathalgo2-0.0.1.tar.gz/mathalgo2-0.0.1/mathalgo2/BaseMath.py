from typing import Union, Optional, List, Tuple
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from mathalgo2.logger import setup_logger, logging
import os
from pathlib import Path
from mathalgo2.MathUtiles import MathUtils as mu

# 獲取當前文件所在目錄的根目錄
ROOT_DIR = Path(__file__).parent.parent

# 設置日誌文件路徑
log_file = os.path.join(ROOT_DIR, "__log__", "math.log")
logger = setup_logger("Math_mode", log_file, level=logging.INFO)

# 定義符號變量
x = sp.Symbol("x")

class Calculus:
    """
    # 微積分類別
    
    提供各種微積分相關運算的核心類別。
    
    ## 功能
    - 符號微分和數值微分
    - 不定積分和定積分
    - 極限計算
    - 函數繪圖
    - 泰勒級數展開
    """

    def __init__(self, func_expr: Union[str, sp.Expr]):
        """
        # 初始化函數表達式
        
        ## 參數
        - `func_expr`: 字串或 sympy 表達式形式的函數
        """
        try:
            self.func_expr = sp.sympify(func_expr) if isinstance(func_expr, str) else func_expr
            logger.info(f"函數表達式 f(x) = {self.func_expr} 初始化成功")
        except Exception as e:
            logger.error(f"函數表達式初始化失敗: {str(e)}")
            raise ValueError("無效的函數表達式")

    def __repr__(self) -> str:
        """函數表達式的字串表示"""
        return f"f(x) = {str(self.func_expr)}"

    def derivative(self, order: int = 1) -> 'Calculus':
        """
        # 計算函數導數
        
        ## 參數
        - `order`: 導數階數
        
        ## 回傳
        - 導數結果的 Calculus 物件
        """
        try:
            result = sp.diff(self.func_expr, x, order)
            logger.info(f"{order} 階導數計算成功: {result}")
            return Calculus(result)
        except Exception as e:
            logger.error(f"導數計算失敗: {str(e)}")
            raise ValueError("導數計算錯誤")

    def evaluate(self, x_value: float) -> float:
        """
        # 計算函數在特定點的值
        
        ## 參數
        * `x_value`: x 的值
        
        ## 返回
        * 函數值
        """
        try:
            result = float(self.func_expr.subs(x, x_value))
            logger.info(f"函數在 x = {x_value} 處的值為 {result}")
            return result
        except Exception as e:
            logger.error(f"函數值計算失敗: {str(e)}")
            raise ValueError("函數值計算錯誤")

    def indefinite_integral(self) -> 'Calculus':
        """
        # 計算不定積分
        
        ## 返回
        * 不定積分結果
        """
        try:
            result = sp.integrate(self.func_expr, x)
            logger.info(f"不定積分計算成功: {result}")
            return Calculus(result)
        except Exception as e:
            logger.error(f"不定積分計算失敗: {str(e)}")
            raise ValueError("不定積分計算錯誤")

    def definite_integral(self, lower: float, upper: float) -> float:
        """
        # 計算定積分
        
        ## 參數
        * `lower`: 積分下限
        * `upper`: 積分上限
        
        ## 返回
        * 定積分值
        """
        try:
            result = float(sp.integrate(self.func_expr, (x, lower, upper)))
            logger.info(f"定積分從 {lower} 到 {upper} 的值為 {result}")
            return result
        except Exception as e:
            logger.error(f"定積分計算失敗: {str(e)}")
            raise ValueError("定積分計算錯誤")

    def limit(self, point: float, direction: Optional[str] = None) -> float:
        """
        # 計算極限
        
        ## 參數
        * `point`: 趨近點
        * `direction`: 趨近方向 ('left', 'right', None)
        
        ## 返回
        * 極限值
        """
        try:
            if direction == 'left':
                result = float(sp.limit(self.func_expr, x, point, dir='-'))
            elif direction == 'right':
                result = float(sp.limit(self.func_expr, x, point, dir='+'))
            else:
                result = float(sp.limit(self.func_expr, x, point))
            logger.info(f"極限計算在 x -> {point} ({direction if direction else 'both'}) 的值為 {result}")
            return result
        except Exception as e:
            logger.error(f"極限計算失敗: {str(e)}")
            raise ValueError("極限計算錯誤")

    def taylor_series(self, point: float, order: int) -> 'Calculus':
        """
        # 計算泰勒級數展開
        
        ## 參數
        * `point`: 展開點
        * `order`: 展開階數
        
        ## 返回
        * 泰勒級數
        """
        try:
            result = sp.series(self.func_expr, x, point, order).removeO()
            logger.info(f"在 x = {point} 處的 {order} 階泰勒展開成功")
            return Calculus(result)
        except Exception as e:
            logger.error(f"泰勒展開失敗: {str(e)}")
            raise ValueError("泰勒展開錯誤")

    def plot(self, start: float = -10, end: float = 10, points: int = 1000) -> None:
        """
        # 繪製函數圖形
        
        ## 參數
        * `start`: x 軸起始值
        * `end`: x 軸結束值
        * `points`: 採樣點數
        """
        try:
            x_vals = np.linspace(start, end, points)
            y_vals = [self.evaluate(float(x_val)) for x_val in x_vals]
            
            plt.figure(figsize=(10, 6))
            plt.plot(x_vals, y_vals, label=f'f(x) = {self.func_expr}')
            plt.grid(True)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('Function Plot')
            plt.legend()
            plt.show()
            
            logger.info("函數圖形繪製成功")
        except Exception as e:
            logger.error(f"函數圖形繪製失敗: {str(e)}")
            raise ValueError("函數圖形繪製錯誤")

    def find_critical_points(self) -> List[float]:
        """
        # 尋找函數的臨界點
        
        ## 返回
        * 臨界點列表
        """
        try:
            derivative = self.derivative()
            critical_points = sp.solve(derivative.func_expr, x)
            critical_points = [float(point.evalf()) for point in critical_points if point.is_real]
            logger.info(f"找到的臨界點: {critical_points}")
            return critical_points
        except Exception as e:
            logger.error(f"臨界點計算失敗: {str(e)}")
            raise ValueError("臨界點計算錯誤")

class Matrix:
    """
    矩陣相關功能的核心類
    """

    def __init__(self, data):
        """
        # 初始化矩陣
        
        ## 參數
        - `data`: 二維列表表示的矩陣或其他可轉換為矩陣的格式
        
        ## 異常
        - ValueError: 當輸入的矩陣格式不正確時
        """
        try:
            if isinstance(data, str):
                converted_data = mu.convert_to_matrix(data)
                logger.info(f"矩陣初始化成功，維度為 {converted_data.shape[0]}x{converted_data.shape[1]}")
            else:
                # 檢查資料維度
                if isinstance(data, list):
                    if not data or not isinstance(data[0], list):
                        raise ValueError("輸入必須是二維列表")
                    rows = len(data)
                    cols = len(data[0])
                    if not all(len(row) == cols for row in data):
                        raise ValueError("所有行的長度必須相同")
                    converted_data = np.array(data)
                elif isinstance(data, np.ndarray):
                    if data.ndim != 2:
                        raise ValueError("NumPy 陣列必須是二維的")
                    converted_data = data
                else:
                    raise ValueError("輸入必須是字串、列表或 NumPy 陣列")
            
            self.data = converted_data
            self.rows = self.data.shape[0] 
            self.cols = self.data.shape[1]
            logger.info(f"矩陣初始化成功，維度為 {self.rows}x{self.cols}")
        except Exception as e:
            logger.error(f"矩陣初始化失敗: {str(e)}")
            raise ValueError(f"無效的矩陣格式: {str(e)}")
        
    
    def _check_dimensions(self, other: 'Matrix', operation: str):
        """
        # 檢查矩陣維度是否相同
        
        ## 參數
        - `other`: 另一個要比較的矩陣
        - `operation`: 要執行的運算名稱
        
        ## 異常
        - ValueError: 當矩陣維度不一致時拋出
        """
        if self.rows != other.rows or self.cols != other.cols:
            logger.error(f"矩陣{operation}失敗: 維度不一致")
            raise ValueError(f"矩陣的維度必須相同才能進行{operation}運算。")

    def __repr__(self, formatted: bool = True) -> str:
        """
        矩陣的字串表示
        
        Args:
            formatted: 是否格式化輸出，默認為True
            
        Returns:
            str: 矩陣的字串表示
        """
        if formatted:
            return self.format_matrix()
        else:
            return "\n".join([str(row) for row in self.data])

    def add(self, other: 'Matrix') -> 'Matrix':
        """
        矩陣加法
        :param other: 另一個矩陣
        :return: 相加後的矩陣
        """
        self._check_dimensions(other, "加法")
        result = [
            [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        logger.info("矩陣加法成功")
        return Matrix(result)

    def subtract(self, other: 'Matrix') -> 'Matrix':
        """
        矩陣減法
        :param other: 另一個矩陣
        :return: 相減後的矩陣
        """
        self._check_dimensions(other, "減法")
        result = [
            [self.data[i][j] - other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        logger.info("矩陣減法成功")
        return Matrix(result)

    def multiply(self, other: 'Matrix') -> 'Matrix':
        """
        矩陣乘法
        :param other: 另一個矩陣
        :return: 相乘後的矩陣
        """
        self._check_dimensions(other, "乘法")
        result = [
            [
                sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                for j in range(other.cols)
            ]
            for i in range(self.rows)
        ]
        logger.info("矩陣乘法成功 : {result}")
        return Matrix(result)

    def transpose(self) -> 'Matrix':
        """
        矩陣轉置
        :return: 轉置後的矩陣
        """
        result = [[self.data[j][i] for j in range(self.rows)] for i in range(self.cols)]
        logger.info("矩陣轉置成功")
        return Matrix(result)

    def determinant(self) -> float:
        """
        計算方陣的行列式
        :return: 行列式的值
        """
        if not self.is_square():
            logger.error("行列式計算失敗: 非方陣")
            raise ValueError("只有方陣才能計算行列式。")

        def _det_recursive(matrix: List[List[float]]) -> float:
            if len(matrix) == 1:
                return matrix[0][0]
            if len(matrix) == 2:
                return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
            det = 0
            for col in range(len(matrix)):
                minor = [row[:col] + row[col + 1:] for row in matrix[1:]]
                det += ((-1) ** col) * matrix[0][col] * _det_recursive(minor)
            return det

        determinant_value = _det_recursive(self.data)
        logger.info(f"行列式計算成功: {determinant_value}")
        return determinant_value

    def inverse(self) -> 'Matrix':
        """
        計算方陣的逆矩陣
        :return: 逆矩陣
        """
        if not self.is_square():
            logger.error("逆矩陣計算失敗: 非方陣")
            raise ValueError("只有方陣才能計算逆矩陣。")
        if self.determinant() == 0:
            logger.error("逆矩陣計算失敗: 奇異矩陣")
            raise ValueError("此矩陣是奇異矩陣，無法求逆。")
        
        # 計算逆矩陣（省略詳盡實現）
        # ...

    def is_square(self) -> bool:
        """
        檢查矩陣是否為方陣
        :return: 是否為方陣
        """
        return self.rows == self.cols

    def format_matrix(self):
        """
        # 格式化矩陣輸出
        
        將矩陣格式化為對齊的字串表示。
        
        ## 返回
        - 格式化後的矩陣字串，每個數字右對齊，並用方括號包圍
        
        ## 範例
        ```python
        matrix = Matrix([[1, 22, 333], [4444, 55555, 666666]])
        print(matrix.format_matrix())
        # [   1    22    333]
        # [4444 55555 666666]
        ```
        """
        # 找出最長數字的寬度
        width = max(len(str(num)) for row in self.data for num in row)
        # 使用格式化字符串對齊
        formatted_rows = []
        for row in self.data:
            formatted_row = [f"{num:>{width}}" for num in row]
            formatted_rows.append("[" + " ".join(formatted_row) + "]")
        return "\n".join(formatted_rows)
    
    def show(self):
        """
        # 顯示矩陣
        
        將矩陣以格式化的方式輸出到控制台。
        使用 __repr__() 方法的格式化輸出。
        
        ## 範例
        ```python
        matrix = Matrix([[1, 2], [3, 4]])
        matrix.show()
        # [1 2]
        # [3 4]
        ```
        """
        logger.info(f"顯示矩陣，維度為 {self.rows}x{self.cols}")
        print(self.__repr__())
    
    def __size__(self):
        """
        # 返回矩陣的維度
        
        ## 返回
        - 矩陣的維度
        """
        logger.info(f"獲取矩陣維度: {self.rows}x{self.cols}")
        return self.rows, self.cols
    
    def __len__(self):
        """
        # 返回矩陣的元素數量
        
        ## 返回
        - 矩陣的元素數量
        """
        elements = self.rows * self.cols
        logger.info(f"獲取矩陣元素數量: {elements}")
        return elements
    
    def __getitem__(self, index: int) -> List[float]:
        """
        # 返回矩陣的第 index 行
        
        ## 參數
        - `index`: 要返回的行數
        
        ## 返回
        - 矩陣的第 index 行
        """
        try:
            row = self.data[index]
            logger.info(f"獲取矩陣第 {index} 行: {row}")
            return row
        except IndexError as e:
            logger.error(f"獲取矩陣行失敗: 索引 {index} 超出範圍")
            raise IndexError(f"索引 {index} 超出矩陣範圍")
    
    def __setitem__(self, index: int, value: List[float]) -> None:
        """
        # 設定矩陣的第 index 行
        
        ## 參數
        - `index`: 要設定的行數
        - `value`: 要設定的行
        """
        try:
            if len(value) != self.cols:
                logger.error(f"設定矩陣行失敗: 新行的長度 {len(value)} 與矩陣列數 {self.cols} 不符")
                raise ValueError(f"新行的長度必須為 {self.cols}")
            self.data[index] = value
            logger.info(f"設定矩陣第 {index} 行為: {value}")
        except IndexError as e:
            logger.error(f"設定矩陣行失敗: 索引 {index} 超出範圍")
            raise IndexError(f"索引 {index} 超出矩陣範圍")
    
    def __iter__(self):
        """
        # 返回矩陣的迭代器
        
        ## 返回
        - 矩陣的迭代器
        """
        logger.info("開始矩陣迭代")
        return iter(self.data)
    
    def __contains__(self, item: float) -> bool:
        """
        # 檢查矩陣是否包含某個元素
        
        ## 參數
        - `item`: 要檢查的元素
        
        ## 返回
        - 是否包含該元素
        """
        result = item in self.data
        logger.info(f"檢查元素 {item} 是否在矩陣中: {'是' if result else '否'}")
        return result
    
    def __eq__(self, other: 'Matrix') -> bool:
        """
        # 檢查兩個矩陣是否相等
        """
        result = self.data == other.data
        logger.info(f"比較兩個矩陣是否相等: {'是' if result else '否'}")
        return result
    
    def to_list(self) -> List[float]:
        """
        # 將矩陣轉換為一維列表
        
        ## 返回
        - 包含矩陣所有元素的一維列表
        """
        try:
            flattened = self.data.flatten().tolist()
            logger.info(f"矩陣成功轉換為一維列表，長度為 {len(flattened)}")
            return flattened
        except Exception as e:
            logger.error(f"矩陣轉換失敗: {str(e)}")
            raise ValueError("矩陣轉換錯誤")

class Vector_space:
    """
    # 向量空間類別
    
    提供向量空間運算的核心類別。
    """

    def __init__(self, vector: List[float] = None):
        """
        # 初始化向量
        
        ## 參數
        - `vector`: 以一維列表表示的向量
        """
        if vector is not None and not isinstance(vector, list):
            logger.error("向量初始化失敗: 資料類型錯誤")
            raise ValueError("向量必須是一維列表。")
        self.vector = vector if vector else []
        self.dimension = len(self.vector)
        logger.info("向量初始化成功")

    def dot_product(self, other: 'Vector_space') -> float:
        """
        # 計算內積
        
        ## 參數
        - `other`: 另一個向量物件
        
        ## 回傳
        - 內積計算結果
        """
        if self.dimension != other.dimension:
            logger.error("內積計算失敗: 向量維度不一致")
            raise ValueError("向量維度必須相同。")
        
        result = sum(a * b for a, b in zip(self.vector, other.vector))
        logger.info(f"內積計算成功: {result}")
        return result

    def cross_product(self, other: 'Vector_space') -> 'Vector_space':
        """
        # 計算外積
        
        ## 參數
        - `other`: 另一個向量物件
        
        ## 回傳
        - 外積計算結果的向量物件
        
        ## 說明
        - 僅適用於三維向量
        """
        if self.dimension != 3 or other.dimension != 3:
            logger.error("外積計算失敗: 向量維度必須為3")
            raise ValueError("外積只能在三維向量間計算。")

        result = [
            self.vector[1] * other.vector[2] - self.vector[2] * other.vector[1],
            self.vector[2] * other.vector[0] - self.vector[0] * other.vector[2],
            self.vector[0] * other.vector[1] - self.vector[1] * other.vector[0]
        ]
        logger.info("外積計算成功")
        return Vector_space(result)

    def norm(self) -> float:
        """
        計算向量的範數（長度）
        :return: 向量範數
        """
        result = np.sqrt(sum(x * x for x in self.vector))
        logger.info(f"範數計算成功: {result}")
        return result

    def normalize(self) -> 'Vector_space':
        """
        向量正規化
        :return: 正規化後的向量
        """
        norm = self.norm()
        if norm == 0:
            logger.error("正規化失敗: 零向量")
            raise ValueError("零向量無法正規化。")
        
        result = [x / norm for x in self.vector]
        logger.info("向量正規化成功")
        return Vector_space(result)

    def angle_between(self, other: 'Vector_space') -> float:
        """
        計算兩個向量之間的夾角（以弧度為單位）
        :param other: 另一個向量
        :return: 夾角（弧度）
        """
        dot_prod = self.dot_product(other)
        norms = self.norm() * other.norm()
        
        if norms == 0:
            logger.error("夾角計算失敗: 存在零向量")
            raise ValueError("零向量無法計算夾角。")
        
        cos_theta = dot_prod / norms
        # 處理數值誤差
        cos_theta = min(1.0, max(-1.0, cos_theta))
        angle = np.arccos(cos_theta)
        logger.info(f"夾角計算成功: {angle} 弧度")
        return angle

    def projection(self, other: 'Vector_space') -> 'Vector_space':
        """
        計算此向量在另一個向量上的投影
        :param other: 投影基底向量
        :return: 投影向量
        """
        if other.norm() == 0:
            logger.error("投影計算失敗: 基底為零向量")
            raise ValueError("無法投影到零向量上。")
        
        scalar = self.dot_product(other) / (other.norm() ** 2)
        result = [scalar * x for x in other.vector]
        logger.info("投影計算成功")
        return Vector_space(result)

    def is_orthogonal(self, other: 'Vector_space') -> bool:
        """
        檢查兩個向量是否正交
        :param other: 另一個向量
        :return: 是否正交
        """
        return abs(self.dot_product(other)) < 1e-10

__all__ = [
    "Calculus",
    "Matrix",
    "Vector_space"
]

