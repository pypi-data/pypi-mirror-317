from mathalgo2.algorithm.OpAlgo import BaseOptimizer
import numpy as np
from typing import Tuple, Callable, List

class GeneticAlgorithm(BaseOptimizer):
    def __init__(self, objective_func: Callable, bounds: List[Tuple[float, float]], 
                 population_size: int = 50, test_mode: bool = False, **kwargs):
        """初始化遺傳算法
        
        Args:
            objective_func: 目標函數
            bounds: 解的範圍限制
            population_size: 種群大小
            test_mode: 是否為測試模式
            **kwargs: 其他參數
        """
        super().__init__(objective_func, bounds, test_mode=test_mode, **kwargs)
        self.population_size = population_size
        self.logger.info(f"初始化GeneticAlgorithm最佳化器，種群大小: {self.population_size}")

    def _optimize(self, **kwargs) -> Tuple[np.ndarray, float]:
        """執行遺傳算法優化"""
        solution = self._initialize_solution()
        fitness = self.objective_func(solution)
        self._update_best_solution(solution, fitness)
        return self.best_solution, self.best_fitness 