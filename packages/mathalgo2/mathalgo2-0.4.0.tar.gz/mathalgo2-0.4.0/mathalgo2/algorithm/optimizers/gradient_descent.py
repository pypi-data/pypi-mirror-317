from mathalgo2.algorithm.OpAlgo import BaseOptimizer
import numpy as np
from typing import Tuple, Callable, List

class GradientDescent(BaseOptimizer):
    def __init__(self, objective_func: Callable, bounds: List[Tuple[float, float]], **kwargs):
        """初始化梯度下降算法
        
        Args:
            objective_func: 目標函數
            bounds: 解的範圍限制
            **kwargs: 其他參數
        """
        super().__init__(objective_func, bounds, **kwargs)
        self.learning_rate = kwargs.get('learning_rate', 0.01)
        self.logger.info(f"初始化GradientDescent最佳化器，學習率: {self.learning_rate}")

    def _optimize(self, max_iter=1000, **kwargs) -> Tuple[np.ndarray, float]:
        """執行梯度下降優化
        
        Args:
            max_iter: 最大迭代次數
            **kwargs: 其他參數
        
        Returns:
            Tuple[np.ndarray, float]: (最佳解, 最佳適應度值)
        """
        # 初始化解
        current_solution = self._initialize_solution()
        current_fitness = self.objective_func(current_solution)
        self._update_best_solution(current_solution, current_fitness)
        self.logger.info(f"初始解: {current_solution}, 初始適應度: {current_fitness}")
        
        for i in range(max_iter):
            # 計算數值梯度
            gradient = np.zeros(self.dimension)
            epsilon = 1e-8
            for j in range(self.dimension):
                temp_solution = current_solution.copy()
                temp_solution[j] += epsilon
                gradient[j] = (self.objective_func(temp_solution) - current_fitness) / epsilon
            
            # 更新解
            current_solution = current_solution - self.learning_rate * gradient
            current_solution = self._clip_to_bounds(current_solution)
            current_fitness = self.objective_func(current_solution)
            
            # 更新最佳解
            self._update_best_solution(current_solution, current_fitness)
            self.history.append(self.best_fitness)
            
            self.logger.debug(f"迭代 {i}: 當前解: {current_solution}, 適應度: {current_fitness}")
            
        self.logger.info(f"最佳化完成，最佳解: {self.best_solution}, 最佳適應度: {self.best_fitness}")
        return self.best_solution, self.best_fitness 