from typing import List, Dict, Any, Optional, Tuple, Union
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from mathalgo2.logger import setup_logger, logging
import os
from pathlib import Path
from typing import Callable

"""
# SearchAlgo 模組

提供各種搜尋演算法的實作與視覺化功能。

## 主要功能
- 二分搜尋 (Binary Search)
- 線性搜尋 (Linear Search)
- 插值搜尋 (Interpolation Search) [待實現]
- 跳躍搜尋 (Jump Search) [待實作]

每個搜尋演算法都提供:
- 基本搜尋功能
- 視覺化過程
- 詳細日誌記錄
- 效能分析
"""

# 設置根目錄和日誌
ROOT_DIR = Path(__file__).parent.parent.parent
log_file = ROOT_DIR / "__log__" / "SearchAlgo.log"
logger = setup_logger("SearchAlgo", log_file, level=logging.INFO)

class Algorithm(ABC):
    """演算法基礎抽象類別
    
    提供所有搜尋演算法的共用介面和基本功能。
    """
    
    def __init__(self):
        """初始化基礎類別"""
        self.logger = logger
        
    @abstractmethod
    def visualize(self, *args, **kwargs):
        """視覺化方法的抽象介面"""
        pass

class SearchBase(ABC):
    """搜尋演算法基礎類別
    
    定義搜尋演算法的共用介面。
    """
    
    @abstractmethod
    def search(self, arr: List[Any], target: Any) -> Optional[int]:
        """執行搜尋
        
        Args:
            arr: 要搜尋的數列
            target: 搜尋目標
            
        Returns:
            目標值的索引，若未找到則返回 None
        """
        pass
        
    @abstractmethod
    def update_visualization(self, arr: List[Any], **kwargs):
        """更新視覺化
        
        Args:
            arr: 要視覺化的數列
            **kwargs: 視覺化所需的其他參數
        """
        pass

class BinarySearch(SearchBase):
    """二分搜尋演算法實作"""
    
    def search(self, arr: List[Any], target: Any) -> Optional[int]:
        """執行二分搜尋"""
        logger.info(f"開始二分搜尋: 目標值 = {target}")
        left, right = 0, len(arr) - 1
        
        # 取得視覺化物件 (如果有的話)
        ax = getattr(self, 'ax', None)
        
        while left <= right:
            mid = (left + right) // 2
            logger.debug(f"左={left}, 中={mid}, 右={right}")
            
            # 更新視覺化
            if ax:
                self.update_visualization(arr, ax, left, mid, right)
            
            if arr[mid] == target:
                logger.info(f"找到目標值於索引 {mid}")
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
                
        logger.info("未找到目標值")
        return None
        
    def update_visualization(self, arr: List[Any], ax: plt.Axes, left: int, mid: int, right: int):
        """更新二分搜尋視覺化"""
        ax.clear()
        bars = ax.bar(range(len(arr)), arr, color='lightblue')
        
        # 標記搜尋範圍
        for i in range(left, right + 1):
            bars[i].set_color('lightgreen')
        
        # 標記中間元素
        bars[mid].set_color('red')
        
        # 標記左右邊界
        bars[left].set_color('yellow')
        bars[right].set_color('yellow')
        
        # 設置圖表屬性
        ax.set_xlabel("索引")
        ax.set_ylabel("數值")
        ax.set_title("二分搜尋視覺化")
        
        # 設置 y 軸範圍
        ax.set_ylim(0, max(arr) * 1.2)
        
        # 在每個長條上方顯示數值
        for i, v in enumerate(arr):
            ax.text(i, v, str(v), ha='center', va='bottom')
            
        # 強制更新圖表
        plt.draw()
        plt.pause(0.8)  # 暫停 0.8 秒以便觀察

    def animate_search(self, arr: List[Any], ax: plt.Axes, search_history: List[Tuple[int, int, int]]):
        """動畫化二分搜尋過程
        
        Args:
            arr: 要視覺化的數列
            ax: matplotlib 座標軸物件
            search_history: 搜尋過程的歷史記錄
        """
        def update(frame):
            left, right, mid = search_history[frame]
            self.update_visualization(arr, ax, left, mid, right)
        
        ani = FuncAnimation(plt.gcf(), update, frames=len(search_history), repeat=False)
        plt.show()

