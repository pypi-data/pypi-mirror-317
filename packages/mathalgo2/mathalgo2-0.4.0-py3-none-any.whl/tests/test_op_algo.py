import pytest
import numpy as np
from mathalgo2.algorithm.OpAlgo import BaseOptimizer, OptimizationFactory

def simple_objective(x):
    """簡單的測試目標函數：求和的平方"""
    return np.sum(x ** 2)

@pytest.fixture
def test_optimizer():
    """用於測試的簡單優化器實例"""
    class TestOptimizer(BaseOptimizer):
        def _optimize(self, **kwargs):
            solution = self._initialize_solution()
            fitness = self.objective_func(solution)
            self._update_best_solution(solution, fitness)
            return solution, fitness
    
    bounds = [(-5, 5), (-5, 5)]  # 2D 問題
    return TestOptimizer(simple_objective, bounds, test_mode=True)

class TestBaseOptimizer:
    def test_initialization(self, test_optimizer):
        """測試優化器初始化"""
        assert test_optimizer.dimension == 2
        assert test_optimizer.best_solution is None
        assert test_optimizer.best_fitness == float('inf')
        assert len(test_optimizer.history) == 0
        assert test_optimizer.fig is None
        assert test_optimizer.ax is None

    def test_bounds_clipping(self, test_optimizer):
        """測試解的邊界限制"""
        solution = np.array([10, -10])  # 超出邊界的解
        clipped = test_optimizer._clip_to_bounds(solution)
        assert np.all(clipped <= 5)
        assert np.all(clipped >= -5)

    def test_solution_initialization(self, test_optimizer):
        """測試解的初始化"""
        solution = test_optimizer._initialize_solution()
        assert solution.shape == (2,)
        assert np.all(solution >= -5)
        assert np.all(solution <= 5)

    def test_best_solution_update(self, test_optimizer):
        """測試最佳解更新"""
        solution = np.array([1.0, 1.0])
        fitness = simple_objective(solution)
        test_optimizer._update_best_solution(solution, fitness)
        assert np.array_equal(test_optimizer.best_solution, solution)
        assert test_optimizer.best_fitness == fitness
        assert len(test_optimizer.history) == 1

class TestOptimizationFactory:
    @pytest.fixture
    def factory_instance(self):
        """建立優化工廠測試實例"""
        bounds = [(-5, 5), (-5, 5)]  # 2D 問題
        return OptimizationFactory(simple_objective, bounds, test_mode=True)

    def test_factory_initialization(self, factory_instance):
        """測試工廠初始化"""
        assert factory_instance.objective_func == simple_objective
        assert len(factory_instance.bounds) == 2
        assert factory_instance.test_mode is True

    def test_create_optimizer(self, factory_instance):
        """測試創建優化器"""
        optimizers = ["genetic", "annealing", "gradient"]
        for opt_name in optimizers:
            optimizer = factory_instance.create_optimizer(opt_name)
            assert isinstance(optimizer, BaseOptimizer)
            assert optimizer.dimension == 2
            assert optimizer.objective_func == simple_objective
            assert optimizer.test_mode is True

    def test_invalid_algorithm(self, factory_instance):
        """測試無效的算法名稱"""
        with pytest.raises(ValueError):
            factory_instance.create_optimizer("invalid_algorithm")

    def test_register_algorithm(self, factory_instance):
        """測試註冊新算法"""
        class TestOptimizer(BaseOptimizer):
            def _optimize(self, **kwargs):
                solution = self._initialize_solution()
                fitness = self.objective_func(solution)
                self._update_best_solution(solution, fitness)
                return solution, fitness
        
        OptimizationFactory.register_algorithm("test", TestOptimizer)
        optimizer = factory_instance.create_optimizer("test")
        assert isinstance(optimizer, TestOptimizer)

    def test_register_invalid_algorithm(self):
        """測試註冊無效的算法類"""
        class InvalidOptimizer:
            pass
            
        with pytest.raises(TypeError):
            OptimizationFactory.register_algorithm("invalid", InvalidOptimizer)

    def test_optimization_with_custom_params(self, factory_instance):
        """測試帶自定義參數的優化器創建"""
        custom_params = {
            "population_size": 50
        }
        optimizer = factory_instance.create_optimizer("genetic", **custom_params)
        assert isinstance(optimizer, BaseOptimizer)
        assert hasattr(optimizer, "population_size")
        assert optimizer.population_size == 50 