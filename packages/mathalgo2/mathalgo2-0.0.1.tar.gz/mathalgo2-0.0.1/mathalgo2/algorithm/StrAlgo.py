from typing import List
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mathalgo2.logger import setup_logger, logging
from pathlib import Path
from mathalgo2.algorithm.string.RabinKarp import RabinKarp
from mathalgo2.algorithm.string.KMP import KMP

# 設置根目錄和日誌
ROOT_DIR = Path(__file__).parent.parent.parent
log_file = ROOT_DIR / "__log__" / "StrAlgo.log"
logger = setup_logger("StrAlgo", log_file, level=logging.INFO)

class Algorithm(ABC):
    """演算法基礎抽象類別，提供所有字串演算法的共用介面和基本功能。"""
    
    def __init__(self):
        """初始化基礎類別"""
        self.logger = logger
        
    @abstractmethod
    def visualize(self, *args, **kwargs):
        """視覺化方法的抽象介面"""
        pass

class StrAlgo(Algorithm):
    """
    字串演算法類別，實現多種字串匹配算法並提供可視化功能。
    
    支援的字串演算法:
    - KMP (Knuth-Morris-Pratt)
    - Rabin-Karp
    - Trie (字典樹)
    - Suffix Array (後綴數組)
    
    Attributes:
        text (str): 待處理的文本
        pattern (str): 待匹配的模式
        fig (Figure): matplotlib 圖形對象
        ax (Axes): matplotlib 座標軸對象
        animation (FuncAnimation): matplotlib 動畫對象
    """
    
    def __init__(self, text: str, pattern: str):
        """
        初始化字串演算法類
        
        Args:
            text: 待處理的文本
            pattern: 待匹配的模式
        """
        super().__init__()
        self.text = text
        self.pattern = pattern
        self.fig, self.ax = plt.subplots()
        self.animation = None
        
        self.logger.info(f"初始化字串演算法類，文本長度: {len(text)}, 模式長度: {len(pattern)}")
        
    def kmp_search(self) -> List[int]:
        """KMP 字串匹配算法實現，返回匹配到的起始索引列表。"""
        self.logger.debug("開始 KMP 字串匹配")
        matches = KMP(self.pattern).search(self.text)
        self.logger.info(f"KMP 匹配完成，找到 {len(matches)} 個匹配")
        return matches
        
    def rabin_karp_search(self) -> List[int]:
        """Rabin-Karp 字串匹配算法實現，返回匹配到的起始索引列表。"""
        self.logger.debug("開始 Rabin-Karp 字串匹配")
        matches = RabinKarp(self.pattern).search(self.text)
        self.logger.info(f"Rabin-Karp 匹配完成，找到 {len(matches)} 個匹配")
        return matches
        
    def visualize(self, *args, **kwargs):
        """視覺化方法，傳遞給視覺化方法的位置參數和關鍵字參數。"""
        self.logger.debug("開始視覺化")
        self.ax.clear()
        self.ax.set_title("String Matching Visualization")
        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Match")
        
        matches = self.kmp_search()
        self.ax.plot(matches, [1] * len(matches), 'ro')
        
        self.animation = FuncAnimation(self.fig, self.update_visualization, frames=len(self.text), repeat=False)
        plt.show()
        self.logger.info("視覺化完成")
        
    def update_visualization(self, frame):
        """更新動畫視覺化，當前動畫幀。"""
        self.logger.debug(f"更新動畫視覺化，幀: {frame}")
        self.ax.set_title(f"Frame {frame}")

__all__ = [
    "StrAlgo"
]


