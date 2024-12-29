from typing import List, Dict, Any, Optional, Tuple, Union
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import numpy as np
from mathalgo2.logger import setup_logger, logging
import os
from pathlib import Path
from typing import Callable

# 設置根目錄和日誌
ROOT_DIR = Path(__file__).parent.parent.parent
log_file = ROOT_DIR / "__log__" / "OpAlgo.log"
logger = setup_logger("OpAlgo", log_file, level=logging.INFO)

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
    
    def __init__(self, objective_func: Callable, bounds: List[Tuple[float, float]]):
        """初始化最佳化器
        
        Args:
            objective_func: 目標函數，接受numpy陣列作為輸入
            bounds: 每個維度的取值範圍列表，每個元素為(最小值,最大值)
        """
        self.logger = logger
        self.logger.info(f"初始化{self.__class__.__name__}最佳化器")
        
        self.objective_func = objective_func
        self.bounds = bounds
        self.dimension = len(bounds)
        self.best_solution = None
        self.best_fitness = float('inf')
        self.history = []
        self.fig = None
        self.ax = None

    def optimize(self, *args, **kwargs) -> Tuple[np.ndarray, float]:
        """執行最佳化
        
        Args:
            *args: 傳遞給_optimize的位置參數
            **kwargs: 傳遞給_optimize的關鍵字參數
            
        Returns:
            Tuple[np.ndarray, float]: (最佳解, 最佳適應度值)
        """
        return self._optimize(*args, **kwargs)
        
    @abstractmethod
    def _optimize(self, **kwargs) -> Tuple[np.ndarray, float]:
        """實際的最佳化實現
        
        Args:
            **kwargs: 算法特定的參數
            
        Returns:
            Tuple[np.ndarray, float]: (最佳解, 最佳適應度值)
        """
        pass

    def visualize(self, *args, **kwargs):
        """視覺化最佳化過程"""
        self.logger.info("開始視覺化最佳化過程")
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.ax.set_title(f"{self.__class__.__name__} Optimization Progress")
        self.ax.set_xlabel("Iteration")
        self.ax.set_ylabel("Objective Value")
        
        # 執行最佳化，確保參數正確傳遞
        result = self.optimize(**kwargs)
        
        plt.ioff()
        plt.show()
        self.logger.info("視覺化完成")
        return result

    def _update_plot(self, iteration: int):
        """更新優化過程圖表
        
        Args:
            iteration: 當前迭代次數
        """
        if self.fig is not None:
            self.ax.clear()
            self.ax.plot(self.history, 'b-', label='Best Fitness')
            self.ax.set_title(f"{self.__class__.__name__} Progress - Iteration {iteration}")
            self.ax.set_xlabel("Iteration")
            self.ax.set_ylabel("Objective Value")
            self.ax.legend()
            plt.pause(0.01)

    def _update_best_solution(self, solution: np.ndarray, fitness: float, iteration: Optional[int] = None):
        """更新最佳解
        
        Args:
            solution: 候選解
            fitness: 候選解的適應度值
            iteration: 當前迭代次數(用於日誌)
        """
        if fitness < self.best_fitness:
            self.best_fitness = fitness
            self.best_solution = solution.copy()
            if iteration is not None:
                self.logger.info(f"迭代 {iteration}: 找到新的最佳解: {self.best_fitness}")

    def _initialize_solution(self) -> np.ndarray:
        """初始化解
        
        Returns:
            np.ndarray: 在指定範圍內隨機生成的初始解
        """
        self.logger.debug("初始化解")
        return np.random.uniform(
            low=[b[0] for b in self.bounds],
            high=[b[1] for b in self.bounds],
            size=self.dimension
        )

    def _clip_to_bounds(self, solution: np.ndarray) -> np.ndarray:
        """將解限制在邊界內
        
        Args:
            solution: 需要限制的解
            
        Returns:
            np.ndarray: 限制在邊界內的解
        """
        return np.clip(solution,
                      [b[0] for b in self.bounds],
                      [b[1] for b in self.bounds])

# 從各自的模組中導入最佳化算法
from mathalgo2.algorithm.optimizers.genetic import GeneticAlgorithm
from mathalgo2.algorithm.optimizers.simulated_annealing import SimulatedAnnealing
from mathalgo2.algorithm.optimizers.gradient_descent import GradientDescent

class OptimizationFactory:
    """最佳化算法工廠類"""
    
    _algorithms = {
        "genetic": GeneticAlgorithm,
        "annealing": SimulatedAnnealing,
        "gradient": GradientDescent
    }
    
    def __init__(self, objective_func: Callable, bounds: List[Tuple[float, float]]):
        self.objective_func = objective_func
        self.bounds = bounds
        self.logger = logger
        self.logger.info("初始化最佳化工廠")
    
    def create_optimizer(self, algorithm: str, **kwargs) -> BaseOptimizer:
        """創建最佳化器實例
        
        Args:
            algorithm: 算法名稱
            **kwargs: 傳遞給優化器的初始化參數
        """
        self.logger.info(f"創建{algorithm}最佳化器")
        if algorithm not in self.__class__._algorithms:
            self.logger.error(f"嘗試創建不支援的算法: {algorithm}")
            raise ValueError(f"不支援的算法: {algorithm}")
        return self.__class__._algorithms[algorithm](self.objective_func, self.bounds, **kwargs)

    @classmethod
    def register_algorithm(cls, name: str, algorithm_class: type):
        """註冊新的最佳化算法"""
        if not issubclass(algorithm_class, BaseOptimizer):
            cls.logger.error(f"嘗試註冊無效的算法類: {algorithm_class.__name__}")
            raise TypeError("算法類必須繼承BaseOptimizer")
        cls._algorithms[name] = algorithm_class
        cls.logger.info(f"成功註冊新算法: {name}")

# 為了向後兼容，保留原來的 Optimization 類
class Optimization(OptimizationFactory):
    """向後兼容的別名類"""
    pass

__all__ = [
    "Optimization"
]
