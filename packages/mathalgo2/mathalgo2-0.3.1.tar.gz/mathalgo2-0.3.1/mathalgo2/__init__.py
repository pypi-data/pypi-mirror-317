"""
# MathAlgo2 - 數學演算法工具包

這個模組包含了豐富的數學演算法實現，提供從基礎到進階的數學運算功能。

## 模組結構

mathalgo2/
├── __init__.py
├── sorting/              # 排序演算法
├── searching/           # 搜尋演算法
├── visualization/       # 演算法視覺化
├── data_structures/    # 資料結構
├── cryptography/       # 密碼學
├── calculus/           # 微積分
├── basic_math/         # 基本數學運算
├── advanced_math/      # 高級數學運算
├── matrix_operations/  # 矩陣運算
├── statistical_analysis/ # 統計分析
└── utils/              # 工具模組

## 功能概述

### 1. 基礎數學運算 (basic_math/)
- 基本的數學運算函數，如加法、減法、乘法和除法

### 2. 高級數學運算 (advanced_math/)
- 高級數學運算函數，如微積分和線性代數

### 3. 矩陣運算 (matrix_operations/)
- 矩陣運算函數，如矩陣乘法和轉置

### 4. 統計分析 (statistical_analysis/)
- 統計分析函數，如平均值、標準差和回歸分析

### 5. 排序演算法 (sorting/)
- bubble_sort: 氣泡排序
- quick_sort: 快速排序
- merge_sort: 合併排序
- heap_sort: 堆積排序

### 6. 搜尋演算法 (searching/)
- binary_search: 二分搜尋
- linear_search: 線性搜尋
- depth_first_search: 深度優先搜尋
- breadth_first_search: 廣度優先搜尋

### 7. 資料結構 (data_structures/)
- BinaryTree: 二元樹結構
- LinkedList: 鏈結串列
- Queue: 佇列結構
- Stack: 堆疊結構

### 8. 密碼學 (cryptography/)
- morse: 摩斯密碼編碼與解碼
- ascii: ASCII 編碼與解碼
- caesar: 凱薩密碼加密與解密
- rail_fence: 柵欄密碼加密與解密

### 9. 微積分模組 (calculus/)
- derivative: 符號微分與數值微分
- integral: 定積分與不定積分計算
- limit: 極限計算功能
- taylor_series: 泰勒級數展開
- plot: 函數圖形繪製

### 10. 工具模組 (utils/)
- file_handler: 檔案操作工具
- math_utils: 數學函數工具
- logger: 日誌記錄系統

## 使用方法

基本導入：
```python
from mathalgo2.sorting import quick_sort
from mathalgo2.searching import binary_search
from mathalgo2.basic_math import addition
from mathalgo2.matrix_operations import matrix_multiply
```

完整功能導入：
```python
import mathalgo2
```

詳細使用方法請參考各子模組的文檔。
"""

# 版本信息
__version__ = '1.0.0'
__author__ = 'Your Name'
__email__ = 'your.email@example.com'

from mathalgo2.algorithm.GraphAlgo import *
from mathalgo2.algorithm.SearchAlgo import *
from mathalgo2.algorithm.SortAlgo import *
from mathalgo2.algorithm.StrAlgo import *
from mathalgo2.algorithm.OpAlgo import *
from mathalgo2.Code import *
from mathalgo2.FileUtiles import *
from mathalgo2.logger import *
from mathalgo2.BaseMath import *
from mathalgo2.MathUtiles import *
from mathalgo2.Structure import *

__all__ = [
    "GraphAlgo",
    "Searching",
    "Sorting",
    "StrAlgo",
    "Optimization",
    "CodeBase",
    "ClassicalCipher",
    "FileUtils",
    "logger",
    "Calculus",
    "Matrix",
    "Vector_space",
    "MathUtils",
    "Tree",
    "TreeNode",
    "Stack",
    "Queue",
    "LinkedList",
    "LinkedListNode",
    "Graph"
]

