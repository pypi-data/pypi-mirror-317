import pytest
from mathalgo2.MathUtiles import MathUtils

class TestMathUtils:
    def test_precedence(self):
        assert MathUtils.precedence('+') == 1
        assert MathUtils.precedence('-') == 1
        assert MathUtils.precedence('*') == 2
        assert MathUtils.precedence('/') == 2
        assert MathUtils.precedence('^') == 3
        assert MathUtils.precedence('(') == 0
        assert MathUtils.precedence('invalid') == 0

    def test_infix_to_postfix(self):
        # 基本運算測試
        assert MathUtils.infix_to_postfix("2+3") == ['2', '3', '+']
        assert MathUtils.infix_to_postfix("2*3+4") == ['2', '3', '*', '4', '+']
        
        # 括號測試
        assert MathUtils.infix_to_postfix("(2+3)*4") == ['2', '3', '+', '4', '*']
        
        # 複雜表達式測試
        assert MathUtils.infix_to_postfix("3+4*2/(1-5)^2") == ['3', '4', '2', '*', '1', '5', '-', '2', '^', '/', '+']
        
        # 錯誤測試
        with pytest.raises(ValueError):
            MathUtils.infix_to_postfix("((2+3)")
        with pytest.raises(ValueError):
            MathUtils.infix_to_postfix("2+3)")

    def test_is_almost_equal(self):
        assert MathUtils.is_almost_equal(0.1 + 0.2, 0.3)
        assert MathUtils.is_almost_equal(1.0, 1.0)
        assert not MathUtils.is_almost_equal(1.0, 1.1)
        
        # 自定義容許誤差測試
        assert MathUtils.is_almost_equal(1.0, 1.01, tolerance=0.1)
        assert not MathUtils.is_almost_equal(1.0, 1.01, tolerance=0.001)

    def test_evaluate_postfix(self):
        # 基本運算測試
        assert MathUtils.evaluate_postfix(['2', '3', '+']) == 5.0
        assert MathUtils.evaluate_postfix(['2', '3', '*']) == 6.0
        assert MathUtils.evaluate_postfix(['6', '2', '/']) == 3.0
        assert MathUtils.evaluate_postfix(['2', '3', '^']) == 8.0
        
        # 複雜表達式測試
        assert MathUtils.evaluate_postfix(['3', '4', '2', '*', '1', '5', '-', '2', '^', '/', '+']) == 3.5
        
        # 除以零測試
        assert MathUtils.evaluate_postfix(['1', '0', '/']) == float('inf')
        
        # 錯誤測試
        with pytest.raises(ValueError):
            MathUtils.evaluate_postfix(['1', '+'])  # 操作數不足
        with pytest.raises(ValueError):
            MathUtils.evaluate_postfix(['1', '2', '3', '+'])  # 堆疊中剩餘多個值
        with pytest.raises(ValueError):
            MathUtils.evaluate_postfix(['1', '2', '&'])  # 不支援的運算符 