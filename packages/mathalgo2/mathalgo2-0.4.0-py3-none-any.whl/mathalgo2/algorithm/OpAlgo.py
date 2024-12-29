from typing import List, Dict, Any, Optional, Tuple, Union, Callable
from typing import Type  # 明確導入 Type
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import numpy as np
from mathalgo2.Logger import Logger, logging
import os
from pathlib import Path

# 設置根目錄和日誌
ROOT_DIR = Path(__file__).parent.parent.parent
log_file = ROOT_DIR / "__log__" / "OpAlgo.log"

# 初始化日誌管理器
logger_manager = Logger(
    name="OpAlgo",
    log_file=str(log_file),
    level=logging.INFO
)

class BaseOptimizer(ABC):
    """最佳化算法的基類
    
    此類提供最佳化算法的基本框架，包含:
    - 目標函數管理
    - 解的範圍限制
    - 最佳解追蹤
    - 視覺化功能
    - 日誌記錄
    
    Attributes:
        objective_func (Callable): 目標函數
        bounds (List[Tuple[float, float]]): 每個維度的取值範圍
        dimension (int): 問題維度
        best_solution (np.ndarray): 目前找到的最佳解
        best_fitness (float): 最佳解的適應度值
        history (List[float]): 最佳適應度的歷史記錄
        logger (logging.Logger): 日誌記錄器
        fig (plt.Figure): matplotlib圖形物件
        ax (plt.Axes): matplotlib座標軸物件
    """
    
    def __init__(self, objective_func: Callable, bounds: List[Tuple[float, float]], test_mode: bool = False, **kwargs):
        """初始化最佳化器"""
        self.logger = logger_manager
        self.logger.info(f"初始化{self.__class__.__name__}最佳化器")
        
        self.objective_func = objective_func
        self.bounds = bounds
        self.dimension = len(bounds)
        self.best_solution = None
        self.best_fitness = float('inf')
        self.history = []
        self.test_mode = test_mode
        
        if not self.test_mode:
            try:
                self.fig, self.ax = plt.subplots(figsize=(10, 6))
            except Exception as e:
                self.logger.warning(f"無法創建圖形界面: {e}")
                self.fig = None
                self.ax = None
        else:
            self.fig = None
            self.ax = None

    def optimize(self, **kwargs) -> Tuple[np.ndarray, float]:
        """執行最佳化過程"""
        return self._optimize(**kwargs)

    @abstractmethod
    def _optimize(self, **kwargs) -> Tuple[np.ndarray, float]:
        """執行最佳化過程的具體實現（抽象方法）"""
        pass

    def _initialize_solution(self) -> np.ndarray:
        """初始化一個解"""
        solution = np.zeros(self.dimension)
        for i, (low, high) in enumerate(self.bounds):
            solution[i] = np.random.uniform(low, high)
        return solution

    def _clip_to_bounds(self, solution: np.ndarray) -> np.ndarray:
        """將解限制在邊界內"""
        for i, (low, high) in enumerate(self.bounds):
            solution[i] = np.clip(solution[i], low, high)
        return solution

    def _update_best_solution(self, solution: np.ndarray, fitness: float):
        """更新最佳解"""
        if fitness < self.best_fitness:
            self.best_solution = solution.copy()
            self.best_fitness = fitness
            self.history.append(fitness)

# 從各自的模組中導入最佳化算法
from mathalgo2.algorithm.optimizers.genetic import GeneticAlgorithm
from mathalgo2.algorithm.optimizers.simulated_annealing import SimulatedAnnealing
from mathalgo2.algorithm.optimizers.gradient_descent import GradientDescent

class OptimizationFactory:
    """最佳化算法工廠類"""
    
    _algorithms = {}  # 移除預設的算法註冊
    
    @classmethod
    def register_algorithm(cls, name: str, algorithm_class: Type[BaseOptimizer]):
        """註冊新的優化算法"""
        if not issubclass(algorithm_class, BaseOptimizer):
            raise TypeError("算法類必須繼承自 BaseOptimizer")
        cls._algorithms[name] = algorithm_class
    
    def __init__(self, objective_func: Callable, bounds: List[Tuple[float, float]], test_mode: bool = False):
        self.objective_func = objective_func
        self.bounds = bounds
        self.test_mode = test_mode
        self.logger = logger_manager
        self.logger.info("初始化最佳化工廠")
    
    def create_optimizer(self, algorithm: str, **kwargs) -> BaseOptimizer:
        """創建最佳化器實例"""
        self.logger.info(f"創建{algorithm}最佳化器")
        if algorithm not in self.__class__._algorithms:
            self.logger.error(f"嘗試創建不支援的算法: {algorithm}")
            raise ValueError(f"不支援的算法: {algorithm}")
            
        all_kwargs = {
            'test_mode': self.test_mode,
            **kwargs
        }
            
        return self.__class__._algorithms[algorithm](
            self.objective_func, 
            self.bounds, 
            **all_kwargs
        )

# 註冊算法
from mathalgo2.algorithm.optimizers.genetic import GeneticAlgorithm
from mathalgo2.algorithm.optimizers.simulated_annealing import SimulatedAnnealing
from mathalgo2.algorithm.optimizers.gradient_descent import GradientDescent

OptimizationFactory.register_algorithm("genetic", GeneticAlgorithm)
OptimizationFactory.register_algorithm("annealing", SimulatedAnnealing)
OptimizationFactory.register_algorithm("gradient", GradientDescent)

__all__ = [
    "BaseOptimizer",
    "OptimizationFactory",
]

# 為測試目的添加簡單的優化器實現
class SimulatedAnnealing(BaseOptimizer):
    def __init__(self, objective_func: Callable, bounds: List[Tuple[float, float]], **kwargs):
        """初始化模擬退火算法"""
        super().__init__(objective_func, bounds)
        self.temperature = kwargs.get('temperature', 1000.0)
        self.cooling_rate = kwargs.get('cooling_rate', 0.95)

    def _optimize(self, **kwargs) -> Tuple[np.ndarray, float]:
        """執行模擬退火優化"""
        # 初始化
        current_solution = self._initialize_solution()
        current_fitness = self.objective_func(current_solution)
        self._update_best_solution(current_solution, current_fitness)
        
        # 簡單的實現用於測試
        return self.best_solution, self.best_fitness

class GeneticAlgorithm(BaseOptimizer):
    def __init__(self, objective_func: Callable, bounds: List[Tuple[float, float]], population_size: int = 50, **kwargs):
        """初始化遺傳算法"""
        super().__init__(objective_func, bounds)
        self.population_size = population_size

    def _optimize(self, **kwargs) -> Tuple[np.ndarray, float]:
        """執行遺傳算法優化"""
        solution = self._initialize_solution()
        fitness = self.objective_func(solution)
        self._update_best_solution(solution, fitness)
        return solution, fitness

class GradientDescent(BaseOptimizer):
    def __init__(self, objective_func: Callable, bounds: List[Tuple[float, float]], **kwargs):
        """初始化梯度下降算法"""
        super().__init__(objective_func, bounds)

    def _optimize(self, **kwargs) -> Tuple[np.ndarray, float]:
        """執行梯度下降優化"""
        solution = self._initialize_solution()
        fitness = self.objective_func(solution)
        self._update_best_solution(solution, fitness)
        return solution, fitness
