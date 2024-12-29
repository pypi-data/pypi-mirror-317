from mathalgo2.algorithm.OpAlgo import BaseOptimizer
import numpy as np
from typing import Tuple

class SimulatedAnnealing(BaseOptimizer):
    def __init__(self, objective_func, bounds, initial_temp=100.0, cooling_rate=0.95, **kwargs):
        """初始化模擬退火算法
        
        Args:
            objective_func: 目標函數
            bounds: 解的範圍限制
            initial_temp: 初始溫度
            cooling_rate: 降溫速率
            **kwargs: 其他參數
        """
        super().__init__(objective_func, bounds, **kwargs)
        self.temp = initial_temp
        self.cooling_rate = cooling_rate
        self.logger.info(f"初始化SimulatedAnnealing最佳化器，初始溫度: {self.temp}, 降溫速率: {self.cooling_rate}")

    def _optimize(self, max_iter=1000, **kwargs) -> Tuple[np.ndarray, float]:
        """執行模擬退火最佳化
        
        Args:
            max_iter: 最大迭代次數
            **kwargs: 其他參數
        
        Returns:
            Tuple[np.ndarray, float]: (最佳解, 最佳適應度值)
        """
        # 初始化解
        current_solution = self._initialize_solution()
        current_fitness = self.objective_func(current_solution)
        self.logger.info(f"初始解: {current_solution}, 初始適應度: {current_fitness}")
        
        for i in range(max_iter):
            # 生成鄰居解
            neighbor = current_solution + np.random.normal(0, self.temp, self.dimension)
            neighbor = self._clip_to_bounds(neighbor)
            neighbor_fitness = self.objective_func(neighbor)
            self.logger.debug(f"迭代 {i}: 生成鄰居解: {neighbor}, 鄰居適應度: {neighbor_fitness}")
            
            # 決定是否接受新解
            delta = neighbor_fitness - current_fitness
            if delta < 0 or np.random.random() < np.exp(-delta / self.temp):
                self.logger.info(f"迭代 {i}: 接受新解: {neighbor}, 適應度: {neighbor_fitness}")
                current_solution = neighbor
                current_fitness = neighbor_fitness
            else:
                self.logger.debug(f"迭代 {i}: 拒絕新解: {neighbor}, 適應度: {neighbor_fitness}")
            
            # 更新最佳解
            self._update_best_solution(current_solution, current_fitness)
            self.history.append(self.best_fitness)
            
            # 降低溫度
            self.temp *= self.cooling_rate
            self.logger.debug(f"迭代 {i}: 更新溫度: {self.temp}")
            
        self.logger.info(f"最佳化完成，最佳解: {self.best_solution}, 最佳適應度: {self.best_fitness}")
        return self.best_solution, self.best_fitness 