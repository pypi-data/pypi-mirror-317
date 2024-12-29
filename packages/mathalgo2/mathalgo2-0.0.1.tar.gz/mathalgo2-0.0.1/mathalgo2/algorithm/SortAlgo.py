from typing import List, Dict, Any, Optional, Tuple, Union, Callable
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from mathalgo2.logger import setup_logger, logging
import os
from pathlib import Path

# 設置根目錄和日誌
ROOT_DIR = Path(__file__).parent.parent.parent
log_file = ROOT_DIR / "__log__" / "SortAlgo.log"
logger = setup_logger("SortAlgo", log_file, level=logging.INFO)

class Algorithm(ABC):
    """演算法基礎類別，提供共用功能和介面"""
    
    def __init__(self):
        """初始化基礎類別，設置日誌記錄器"""
        self.logger = logger
        
    @abstractmethod
    def visualize(self, *args, **kwargs):
        """
        視覺化方法的抽象介面
        
        所有繼承的演算法類別都必須實現此方法
        """
        pass

class Sorting(Algorithm):
    """
    排序演算法類別，實現多種排序算法並提供可視化功能
    
    支援的排序算法:
    - 氣泡排序 (Bubble Sort)
    - 快速排序 (Quick Sort)
    - 插入排序 (Insertion Sort)
    - 合併排序 (Merge Sort)
    
    Attributes:
        arr (List[Any]): 待排序的數組
        fig (Figure): matplotlib 圖形對象
        ax (Axes): matplotlib 座標軸對象
        animation_speed (float): 動畫速度控制參數
        colors (Dict[str, str]): 視覺化顏色配置
    """
    
    def __init__(self, arr: List[Any], animation_speed: float = 0.1):
        """
        初始化排序類
        
        Args:
            arr: 待排序的數組
            animation_speed: 視覺化動畫速度，默認0.1秒
        """
        super().__init__()
        self.arr = arr.copy()  # 複製輸入數組以避免修改原數組
        self.fig = None  # matplotlib圖形對象
        self.ax = None   # matplotlib座標軸對象
        self.animation_speed = animation_speed
        
        # 視覺化顏色配置
        self.colors = {
            'default': 'skyblue',
            'highlight': 'red',
            'sorted': 'green'
        }
        
        self.logger.info(f"初始化排序類，數組長度: {len(arr)}")
        
    def bubble_sort(self, reverse: bool = False) -> List[Any]:
        """
        氣泡排序算法實現
        
        原理: 重複遍歷待排序數組，比較相鄰元素並交換順序
        時間複雜度: O(n²) - 需要進行n輪比較，每輪比較n-i-1次
        空間複雜度: O(1) - 只需要常數級額外空間
        穩定性: 穩定 - 相等元素的相對位置不會改變
        
        Args:
            reverse: 是否降序排序，默認為False(升序)
            
        Returns:
            排序後的數組
        """
        self.logger.info(f"開始氣泡排序，排序方向: {'降序' if reverse else '升序'}")
        n = len(self.arr)
        
        if self.fig is not None:  # 啟用可視化
            plt.ion()  # 開啟交互模式
            self.logger.debug("啟用排序可視化")
            
        for i in range(n):
            self.logger.debug(f"開始第{i+1}輪排序")
            swapped = False  # 優化標記：如果一輪中沒有交換，則數組已排序
            
            for j in range(0, n-i-1):
                # 根據排序方向決定比較邏輯
                if (self.arr[j] > self.arr[j+1]) != reverse:
                    # 交換元素
                    self.arr[j], self.arr[j+1] = self.arr[j+1], self.arr[j]
                    swapped = True
                    
                    # 更新視覺化
                    if self.fig is not None:
                        self._update_plot(
                            highlight_indices=[j, j+1],
                            sorted_indices=list(range(n-i, n)),
                            status=f"比較位置 {j} 和 {j+1}"
                        )
            
            if not swapped:  # 如果沒有發生交換，提前結束
                self.logger.debug(f"數組在第{i+1}輪後已排序完成")
                break
                        
        self.logger.info("氣泡排序完成")
        return self.arr
    
    def quick_sort(self, reverse: bool = False) -> List[Any]:
        """
        快速排序算法實現
        
        原理: 選擇基準值(pivot)，將數組分為小於和大於基準值的兩部分，遞歸排序
        時間複雜度: 平均O(nlogn)，最壞O(n²)
        空間複雜度: O(logn) - 遞歸調用棧的深度
        穩定性: 不穩定
        
        Args:
            reverse: 是否降序排序，默認為False(升序)
            
        Returns:
            排序後的數組
        """
        self.logger.info(f"開始快速排序，排序方向: {'降序' if reverse else '升序'}")
        if self.fig is not None:
            plt.ion()
        self._quick_sort_helper(0, len(self.arr)-1, reverse)
        self.logger.info("快速排序完成")
        return self.arr
        
    def _quick_sort_helper(self, low: int, high: int, reverse: bool):
        """
        快速排序的遞歸輔助方法
        
        Args:
            low: 子數組的起始索引
            high: 子數組的結束索引
            reverse: 排序方向
        """
        if low < high:
            self.logger.debug(f"處理子數組 [{low}, {high}]")
            pivot = self._partition(low, high, reverse)
            self._quick_sort_helper(low, pivot-1, reverse)
            self._quick_sort_helper(pivot+1, high, reverse)
            
    def _partition(self, low: int, high: int, reverse: bool) -> int:
        """
        快速排序的分區方法
        
        Args:
            low: 子數組的起始索引
            high: 子數組的結束索引
            reverse: 排序方向
            
        Returns:
            基準值的最終位置
        """
        pivot = self.arr[high]  # 選擇最後一個元素作為基準值
        i = low - 1  # 小於基準值的元素的最後位置
        
        for j in range(low, high):
            # 根據排序方向決定比較邏輯
            if (self.arr[j] <= pivot) != reverse:
                i += 1
                self.arr[i], self.arr[j] = self.arr[j], self.arr[i]
                
                # 更新視覺化
                if self.fig is not None:
                    self._update_plot(
                        highlight_indices=[i, j, high],
                        status=f"Partitioning: pivot={pivot}"
                    )
        
        # 將基準值放到正確的位置
        self.arr[i + 1], self.arr[high] = self.arr[high], self.arr[i + 1]
        
        # 最後一次視覺化更新
        if self.fig is not None:
            self._update_plot(
                highlight_indices=[i + 1],
                status=f"Placed pivot={pivot}"
            )
        
        return i + 1
    
    def insertion_sort(self, reverse: bool = False) -> List[Any]:
        """
        插入排序算法實現
        
        原理: 將數組分為已排序和未排序兩部分，逐個將未排序元素插入到已排序部分的正確位置
        時間複雜度: O(n²) - 需要進行n輪插入，每輪最多比較n次
        空間複雜度: O(1) - 只需要常數級額外空間
        穩定性: 穩定 - 相等元素的相對位置不會改變
        
        Args:
            reverse: 是否降序排序，默認為False(升序)
            
        Returns:
            排序後的數組
        """
        self.logger.info(f"開始插入排序，排序方向: {'降序' if reverse else '升序'}")
        n = len(self.arr)
        
        if self.fig is not None:  # 啟用可視化
            plt.ion()  # 開啟交互模式
            self.logger.debug("啟用排序可視化")
        
        for i in range(1, n):
            key = self.arr[i]
            j = i - 1
            
            # 根據排序方向決定比較邏輯
            while j >= 0 and (self.arr[j] > key) != reverse:
                self.arr[j + 1] = self.arr[j]
                j -= 1
                
                # 更新視覺化
                if self.fig is not None:
                    self._update_plot(
                        highlight_indices=[j + 1, j + 2],
                        sorted_indices=list(range(i + 1)),
                        status=f"插入位置 {j + 1}"
                    )
            
            self.arr[j + 1] = key
            
            # 最後一次視覺化更新
            if self.fig is not None:
                self._update_plot(
                    highlight_indices=[j + 1],
                    sorted_indices=list(range(i + 1)),
                    status=f"插入位置 {j + 1}"
                )
        
        self.logger.info("插入排序完成")
        return self.arr
    
    def merge_sort(self, reverse: bool = False) -> List[Any]:
        """
        合併排序算法實現
        
        原理: 將數組分成兩部分，遞歸排序每部分，然後合併已排序的部分
        時間複雜度: O(nlogn)
        空間複雜度: O(n) - 需要額外的數組來合併
        穩定性: 穩定
        
        Args:
            reverse: 是否降序排序，默認為False(升序)
            
        Returns:
            排序後的數組
        """
        self.logger.info(f"開始合併排序，排序方向: {'降序' if reverse else '升序'}")
        if self.fig is not None:
            plt.ion()
        self.arr = self._merge_sort_helper(self.arr, reverse)
        self.logger.info("合併排序完成")
        return self.arr
    
    def _merge_sort_helper(self, arr: List[Any], reverse: bool) -> List[Any]:
        """
        合併排序的遞歸輔助方法
        
        Args:
            arr: 待排序的數組
            reverse: 排序方向
            
        Returns:
            排序後的數組
        """
        if len(arr) > 1:
            mid = len(arr) // 2
            left_half = arr[:mid]
            right_half = arr[mid:]
            
            self.logger.debug(f"分割數組: 左半部分 {left_half}, 右半部分 {right_half}")
            
            left_sorted = self._merge_sort_helper(left_half, reverse)
            right_sorted = self._merge_sort_helper(right_half, reverse)
            
            merged = self._merge(left_sorted, right_sorted, reverse)
            
            # 更新視覺化
            if self.fig is not None:
                self._update_plot(
                    highlight_indices=[],
                    status=f"合併: {merged}"
                )
            
            return merged
        else:
            return arr
    
    def _merge(self, left: List[Any], right: List[Any], reverse: bool) -> List[Any]:
        """
        合併兩個已排序數組
        
        Args:
            left: 左半部分已排序數組
            right: 右半部分已排序數組
            reverse: 排序方向
            
        Returns:
            合併後的已排序數組
        """
        merged = []
        while left and right:
            if (left[0] <= right[0]) != reverse:
                merged.append(left.pop(0))
            else:
                merged.append(right.pop(0))
        
        merged.extend(left or right)
        return merged
    
    def visualize(self, algorithm: str = "bubble", reverse: bool = False):
        """
        視覺化排序過程
        
        Args:
            algorithm: 排序算法名稱 ("bubble", "quick", "insertion" 或 "merge")
            reverse: 是否降序排序
        """
        self.logger.info(f"開始{algorithm}排序可視化")
        
        # 設置視覺化窗口
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.ax.set_title(f"{algorithm.capitalize()} Sort Visualization")
        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Value")
        
        # 執行指定的排序算法
        if algorithm == "bubble":
            self.bubble_sort(reverse)
        elif algorithm == "quick":
            self.quick_sort(reverse)
        elif algorithm == "insertion":
            self.insertion_sort(reverse)
        elif algorithm == "merge":
            self.merge_sort(reverse)
        else:
            self.logger.error(f"不支持的算法: {algorithm}")
            return
            
        plt.ioff()
        plt.show()
        self.logger.info("排序可視化完成")
        
    def _update_plot(self, highlight_indices: List[int], sorted_indices: List[int] = None, status: str = ""):
        """
        更新排序可視化圖形
        
        Args:
            highlight_indices: 需要高亮顯示的元素索引
            sorted_indices: 已排序的元素索引
            status: 當前操作的狀態描述
        """
        self.ax.clear()
        bars = self.ax.bar(range(len(self.arr)), self.arr, color=self.colors['default'])
        
        # 高亮顯示正在比較的元素
        for idx in highlight_indices:
            bars[idx].set_color(self.colors['highlight'])
            
        # 標記已排序的元素
        if sorted_indices:
            for idx in sorted_indices:
                if 0 <= idx < len(bars):
                    bars[idx].set_color(self.colors['sorted'])
            
        if status:
            self.ax.set_title(f"Sorting Progress - {status}")
            
        # 設置適當的坐標軸範圍
        self.ax.set_ylim(0, max(self.arr) * 1.1)
        
        # 控制動畫速度
        plt.pause(self.animation_speed)
        
    def animate(self, algorithm: str = "bubble", reverse: bool = False):
        """
        動畫化排序過程
        
        Args:
            algorithm: 排序算法名稱 ("bubble", "quick", "insertion" 或 "merge")
            reverse: 是否降序排序
        """
        self.logger.info(f"開始{algorithm}排序動畫化")
        
        # 設置動畫窗口
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.ax.set_title(f"{algorithm.capitalize()} Sort Animation")
        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Value")
        
        # 初始化動畫數據
        self.bars = self.ax.bar(range(len(self.arr)), self.arr, color=self.colors['default'])
        
        # 選擇排序算法
        if algorithm == "bubble":
            self.anim = FuncAnimation(self.fig, self._bubble_sort_animation, frames=len(self.arr), repeat=False)
        elif algorithm == "quick":
            self.anim = FuncAnimation(self.fig, self._quick_sort_animation, frames=len(self.arr), repeat=False)
        elif algorithm == "insertion":
            self.anim = FuncAnimation(self.fig, self._insertion_sort_animation, frames=len(self.arr), repeat=False)
        elif algorithm == "merge":
            self.anim = FuncAnimation(self.fig, self._merge_sort_animation, frames=len(self.arr), repeat=False)
        else:
            self.logger.error(f"不支持的算法: {algorithm}")
            return
        
        plt.show()
        self.logger.info("排序動畫化完成")
        
    def _bubble_sort_animation(self, frame):
        """
        氣泡排序動畫幀更新
        
        Args:
            frame: 當前幀索引
        """
        n = len(self.arr)
        for i in range(n):
            swapped = False
            for j in range(0, n-i-1):
                if self.arr[j] > self.arr[j+1]:
                    self.arr[j], self.arr[j+1] = self.arr[j+1], self.arr[j]
                    swapped = True
                    self._update_bars([j, j+1])
            if not swapped:
                break
    
    def _quick_sort_animation(self, frame):
        """
        快速排序動畫幀更新
        
        Args:
            frame: 當前幀索引
        """
        self._quick_sort_helper(0, len(self.arr)-1, False)
    
    def _insertion_sort_animation(self, frame):
        """
        插入排序動畫幀更新
        
        Args:
            frame: 當前幀索引
        """
        n = len(self.arr)
        for i in range(1, n):
            key = self.arr[i]
            j = i - 1
            while j >= 0 and self.arr[j] > key:
                self.arr[j + 1] = self.arr[j]
                j -= 1
                self._update_bars([j + 1, j + 2])
            self.arr[j + 1] = key
    
    def _merge_sort_animation(self, frame):
        """
        合併排序動畫幀更新
        
        Args:
            frame: 當前幀索引
        """
        self.arr = self._merge_sort_helper(self.arr, False)
    
    def _update_bars(self, highlight_indices: List[int]):
        """
        更新動畫條形圖
        
        Args:
            highlight_indices: 需要高亮顯示的元素索引
        """
        for idx, bar in enumerate(self.bars):
            bar.set_height(self.arr[idx])
            bar.set_color(self.colors['default'])
        for idx in highlight_indices:
            self.bars[idx].set_color(self.colors['highlight'])

__all__ = [
    "Sorting"
]

