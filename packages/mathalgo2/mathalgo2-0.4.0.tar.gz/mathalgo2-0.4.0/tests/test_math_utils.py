import pytest
from mathalgo2.MathUtiles import MathUtils
import numpy as np

class TestMathUtils:
    def test_infix_to_postfix(self):
        # 測試基本運算
        assert MathUtils.infix_to_postfix("2+3*4") == ['2', '3', '4', '*', '+']
        assert MathUtils.infix_to_postfix("(1+2)*3") == ['1', '2', '+', '3', '*']
        
        # 測試錯誤情況
        with pytest.raises(ValueError):
            MathUtils.infix_to_postfix("((1+2)")  # 括號不匹配
            
    def test_evaluate_postfix(self):
        # 測試基本運算
        assert MathUtils.evaluate_postfix(['2', '3', '+']) == 5
        assert MathUtils.evaluate_postfix(['2', '3', '4', '*', '+']) == 14
        
        # 測試除以零
        assert MathUtils.evaluate_postfix(['1', '0', '/']) == float('inf')
        
        # 測試錯誤情況
        with pytest.raises(ValueError):
            MathUtils.evaluate_postfix(['1', '+'])  # 操作數不足
            
    def test_prime_factorization(self):
        assert MathUtils.prime_factorization(12) == [2, 2, 3]
        assert MathUtils.prime_factorization(17) == [17]
        
        with pytest.raises(ValueError):
            MathUtils.prime_factorization(-1)
            MathUtils.prime_factorization(0)
            
    def test_factorization(self):
        assert MathUtils.factorization(12) == [[1, 12], [2, 6], [3, 4], [4, 3], [6, 2], [12, 1]]
        assert MathUtils.factorization(7) == [[1, 7], [7, 1]]
        
        with pytest.raises(ValueError):
            MathUtils.factorization(-1)
            
    def test_convert_to_matrix(self):
        # 測試正常情況
        input_str = "1 2 3 4"
        expected = np.array([[1, 2], [3, 4]])
        assert np.array_equal(MathUtils.convert_to_matrix(input_str), expected)
        
    def test_convert_input_to_int_list(self):
        assert MathUtils.convert_input_to_int_list("1 2,3 4") == [1, 2, 3, 4]
        assert MathUtils.convert_input_to_int_list("1,2,3") == [1, 2, 3]
        
        with pytest.raises(ValueError):
            MathUtils.convert_input_to_int_list("1 a 3")
            
    def test_combination(self):
        assert MathUtils.combination(5, 2) == 10
        assert MathUtils.combination(5, 0) == 1
        assert MathUtils.combination(5, 5) == 1
        assert MathUtils.combination(5, 6) == 0
        
    def test_permutation(self):
        assert MathUtils.permutation(5, 2) == 20
        assert MathUtils.permutation(5, 5) == 120
        assert MathUtils.permutation(5, 0) == 1
        assert MathUtils.permutation(5, 6) == 0
        
    def test_factorial(self):
        assert MathUtils.factorial(5) == 120
        assert MathUtils.factorial(0) == 1
        
        with pytest.raises(ValueError):
            MathUtils.factorial(-1)
            
    def test_gcd(self):
        assert MathUtils.gcd(48, 18) == 6
        assert MathUtils.gcd(0, 5) == 5
        assert MathUtils.gcd(-48, 18) == 6
        
    def test_lcm(self):
        assert MathUtils.lcm(12, 18) == 36
        assert MathUtils.lcm(0, 5) == 0
        assert MathUtils.lcm(-12, 18) == 36
        
    def test_is_prime(self):
        assert MathUtils.is_prime(2) == True
        assert MathUtils.is_prime(17) == True
        assert MathUtils.is_prime(4) == False
        assert MathUtils.is_prime(1) == False
        assert MathUtils.is_prime(0) == False
        assert MathUtils.is_prime(-1) == False
        
    def test_fibonacci(self):
        assert MathUtils.fibonacci(5) == [0, 1, 1, 2, 3]
        assert MathUtils.fibonacci(1) == [0]
        assert MathUtils.fibonacci(0) == []
        assert MathUtils.fibonacci(-1) == []
        
    def test_is_perfect_number(self):
        assert MathUtils.is_perfect_number(6) == True
        assert MathUtils.is_perfect_number(28) == True
        assert MathUtils.is_perfect_number(12) == False
        assert MathUtils.is_perfect_number(1) == False
        assert MathUtils.is_perfect_number(0) == False
        
    def test_euler_totient(self):
        assert MathUtils.euler_totient(10) == 4
        assert MathUtils.euler_totient(1) == 1
        
        with pytest.raises(ValueError):
            MathUtils.euler_totient(0)
            MathUtils.euler_totient(-1)
            
    def test_extended_gcd(self):
        d, x, y = MathUtils.extended_gcd(35, 15)
        assert d == 5
        assert 35 * x + 15 * y == d
        
    def test_catalan_number(self):
        assert MathUtils.catalan_number(0) == 1
        assert MathUtils.catalan_number(1) == 1
        assert MathUtils.catalan_number(2) == 2
        assert MathUtils.catalan_number(3) == 5
        
        with pytest.raises(ValueError):
            MathUtils.catalan_number(-1) 