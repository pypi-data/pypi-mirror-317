from typing import Union, Optional, List, Tuple
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from logger import setup_logger, logging
import os
from pathlib import Path

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

    def __init__(self, data: List[List[float]]):
        """
        初始化矩陣
        :param data: 二維列表表示的矩陣
        """
        if not data or not all(len(row) == len(data[0]) for row in data):
            logger.error("矩陣初始化失敗: 資料無效")
            raise ValueError("所有列必須具有相同的長度且資料不可為空。")
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0])
        logger.info("矩陣初始化成功")
    
    def _check_dimensions(self, other: 'Matrix', operation: str):
        if self.rows != other.rows or self.cols != other.cols:
            logger.error(f"矩陣{operation}失敗: 維度不一致")
            raise ValueError(f"矩陣的維度必須相同才能進行{operation}運算。")

    def __repr__(self) -> str:
        """
        矩陣的字串表示
        """
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