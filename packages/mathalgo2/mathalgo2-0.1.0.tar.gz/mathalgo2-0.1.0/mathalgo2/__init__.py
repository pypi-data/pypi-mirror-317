"""
# MathAlgo2 - 數學演算法工具包

## 功能特點

### 微積分模組
- 符號與數值微分
- 定積分與不定積分
- 極限計算
- 泰勒級數展開
- 函數繪圖

### 矩陣模組
- 基礎矩陣運算（加、減、乘）
- 矩陣轉置
- 行列式計算
- 逆矩陣運算

### 向量空間模組
- 向量運算
- 基底轉換
- 線性獨立檢驗

## 使用範例
```python
from mathalgo2.math import Calculus
f = Calculus("x**2")
derivative = f.derivative()
print(derivative)  # 輸出: 2*x
```

## 專案資訊
- 版本：0.1.0
- 作者：Donseking
- 授權：MIT
- 文件：https://github.com/Donseking/MathAlgo2
"""

from typing import Dict, List
import importlib.util

__version__ = "0.1.0"
__author__ = "Donseking"
__email__ = "0717albert@gmail.com"

# 導入主要類別
from mathalgo2.math import Calculus, Matrix, Vector_space

__all__ = [
    "Calculus",
    "Matrix",
    "Vector_space"
]

def _check_dependencies() -> None:
    """檢查必要的套件相依性
    
    檢查所有需要的套件是否已經安裝。
    
    Raises:
        ImportError: 當有套件未安裝時拋出錯誤
    """
    required_packages: Dict[str, str] = {
        "sympy": "用於符號計算",
        "numpy": "用於數值計算",
        "matplotlib": "用於繪圖功能"
    }
    
    missing_packages: List[str] = [
        f"{package} ({purpose})"
        for package, purpose in required_packages.items()
        if not importlib.util.find_spec(package)
    ]
    
    if missing_packages:
        packages_to_install = ' '.join(pkg.split()[0] for pkg in missing_packages)
        raise ImportError(
            "缺少必要的套件，請安裝：\n"
            f"{chr(10).join(f'- {pkg}' for pkg in missing_packages)}\n\n"
            f"可使用以下指令安裝：pip install {packages_to_install}"
        )

# 在導入時檢查相依性
_check_dependencies()