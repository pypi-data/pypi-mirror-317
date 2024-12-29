"""
# MathAlgo2 - 數學演算法工具包

這個模組包含了豐富的數學演算法實現，提供從基礎到進階的數學運算功能。

## 模組結構

mathalgo2/
├── __init__.py
├── algorithm/          # 演算法相關
│   ├── GraphAlgo.py   # 圖論演算法
│   ├── SearchAlgo.py  # 搜尋演算法
│   ├── SortAlgo.py    # 排序演算法
│   ├── StrAlgo.py     # 字串演算法
│   ├── OpAlgo.py      # 最佳化演算法
│   └── StrucAlgo.py   # 結構演算法
├── Code.py            # 編碼相關
├── FileUtiles.py      # 檔案處理工具
├── logger.py          # 日誌系統
├── BaseMath.py        # 基礎數學
├── MathUtiles.py      # 數學工具
└── Structure.py       # 資料結構

## 主要功能模組

### 1. 檔案處理 (FileUtiles.py)
- FileIO: 檔案輸入輸出基本操作
- FileProcessor: 進階檔案處理（壓縮、加密、圖片處理）
- DataAnalyzer: 數據分析與視覺化

### 2. 演算法 (algorithm/)
- 圖論演算法
- 搜尋演算法
- 排序演算法
- 字串演算法
- 最佳化演算法
- 結構演算法

### 3. 數學工具
- 基礎數學運算
- 進階數學功能
- 矩陣運算
- 向量空間運算

### 4. 資料結構
- 樹結構
- 堆疊與佇列
- 鏈結串列
- 圖結構
- 二元樹
- AVL樹
- 並查集
- 堆積

## 使用方法

基本導入：
```python
from mathalgo2.FileUtiles import FileIO, FileProcessor, DataAnalyzer
from mathalgo2.algorithm import SearchAlgo, SortAlgo
```

完整功能導入：
```python
import mathalgo2
```
"""

# 版本信息
__version__ = '1.0.0'
__author__ = 'Donseking'
__email__ = '0717albert@gmail.com'

# 從各模組導入
from mathalgo2.algorithm.GraphAlgo import *
from mathalgo2.algorithm.SearchAlgo import *
from mathalgo2.algorithm.SortAlgo import *
from mathalgo2.algorithm.StrAlgo import *
from mathalgo2.algorithm.OpAlgo import *
from mathalgo2.algorithm.StrucAlgo import *
from mathalgo2.Code import *
from mathalgo2.FileUtiles import *
from mathalgo2.Logger import *
from mathalgo2.BaseMath import *
from mathalgo2.MathUtiles import *
from mathalgo2.Structure import *

__all__ = [
    # 檔案處理
    "FileIO",
    "FileProcessor",
    "DataAnalyzer",
    
    # 演算法
    "GraphAlgo",
    "Searching",
    "Sorting",
    "StrAlgo",
    "Optimization",
    
    # 編碼
    "CodeBase",
    "ClassicalCipher",
    "ModernCipher"
    
    # 日誌
    "Logger",
    
    # 數學
    "Calculus",
    "Matrix",
    "Vector_space",
    "MathUtils",
    
    # 資料結構
    "Tree",
    "TreeNode",
    "Stack",
    "Queue",
    "LinkedList",
    "LinkedListNode",
    "Graph",
    "BinaryTree",
    "AVLTree",
    "UnionFind",
    "Heap",
    "DataStructureFactory"
]

