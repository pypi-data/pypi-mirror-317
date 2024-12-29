from typing import List, Any, Optional, Dict, Type
import matplotlib.pyplot as plt
import numpy as np
from mathalgo2.Logger import Logger, logging

class Searching:
    """搜尋算法類別"""
    
    algorithms = {}  # 類變量，用於存儲註冊的算法
    
    @classmethod
    def register_algorithm(cls, name: str, func):
        """註冊新的搜尋算法
        
        Args:
            name: 算法名稱
            func: 算法函數
        """
        cls.algorithms[name] = func
    
    def __init__(self, arr: List[Any], test_mode: bool = False):
        """初始化搜尋算法
        
        Args:
            arr: 要搜尋的數組
            test_mode: 是否為測試模式（不創建視覺化）
        """
        self.arr = arr.copy()  # 創建數組的副本
        self.logger = Logger(
            name="SearchAlgo",
            log_file="__log__/SearchAlgo.log"
        ).get_logger()
        
        # 只在非測試模式下初始化視覺化
        if not test_mode:
            try:
                self.fig, self.ax = plt.subplots(figsize=(12, 6))
            except Exception as e:
                self.logger.warning(f"無法創建視覺化: {e}")
                self.fig = None
                self.ax = None
        else:
            self.fig = None
            self.ax = None
            
        self.logger.info(f"初始化搜尋算法，數組長度: {len(arr)}")

    def binary_search(self, target: Any) -> Optional[int]:
        """二分搜尋
        
        Args:
            target: 要搜尋的目標值
            
        Returns:
            Optional[int]: 目標值的索引，如果未找到則返回None
        """
        if not self.arr:
            return None
            
        left, right = 0, len(self.arr) - 1
        
        while left <= right:
            mid = (left + right) // 2
            if self.arr[mid] == target:
                return mid
            elif self.arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return None

    def linear_search(self, target: Any) -> Optional[int]:
        """線性搜尋
        
        Args:
            target: 要搜尋的目標值
            
        Returns:
            Optional[int]: 目標值的索引，如果未找到則返回None
        """
        for i, value in enumerate(self.arr):
            if value == target:
                return i
        return None

    def search(self, algorithm: str, target: Any) -> Optional[int]:
        """執行指定的搜尋算法
        
        Args:
            algorithm: 要使用的算法名稱
            target: 要搜尋的目標值
            
        Returns:
            Optional[int]: 目標值的索引，如果未找到則返回None
            
        Raises:
            ValueError: 如果指定的算法不存在
        """
        if algorithm not in self.algorithms:
            raise ValueError(f"不支援的算法: {algorithm}")
            
        return self.algorithms[algorithm](self, target)

# 註冊內建算法
Searching.register_algorithm("binary", Searching.binary_search)
Searching.register_algorithm("linear", Searching.linear_search)

