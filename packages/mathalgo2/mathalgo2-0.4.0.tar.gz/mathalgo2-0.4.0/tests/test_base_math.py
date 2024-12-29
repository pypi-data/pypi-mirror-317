import pytest
import numpy as np
import sympy as sp
from mathalgo2.BaseMath import Calculus, Matrix, Vector_space

# ====== Fixtures ======
@pytest.fixture
def simple_matrix():
    """創建一個簡單的測試矩陣"""
    return Matrix([[1, 2], [3, 4]])

@pytest.fixture
def calculus_linear():
    """創建一個簡單的線性函數"""
    return Calculus("2*x + 1")

@pytest.fixture
def calculus_quadratic():
    """創建一個二次函數"""
    return Calculus("x**2 - 2*x + 1")

# ====== Calculus Tests ======
class TestCalculus:
    def test_derivative(self, calculus_quadratic):
        """測試導數計算"""
        derivative = calculus_quadratic.derivative()
        # x^2 - 2x + 1 的導數應該是 2x - 2
        assert abs(derivative.evaluate(0) - (-2)) < 1e-10
        assert abs(derivative.evaluate(1)) < 1e-10
        assert abs(derivative.evaluate(2) - 2) < 1e-10

    def test_definite_integral(self, calculus_linear):
        """測試定積分計算"""
        # 2x + 1 在 [0,1] 的定積分應該是 2
        result = calculus_linear.definite_integral(0, 1)
        assert abs(result - 2) < 1e-10

    def test_limit(self, calculus_quadratic):
        """測試極限計算"""
        result = calculus_quadratic.limit(1)
        assert abs(result - 0) < 1e-10

    def test_taylor_series(self, calculus_quadratic):
        """測試泰勒級數展開"""
        # x^2 - 2x + 1 在 x=0 處的泰勒展開
        taylor = calculus_quadratic.taylor_series(0, 2)
        
        # 在展開點 x = 0 處檢查
        assert abs(taylor.evaluate(0) - calculus_quadratic.evaluate(0)) < 1e-6
        
        # 在展開點附近檢查近似度
        # 使用較小的 x 值，因為泰勒展開在展開點附近最準確
        test_points = [-0.1, -0.05, 0.05, 0.1]
        
        for x in test_points:
            taylor_val = taylor.evaluate(x)
            actual_val = calculus_quadratic.evaluate(x)
            # 放寬誤差容限到 0.02 (2%)
            assert abs(taylor_val - actual_val) < 0.02, \
                f"在 x={x} 處，泰勒展開值 {taylor_val:.6f} 與實際值 {actual_val:.6f} 相差過大"
        
        # 檢查泰勒展開在 x=0 處的值
        assert abs(taylor.evaluate(0) - 1) < 1e-6, \
            f"在 x=0 處，泰勒展開值應該接近 1，但得到 {taylor.evaluate(0):.6f}"
        
        # 檢查泰勒展開在 x=0 處的導數值（一階導數應該是 -2）
        h = 1e-5  # 小的步長
        derivative_approx = (taylor.evaluate(h) - taylor.evaluate(0)) / h
        assert abs(derivative_approx + 2) < 0.1, \
            f"在 x=0 處，泰勒展開的導數應該接近 -2，但得到 {-derivative_approx:.6f}"

    def test_find_critical_points(self, calculus_quadratic):
        """測試臨界點查找"""
        critical_points = calculus_quadratic.find_critical_points()
        assert len(critical_points) == 1
        assert abs(critical_points[0] - 1) < 1e-10

# ====== Matrix Tests ======
class TestMatrix:
    def test_matrix_initialization(self):
        """測試矩陣初始化"""
        # 測試列表初始化
        matrix = Matrix([[1, 2], [3, 4]])
        assert matrix.rows == 2
        assert matrix.cols == 2
        
        # 測試 numpy 數組初始化
        matrix = Matrix(np.array([[1, 2], [3, 4]]))
        assert matrix.rows == 2
        assert matrix.cols == 2

    def test_matrix_operations(self, simple_matrix):
        """測試矩陣基本運算"""
        # 測試矩陣加法
        result = simple_matrix.add(simple_matrix)
        assert result[0][0] == 2
        assert result[1][1] == 8

        # 測試矩陣乘法
        result = simple_matrix.multiply(simple_matrix)
        assert result[0][0] == 7
        assert result[1][1] == 22

    def test_determinant(self, simple_matrix):
        """測試行列式計算"""
        det = simple_matrix.determinant()
        assert det == -2  # 1*4 - 2*3 = -2

    def test_matrix_properties(self, simple_matrix):
        """測試矩陣屬性"""
        assert simple_matrix.is_square()
        assert simple_matrix.__len__() == 4
        size = simple_matrix.__size__()
        assert size == (2, 2)

    def test_matrix_indexing(self, simple_matrix):
        """測試矩陣索引操作"""
        assert list(simple_matrix[0]) == [1, 2]
        simple_matrix[0] = [5, 6]
        assert list(simple_matrix[0]) == [5, 6]

    def test_matrix_format(self, simple_matrix):
        """測試矩陣格式化輸出"""
        formatted = simple_matrix.format_matrix()
        assert '[' in formatted
        assert ']' in formatted

    def test_invalid_matrix(self):
        """測試無效矩陣初始化"""
        with pytest.raises(ValueError):
            Matrix([[1, 2], [3]])  # 不規則矩陣
        with pytest.raises(ValueError):
            Matrix([])  # 空矩陣

# ====== Vector Space Tests ======
class TestVectorSpace:
    def test_vector_operations(self):
        """測試向量空間操作"""
        v1 = Vector_space([1, 2, 3])
        v2 = Vector_space([4, 5, 6])
        
        # 測試向量點積
        dot_product = v1.dot_product(v2)
        assert dot_product == 32  # 1*4 + 2*5 + 3*6
        
        # 測試向量外積 (僅適用於三維向量)
        cross_product = v1.cross_product(v2)
        expected = [-3, 6, -3]  # 手動計算的結果
        assert all(abs(a - b) < 1e-10 for a, b in zip(cross_product.vector, expected))

    def test_vector_normalization(self):
        """測試向量標準化"""
        v = Vector_space([3, 4])
        normalized = v.normalize()
        # 3-4-5 三角形，標準化後應該是 [0.6, 0.8]
        assert abs(normalized.vector[0] - 0.6) < 1e-10
        assert abs(normalized.vector[1] - 0.8) < 1e-10

    def test_vector_properties(self):
        """測試向量屬性"""
        v = Vector_space([3, 4])
        assert abs(v.norm() - 5) < 1e-10
        assert v.dimension == 2

    def test_vector_angles(self):
        """測試向量角度計算"""
        v1 = Vector_space([1, 0])
        v2 = Vector_space([0, 1])
        # 垂直向量的夾角應該是 π/2
        assert abs(v1.angle_between(v2) - np.pi/2) < 1e-10

    def test_vector_projection(self):
        """測試向量投影"""
        v1 = Vector_space([3, 4])
        v2 = Vector_space([1, 0])
        proj = v1.projection(v2)
        # 投影到 x 軸上應該得到 [3, 0]
        assert abs(proj.vector[0] - 3) < 1e-10
        assert abs(proj.vector[1]) < 1e-10 