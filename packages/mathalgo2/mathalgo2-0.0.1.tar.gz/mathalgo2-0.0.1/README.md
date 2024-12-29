# MathAlgo2 數學演算法工具包

## 專案簡介
MathAlgo2 是一個全面的 Python 數學演算法工具包，專注於提供多樣化的數學計算與演算法實現。本工具包適合研究人員、學生以及需要進行數學計算的開發者使用。

## 核心功能
### 基礎演算法
- 排序演算法（氣泡排序、快速排序、合併排序）
- 搜尋演算法（二分搜尋、線性搜尋）
- 效能分析工具

### 資料結構
- 二元樹實現
- 鏈結串列
- 佇列與堆疊

### 數學計算
- 符號與數值微分
- 定積分與不定積分
- 極限計算
- 泰勒級數展開

### 密碼學工具
- 摩斯密碼編解碼
- ASCII 編碼解碼
- 凱薩密碼加解密
- 柵欄密碼加解密

## 環境需求
- Python 3.7+
- NumPy >= 1.19.0
- SciPy >= 1.6.0
- Matplotlib >= 3.3.0
- SymPy >= 1.8

## 安裝方式

### 使用 pip 安裝
```bash
pip install mathalgo2
```

### 從原始碼安裝
```bash
git clone https://github.com/Donseking/MathAlgo2.git
cd MathAlgo2
python setup.py install
```

## 使用範例

### 基礎功能
```python
from mathalgo2.sort import quick_sort
from mathalgo2.Code import morse_code

# 排序範例
arr = [64, 34, 25, 12, 22, 11, 90]
sorted_arr = quick_sort(arr)

# 摩斯密碼轉換
text = "HELLO"
morse = morse_code.encode(text)
```

### 數學計算
```python
from mathalgo2.calculus import derivative, integral

# 計算導數
result = derivative('x^2', 'x')
# 計算積分
area = integral('x^2', 0, 1)
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

## 版本資訊
- v0.3.0
  - 實現基礎演算法
  - 數學計算功能
  - 整合基礎密碼學工具

## 作者
- Donseking - [GitHub](https://github.com/Donseking)
- Email: 0717albert@gmail.com

## 授權條款
本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案

## 問題回報
如發現任何問題，請至 [Issues](https://github.com/Donseking/MathAlgo2/issues) 頁面回報 