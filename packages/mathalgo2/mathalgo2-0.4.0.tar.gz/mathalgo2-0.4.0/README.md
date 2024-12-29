# MathAlgo2 數學演算法工具包

## 專案簡介
MathAlgo2 是一個全面的 Python 數學演算法與資料處理工具包，提供多樣化的演算法實現、視覺化功能、檔案處理工具以及數據分析功能。本工具包適合研究人員、數據分析師以及需要進行演算法分析和資料處理的開發者使用。

## 版本資訊
- 當前版本：0.4.0
- 發布日期：2024-12-28
- 更新日誌：
  - 0.4.0 (2024-12-28)
    - 基礎數學運算功能（矩陣運算、向量計算、複數運算）
    - 進階演算法功能（最佳化演算法、數值分析、統計分析工具）
    - 實用工具（資料視覺化、效能分析、錯誤處理機制）

## 核心功能

### 數學運算
- 微積分計算（定積分、極限、泰勒級數）
- 矩陣運算（加減乘、轉置、行列式）
- 向量空間運算
- 數學函數視覺化

### 資料結構
- 二元樹（插入、搜尋、序列化）
- 堆疊（LIFO）
- 佇列（FIFO）
- 鏈結串列
- 圖結構（含視覺化）

### 搜尋演算法
- 二分搜尋
- 線性搜尋
- 視覺化搜尋過程
- 效能分析工具

### 圖論演算法
- 深度優先搜尋 (DFS)
- 廣度優先搜尋 (BFS)
- Dijkstra 最短路徑
- 視覺化圖形演算法

### 加密與編碼
- 基礎編碼（ASCII、Base64、摩斯密碼）
- 古典密碼（凱薩密碼、柵欄密碼）
- 現代加密（RSA、AES、DES）
- 檔案加密功能

### 檔案處理工具
- 多格式檔案讀寫
- 檔案壓縮與解壓縮
- 檔案加密與解密
- 圖片處理功能
- 檔案備份管理

### 日誌系統
- 多級別日誌記錄
- 日誌檔案輪轉
- 自定義日誌格式
- 性能監控

## 使用範例

### 數學運算
```python
from mathalgo2.BaseMath import Calculus

# 創建計算器實例
calc = Calculus("x**2 + 2*x + 1")

# 計算定積分
result = calc.definite_integral(0, 1)
print(f"定積分結果: {result}")

# 繪製函數圖形
calc.plot(-5, 5)
```

### 資料結構
```python
from mathalgo2.Structure import Tree, Stack

# 創建二元樹
tree = Tree()
tree.insert(5)
tree.insert(3)
tree.insert(7)

# 使用堆疊
stack = Stack(max_size=10)
stack.push(1)
stack.push(2)
print(stack.pop())  # 輸出: 2
```

### 加密解密
```python
from mathalgo2.Code import ModernCipher

# AES 加密
cipher = ModernCipher()
encrypted, key = cipher.aes_encrypt("Hello, World!")
decrypted = cipher.aes_decrypt(encrypted, key)
```

## 環境需求
- Python 3.7+
- NumPy >= 1.19.0
- SciPy >= 1.6.0
- Pandas >= 1.2.0
- Matplotlib >= 3.3.0
- Seaborn >= 0.11.0
- SymPy >= 1.8
- Cryptography >= 3.4.0
- Pillow >= 8.0.0
- OpenCV >= 4.5.0

## 安裝

### 基本安裝
```bash
pip install mathalgo2
```

### 開發者安裝
```bash
pip install mathalgo2[dev]
```

### 文件開發安裝
```bash
pip install mathalgo2[docs]
```

## 文件
完整文件請參考 [專案文件](docs/)

## 參與貢獻
我們歡迎各種形式的貢獻：

1. Fork 本專案
2. 建立特性分支 (`git checkout -b feature/新功能`)
3. 提交變更 (`git commit -m '新增某功能'`)
4. 推送分支 (`git push origin feature/新功能`)
5. 提交 Pull Request

## 作者
- Donseking - [GitHub](https://github.com/Donseking)
- Email: 0717albert@gmail.com

## 授權條款
本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案

## 問題回報
如發現任何問題，請至 [Issues](https://github.com/Donseking/MathAlgo2/issues) 頁面回報 