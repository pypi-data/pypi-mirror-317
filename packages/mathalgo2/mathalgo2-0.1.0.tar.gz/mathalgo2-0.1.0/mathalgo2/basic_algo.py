from typing import List, Union, Optional
import logging
from mathalgo2.logger import setup_logger
import os
from pathlib import Path

# 獲取當前文件所在目錄的根目錄
ROOT_DIR = Path(__file__).parent.parent

# 設置日誌文件路徑
log_file = os.path.join(ROOT_DIR, "__log__", "algorithm_basic.log")
logger = setup_logger("Algorithm_mode", log_file, level=logging.INFO)

class BasicAlgorithm:
    """
    # 基礎演算法類別
    
    提供各種基礎演算法的實現。
    
    ## 功能
    - 排序算法（氣泡、選擇、插入、快速排序等）
    - 搜尋算法（線性搜尋、二分搜尋）
    - 其他基礎算法
    """

    def _validate_input(arr: List[Union[int, float]]) -> None:
        """
        驗證輸入數組
        
        ## 參數
        - `arr`: 要驗證的數組
        
        ## 異常
        - ValueError: 當輸入無效時拋出
        """
        if arr is None:
            raise ValueError("輸入不能為 None")
        if not isinstance(arr, list):
            raise ValueError("輸入必須是列表類型")
        if not all(isinstance(x, (int, float)) for x in arr):
            raise ValueError("列表中的所有元素必須是數字類型")

    @staticmethod
    def bubble_sort(arr: List[Union[int, float]]) -> List[Union[int, float]]:
        """
        # 氣泡排序
        
        ## 參數
        - `arr`: 要排序的數列
        
        ## 返回
        - 排序後的數列
        """
        try:
            BasicAlgorithm._validate_input(arr)
            n = len(arr)
            arr = arr.copy()
            for i in range(n):
                for j in range(0, n-i-1):
                    if arr[j] > arr[j+1]:
                        arr[j], arr[j+1] = arr[j+1], arr[j]
            logger.info("氣泡排序完成")
            return arr
        except Exception as e:
            logger.error(f"氣泡排序失敗: {str(e)}")
            raise ValueError(str(e))

    @staticmethod
    def quick_sort(arr: List[Union[int, float]]) -> List[Union[int, float]]:
        """
        # 快速排序
        
        ## 參數
        - `arr`: 要排序的數列
        
        ## 返回
        - 排序後的數列
        """
        try:
            BasicAlgorithm._validate_input(arr)
            arr = arr.copy()
            
            def _quick_sort(arr: List[Union[int, float]], low: int, high: int) -> None:
                if low < high:
                    pivot_idx = _partition(arr, low, high)
                    _quick_sort(arr, low, pivot_idx - 1)
                    _quick_sort(arr, pivot_idx + 1, high)

            def _partition(arr: List[Union[int, float]], low: int, high: int) -> int:
                pivot = arr[high]
                i = low - 1
                for j in range(low, high):
                    if arr[j] <= pivot:
                        i += 1
                        arr[i], arr[j] = arr[j], arr[i]
                arr[i + 1], arr[high] = arr[high], arr[i + 1]
                return i + 1

            _quick_sort(arr, 0, len(arr) - 1)
            logger.info("快速排序完成")
            return arr
        except Exception as e:
            logger.error(f"快速排序失敗: {str(e)}")
            raise ValueError(str(e))

    @staticmethod
    def binary_search(arr: List[Union[int, float]], target: Union[int, float]) -> Optional[int]:
        """
        # 二分搜尋
        
        ## 參數
        - `arr`: 已排序的數列
        - `target`: 搜尋目標
        
        ## 返回
        - 目標索引，若未找到則返回 None
        """
        try:
            left, right = 0, len(arr) - 1
            while left <= right:
                mid = (left + right) // 2
                if arr[mid] == target:
                    logger.info(f"找到目標值於索引 {mid}")
                    return mid
                elif arr[mid] < target:
                    left = mid + 1
                else:
                    right = mid - 1
            logger.info("未找到目標值")
            return None
        except Exception as e:
            logger.error(f"二分搜尋失敗: {str(e)}")
            raise ValueError("搜尋錯誤")

    @staticmethod
    def linear_search(arr: List[Union[int, float]], target: Union[int, float]) -> Optional[int]:
        """
        # 線性搜尋
        
        ## 參數
        - `arr`: 數列
        - `target`: 搜尋目標
        
        ## 返回
        - 目標索引，若未找到則返回 None
        """
        try:
            for i, value in enumerate(arr):
                if value == target:
                    logger.info(f"找到目標值於索引 {i}")
                    return i
            logger.info("未找到目標值")
            return None
        except Exception as e:
            logger.error(f"線性搜尋失敗: {str(e)}")
            raise ValueError("搜尋錯誤")

    @staticmethod
    def merge_sort(arr: List[Union[int, float]]) -> List[Union[int, float]]:
        """
        # 合併排序
        
        ## 參數
        - `arr`: 要排序的數列
        
        ## 返回
        - 排序後的數列
        """
        def _merge(left: List[Union[int, float]], right: List[Union[int, float]]) -> List[Union[int, float]]:
            result = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            result.extend(left[i:])
            result.extend(right[j:])
            return result

        try:
            if len(arr) <= 1:
                return arr.copy()
            
            mid = len(arr) // 2
            left = BasicAlgorithm.merge_sort(arr[:mid])
            right = BasicAlgorithm.merge_sort(arr[mid:])
            
            result = _merge(left, right)
            logger.info("合併排序完成")
            return result
        except Exception as e:
            logger.error(f"合併排序失敗: {str(e)}")
            raise ValueError("排序錯誤")