class LinearSearch(SearchBase):
    """線性搜尋演算法實作"""
    
    def search(self, arr: List[Any], target: Any) -> Optional[int]:
        """執行線性搜尋"""
        logger.info(f"開始線性搜尋: 目標值 = {target}")
        
        # 取得視覺化物件 (如果有的話)
        ax = getattr(self, 'ax', None)
        
        for index, value in enumerate(arr):
            logger.debug(f"當前索引: {index}, 當前值: {value}")
            
            # 更新視覺化
            if ax:
                self.update_visualization(arr, ax, index)
            
            if value == target:
                logger.info(f"找到目標值於索引 {index}")
                return index
                
        logger.info("未找到目標值")
        return None
        
    def update_visualization(self, arr: List[Any], ax: plt.Axes, index: int):
        """更新線性搜尋視覺化"""
        ax.clear()
        bars = ax.bar(range(len(arr)), arr, color='lightblue')
        
        # 標記已搜尋過的元素
        for i in range(index):
            bars[i].set_color('gray')
        
        # 標記當前搜尋的元素
        bars[index].set_color('red')
        
        # 設置圖表屬性
        ax.set_xlabel("索引")
        ax.set_ylabel("數值")
        ax.set_title("線性搜尋視覺化")
        
        # 設置 y 軸範圍
        ax.set_ylim(0, max(arr) * 1.2)
        
        # 在每個長條上方顯示數值
        for i, v in enumerate(arr):
            ax.text(i, v, str(v), ha='center', va='bottom')
        
        # 強制更新圖表
        plt.draw()
        plt.pause(0.5)  # 暫停 0.5 秒以便觀察

class Searching(Algorithm):
    """搜尋演算法類別
    
    實作各種搜尋演算法並提供視覺化功能。
    
    Attributes:
        arr (List[Any]): 要搜尋的數列
        fig (Figure): matplotlib 圖形物件
        ax (Axes): matplotlib 座標軸物件
        search_history (List): 搜尋過程的歷史記錄
    """
    
    def __init__(self, arr: List[Any]):
        """初始化搜尋類別
        
        Args:
            arr: 要搜尋的數列
        """
        super().__init__()
        self.arr = arr.copy()
        # 使用內建的樣式
        plt.style.use('classic')  # 或使用 'default'
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.search_history = []
        self.algorithms = {}
        self.register_algorithm('binary', BinarySearch())
        self.register_algorithm('linear', LinearSearch())
        self.logger.info(f"初始化搜尋類別，數列長度: {len(arr)}")
        
    def register_algorithm(self, name: str, algorithm: SearchBase):
        """註冊搜尋演算法
        
        Args:
            name: 演算法名稱
            algorithm: 搜尋演算法實例
        """
        self.algorithms[name] = algorithm
        self.logger.info(f"註冊搜尋演算法: {name}")
        
    def search(self, target: Any, algorithm: str = 'binary') -> Optional[int]:
        """執行指定的搜尋演算法
        
        Args:
            target: 搜尋目標
            algorithm: 搜尋演算法名稱
            
        Returns:
            目標值的索引，若未找到則返回 None
            
        Raises:
            ValueError: 當指定的演算法不存在時
        """
        if algorithm not in self.algorithms:
            raise ValueError(f"不支援的演算法: {algorithm}")
            
        return self.algorithms[algorithm].search(self.arr, target)
        
    def visualize(self, target: Any, algorithm: str = "binary"):
        """視覺化搜尋過程"""
        self.logger.info(f"開始視覺化 {algorithm} 搜尋")
        
        # 重設圖表
        self.ax.clear()
        self.ax.set_title(f"{algorithm.capitalize()} Search Visualization")
        
        # 確保圖表可見
        plt.ion()
        plt.show()
        
        if algorithm in self.algorithms:
            # 設置視覺化物件
            self.algorithms[algorithm].ax = self.ax
            # 執行搜尋
            result = self.search(target, algorithm)
            
        plt.ioff()
        # 保持視窗顯示直到手動關閉
        plt.show(block=True)
        self.logger.info("搜尋視覺化完成")

__all__ = [
    "Searching"
]

