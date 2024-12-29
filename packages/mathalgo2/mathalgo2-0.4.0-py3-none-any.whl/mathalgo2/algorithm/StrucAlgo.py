from typing import List, Optional, Any, TypeVar, Generic
from abc import ABC, abstractmethod
from mathalgo2.Logger import Logger, logging
from pathlib import Path
import graphviz
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
from typing import Dict, List, Tuple
import tempfile

# 設置根目錄和日誌
ROOT_DIR = Path(__file__).parent.parent.parent
log_file = ROOT_DIR / "__log__" / "StrucAlgo.log"

# 初始化日誌管理器
logger_manager = Logger(
    name="StrucAlgo",
    log_file=str(log_file),
    level=logging.INFO
)

T = TypeVar('T')

class BaseAlgo:
    def __init__(self):
        """初始化基礎演算法類"""
        self.logger = logger_manager
        
        # 移除舊的日誌處理器設置，因為現在使用統一的 logger_manager
        # if not self.logger.handlers:
        #     handler = logging.StreamHandler()
        #     formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        #     handler.setFormatter(formatter)
        #     self.logger.addHandler(handler)

class BaseTree(BaseAlgo, Generic[T]):
    """樹結構的抽象基類
    
    提供樹結構的基本框架，包含:
    - 節點管理
    - 基本樹操作
    
    Attributes:
        root: 樹的根節點
        logger: 日誌記錄器
    """
    
    class Node:
        def __init__(self, val: T):
            self.val = val
            self.left = None
            self.right = None
    
    def __init__(self, test_mode: bool = False):
        """初始化基礎樹類
        
        Args:
            test_mode: 是否為測試模式
        """
        super().__init__()  # 先初始化 BaseAlgo，設置 logger
        self.root = None
        self.operation_history = []
        self.test_mode = test_mode  # 保存測試模式狀態
        
        if not test_mode:
            try:
                self.fig, self.ax = plt.subplots()
            except Exception as e:
                self.logger.warning(f"無法創建圖形界面: {e}")
                self.fig = None
                self.ax = None
        else:
            self.fig = None
            self.ax = None
        
        self.animation = None
        self.logger.info(f"初始化{self.__class__.__name__}")

    def visualize(self, filename: str = "tree"):
        """生成樹的靜態可視化圖
        
        Args:
            filename: 輸出文件名（需要包含 .png 副檔名）
        """
        G = nx.Graph()
        pos = {}
        
        def add_to_graph(node: Optional[BaseTree.Node], x: float = 0, y: float = 0, layer: int = 0):
            if node:
                G.add_node(str(id(node)), value=str(node.val))
                pos[str(id(node))] = (x, -y)
                
                if node.left:
                    G.add_edge(str(id(node)), str(id(node.left)))
                    add_to_graph(node.left, x-1/(2**layer), y+1, layer+1)
                
                if node.right:
                    G.add_edge(str(id(node)), str(id(node.right)))
                    add_to_graph(node.right, x+1/(2**layer), y+1, layer+1)
        
        add_to_graph(self.root)
        
        plt.figure(figsize=(10, 8))
        nx.draw(G, pos,
               with_labels=True,
               node_color='lightblue',
               node_size=1000,
               labels={node: G.nodes[node]['value'] for node in G.nodes()})
        
        plt.savefig(filename)
        plt.close()
        self.logger.info(f"生成樹的可視化圖: {filename}")

    def create_animation(self, operations: List[Tuple[str, Any]], filename: str = "tree_animation.gif"):
        """創建樹操作的動畫
        
        Args:
            operations: 操作列表，每個元素為 (操作類型, 值) 的元組
            filename: 輸出的動畫文件名
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        frames = []
        
        def update(frame):
            ax.clear()
            G = nx.Graph()
            pos = {}
            
            def add_to_graph(node: Optional[BaseTree.Node], x: float = 0, y: float = 0, layer: int = 0):
                if node:
                    G.add_node(str(id(node)), value=str(node.val))
                    pos[str(id(node))] = (x, -y)
                    
                    if node.left:
                        G.add_edge(str(id(node)), str(id(node.left)))
                        add_to_graph(node.left, x-1/(2**layer), y+1, layer+1)
                    
                    if node.right:
                        G.add_edge(str(id(node)), str(id(node.right)))
                        add_to_graph(node.right, x+1/(2**layer), y+1, layer+1)
            
            add_to_graph(self.root)
            nx.draw(G, pos, ax=ax, with_labels=True, 
                   node_color='lightblue', 
                   node_size=1000,
                   labels={node: G.nodes[node]['value'] for node in G.nodes()})
            
            ax.set_title(f'Operation: {operations[frame][0]} {operations[frame][1]}')
            return ax,
        
        for op, value in operations:
            if op == "insert":
                self.insert(value)
            elif op == "delete":
                self.delete(value)
            frames.append((op, value))
        
        ani = animation.FuncAnimation(fig, update, frames=len(operations),
                                    interval=1000, blit=True)
        ani.save(filename, writer='pillow')
        plt.close()
        self.logger.info(f"生成樹操作的動畫: {filename}")

class BinaryTree(BaseTree):
    """二元樹實現
    
    提供插入、搜尋和刪除節點的功能，並記錄詳細的日誌。
    """
    
    def __init__(self, test_mode: bool = False):
        """初始化二元樹
        
        Args:
            test_mode: 是否為測試模式
        """
        super().__init__(test_mode)  # 傳遞 test_mode 參數給父類
        self.root = None
        self.operation_history = []  # 添加操作歷史記錄
        
        if not test_mode:
            self.fig, self.ax = plt.subplots()
            self.animation = None
        else:
            self.fig = None
            self.ax = None
            self.animation = None
            
        self.logger.info("初始化二元樹")
    
    def insert(self, value: T):
        """插入新節點
        
        將新節點插入到二元樹中，並記錄插入過程的日誌。
        
        Args:
            value: 要插入的節點值
        """
        self.operation_history.append(("insert", value))
        if self.root is None:
            self.root = self.Node(value)
            self.logger.info(f"插入根節點: {value}")
        else:
            self.logger.info(f"開始插入節點: {value}")
            self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node: BaseTree.Node, value: T):
        """遞歸插入新節點
        
        在樹中找到適當的位置插入新節點，並記錄每一步的日誌。
        
        Args:
            node: 當前節點
            value: 要插入的節點值
        """
        if value < node.val:
            if node.left is None:
                node.left = self.Node(value)
                self.logger.info(f"插入左子節點: {value}")
            else:
                self.logger.info(f"移動到左子節點: {node.left.val}")
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = self.Node(value)
                self.logger.info(f"插入右子節點: {value}")
            else:
                self.logger.info(f"移動到右子節點: {node.right.val}")
                self._insert_recursive(node.right, value)
    
    def search(self, val) -> bool:
        """搜尋節點
        
        Args:
            val: 要搜尋的值
            
        Returns:
            bool: 是否找到該值
        """
        self.logger.info(f"開始搜尋節點: {val}")
        result = self._search(self.root, val)
        if result:
            self.logger.info(f"找到節點: {val}")
        else:
            self.logger.info(f"未找到節點: {val}")
        return result is not None
        
    def _search(self, node, val):
        if not node or node.val == val:
            return node
        if val < node.val:
            return self._search(node.left, val)
        return self._search(node.right, val)
        
    def delete(self, value: T):
        """刪除節點
        
        從二元樹中刪除指定值的節點，並記錄刪除過程的日誌。
        
        Args:
            value: 要刪除的節點值
        """
        self.operation_history.append(("delete", value))
        self.logger.info(f"開始刪除節點: {value}")
        self.root = self._delete_recursive(self.root, value)
    
    def _delete_recursive(self, node: Optional[BaseTree.Node], value: T) -> Optional[BaseTree.Node]:
        """遞歸刪除節點
        
        在樹中遞歸刪除指定值的節點，並記錄每一步的日誌。
        
        Args:
            node: 當前節點
            value: 要刪除的節點值
            
        Returns:
            Optional[BaseTree.Node]: 刪除後的子樹根節點
        """
        if node is None:
            self.logger.info(f"節點 {value} 不存在")
            return None
        
        if value < node.val:
            self.logger.info(f"移動到左子節點: {node.left.val if node.left else 'None'}")
            node.left = self._delete_recursive(node.left, value)
        elif value > node.val:
            self.logger.info(f"移動到右子節點: {node.right.val if node.right else 'None'}")
            node.right = self._delete_recursive(node.right, value)
        else:
            self.logger.info(f"找到節點 {value}，準備刪除")
            if node.left is None:
                self.logger.info(f"刪除節點 {value}，無左子節點")
                return node.right
            elif node.right is None:
                self.logger.info(f"刪除節點 {value}，無右子節點")
                return node.left
            
            min_larger_node = self._get_min(node.right)
            self.logger.info(f"替換節點 {value} 為 {min_larger_node.val}")
            node.val = min_larger_node.val
            node.right = self._delete_recursive(node.right, min_larger_node.val)
        
        return node
    
    def _get_min(self, node: BaseTree.Node) -> BaseTree.Node:
        """獲取最小值節點
        
        在樹中找到最小值的節點，並記錄過程的日誌。
        
        Args:
            node: 當前節點
            
        Returns:
            BaseTree.Node: 最小值節點
        """
        current = node
        while current.left is not None:
            self.logger.info(f"移動到左子節點: {current.left.val}")
            current = current.left
        self.logger.info(f"最小值節點為: {current.val}")
        return current

    def animate(self):
        """動畫展示"""
        if self.test_mode:
            return
        # 實際的動畫邏輯...
        self.logger.info("執行動畫展示")

class AVLNode(BaseTree.Node):
    def __init__(self, value: T):
        super().__init__(value)
        self.height = 1
        self.value = value  # 添加 value 屬性，保持與 val 同步
        self.val = value    # 保持與父類一致

class AVLTree(BaseTree[T]):
    """AVL樹實現
    
    提供插入、刪除和搜尋節點的功能，並保持樹的平衡。
    """
    
    def __init__(self, test_mode: bool = False):
        """初始化AVL樹
        
        Args:
            test_mode: 是否為測試模式
        """
        super().__init__(test_mode)  # 傳遞 test_mode 參數給父類
        self.Node = AVLNode  # 使用 AVLNode 替代基礎 Node
        self.root = None
        self.operation_history = []  # 添加操作歷史記錄
        
        if not test_mode:
            self.fig, self.ax = plt.subplots()
            self.animation = None
        else:
            self.fig = None
            self.ax = None
            self.animation = None
            
        self.logger.info("初始化AVL樹")
    
    def _get_height(self, node: Optional[BaseTree.Node]) -> int:
        """獲取節點高度"""
        if not node:
            return 0
        return node.height
    
    def _update_height(self, node: BaseTree.Node):
        """更新節點高度"""
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        self.logger.info(f"更新節點 {node.val} 的高度為 {node.height}")
    
    def _get_balance(self, node: BaseTree.Node) -> int:
        """獲取節點平衡因子"""
        if not node:
            return 0
        balance = self._get_height(node.left) - self._get_height(node.right)
        self.logger.info(f"節點 {node.val} 的平衡因子為 {balance}")
        return balance
    
    def _rotate_left(self, z: BaseTree.Node) -> BaseTree.Node:
        """左旋轉"""
        self.logger.info(f"左旋轉節點 {z.val}")
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        self._update_height(z)
        self._update_height(y)
        return y
    
    def _rotate_right(self, z: BaseTree.Node) -> BaseTree.Node:
        """右旋轉"""
        self.logger.info(f"右旋轉節點 {z.val}")
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        self._update_height(z)
        self._update_height(y)
        return y
    
    def insert(self, value: T):
        """插入新節點"""
        self.logger.info(f"開始插入節點: {value}")
        self.root = self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node: Optional[BaseTree.Node], value: T) -> BaseTree.Node:
        """遞歸插入新節點"""
        if not node:
            self.logger.info(f"插入新節點: {value}")
            return self.Node(value)
        
        if value < node.val:
            self.logger.info(f"移動到左子節點: {node.left.val if node.left else 'None'}")
            node.left = self._insert_recursive(node.left, value)
        else:
            self.logger.info(f"移動到右子節點: {node.right.val if node.right else 'None'}")
            node.right = self._insert_recursive(node.right, value)
        
        self._update_height(node)
        balance = self._get_balance(node)
        
        if balance > 1 and value < node.left.val:
            self.logger.info(f"右旋轉以平衡節點: {node.val}")
            return self._rotate_right(node)
        
        if balance < -1 and value > node.right.val:
            self.logger.info(f"左旋轉以平衡節點: {node.val}")
            return self._rotate_left(node)
        
        if balance > 1 and value > node.left.val:
            self.logger.info(f"左旋轉左子節點並右旋轉以平衡節點: {node.val}")
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        if balance < -1 and value < node.right.val:
            self.logger.info(f"右旋轉右子節點並左旋轉以平衡節點: {node.val}")
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def delete(self, value: T):
        """刪除節點"""
        self.logger.info(f"開始刪除節點: {value}")
        self.root = self._delete_recursive(self.root, value)
    
    def _delete_recursive(self, node: Optional[BaseTree.Node], value: T) -> Optional[BaseTree.Node]:
        """遞歸刪除節點"""
        if not node:
            self.logger.info(f"節點 {value} 不存在")
            return node
        
        if value < node.val:
            self.logger.info(f"移動到左子節點: {node.left.val if node.left else 'None'}")
            node.left = self._delete_recursive(node.left, value)
        elif value > node.val:
            self.logger.info(f"移動到右子節點: {node.right.val if node.right else 'None'}")
            node.right = self._delete_recursive(node.right, value)
        else:
            self.logger.info(f"找到節點 {value}，準備刪除")
            if not node.left:
                self.logger.info(f"刪除節點 {value}，無左子節點")
                return node.right
            elif not node.right:
                self.logger.info(f"刪除節點 {value}，無右子節點")
                return node.left
            
            min_larger_node = self._get_min(node.right)
            self.logger.info(f"替換節點 {value} 為 {min_larger_node.val}")
            node.val = min_larger_node.val
            node.right = self._delete_recursive(node.right, min_larger_node.val)
        
        self._update_height(node)
        balance = self._get_balance(node)
        
        if balance > 1 and self._get_balance(node.left) >= 0:
            self.logger.info(f"右旋轉以平衡節點: {node.val}")
            return self._rotate_right(node)
        
        if balance > 1 and self._get_balance(node.left) < 0:
            self.logger.info(f"左旋轉左子節點並右旋轉以平衡節點: {node.val}")
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        if balance < -1 and self._get_balance(node.right) <= 0:
            self.logger.info(f"左旋轉以平衡節點: {node.val}")
            return self._rotate_left(node)
        
        if balance < -1 and self._get_balance(node.right) > 0:
            self.logger.info(f"右旋轉右子節點並左旋轉以平衡節點: {node.val}")
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def search(self, value: T) -> Optional[BaseTree.Node]:
        """搜尋節點"""
        self.logger.info(f"開始搜尋節點: {value}")
        return self._search_recursive(self.root, value)
    
    def _search_recursive(self, node: Optional[BaseTree.Node], value: T) -> Optional[BaseTree.Node]:
        """遞歸搜尋節點"""
        if not node:
            self.logger.info(f"節點 {value} 不存在")
            return None
        
        if node.val == value:
            self.logger.info(f"找到節點: {value}")
            return node
        
        if value < node.val:
            self.logger.info(f"移動到左子節點: {node.left.val if node.left else 'None'}")
            return self._search_recursive(node.left, value)
        else:
            self.logger.info(f"移動到右子節點: {node.right.val if node.right else 'None'}")
            return self._search_recursive(node.right, value)

class UnionFind(BaseAlgo):
    """並查集數據結構
    
    實現高效的集合合併和查找操作，並記錄詳細的日誌。
    
    Attributes:
        parent: 父節點數組，記錄每個元素的父節點
        rank: 秩數組，用於優化樹結構，減少查找時間
        logger: 日誌記錄器，用於記錄操作過程
    """
    
    def __init__(self, test_mode: bool = False):
        """初始化並查集"""
        super().__init__()
        self.parent = {}
        self.rank = {}
        self.test_mode = test_mode
        
        if not test_mode:
            try:
                self.fig, self.ax = plt.subplots()
            except Exception as e:
                self.logger.warning(f"無法創建圖形界面: {e}")
                self.fig = None
                self.ax = None
        else:
            self.fig = None
            self.ax = None
            
        self.animation = None
        self.logger.info("初始化並查集")

    def make_set(self, x):
        """創建一個新的集合
        
        Args:
            x: 要加入的元素
        """
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
            self.logger.info(f"創建新集合: {x}")

    def find(self, x):
        """查找元素所屬的集合
        
        Args:
            x: 要查找的元素
            
        Returns:
            該元素所屬集合的代表元素
        """
        if x not in self.parent:
            self.make_set(x)
            
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # 路徑壓縮
        return self.parent[x]

    def union(self, x, y):
        """合併兩個集合
        
        Args:
            x: 第一個元素
            y: 第二個元素
        """
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x != root_y:
            if self.rank[root_x] < self.rank[root_y]:
                root_x, root_y = root_y, root_x
            self.parent[root_y] = root_x
            if self.rank[root_x] == self.rank[root_y]:
                self.rank[root_x] += 1
            self.logger.info(f"合併集合: {x} 和 {y}")

class Heap(BaseAlgo):
    """堆數據結構
    
    實現基本的堆操作，包括插入、刪除和堆化操作，並記錄詳細的日誌。
    
    Attributes:
        heap: 存儲堆元素的列表
        logger: 日誌記錄器
    """
    
    def __init__(self, test_mode: bool = False):  # 添加 test_mode 參數
        super().__init__()
        self.heap = []
        self.test_mode = test_mode
        
        if not test_mode:
            try:
                self.fig, self.ax = plt.subplots()
            except Exception as e:
                self.logger.warning(f"無法創建圖形界面: {e}")
                self.fig = None
                self.ax = None
        else:
            self.fig = None
            self.ax = None
            
        self.animation = None
    
    def parent(self, i: int) -> int:
        """獲取父節點索引"""
        return (i - 1) // 2
    
    def left_child(self, i: int) -> int:
        """獲取左子節點索引"""
        return 2 * i + 1
    
    def right_child(self, i: int) -> int:
        """獲取右子節點索引"""
        return 2 * i + 2
    
    def insert(self, value: T):
        """插入新元素到堆中
        
        Args:
            value: 要插入的元素
        """
        self.heap.append(value)
        self.logger.info(f"插入元素: {value}")
        self._heapify_up(len(self.heap) - 1)
    
    def _heapify_up(self, index: int):
        """向上堆化
        
        將新插入的元素向上移動到適當的位置
        
        Args:
            index: 新插入元素的索引
        """
        while index > 0 and self.heap[self.parent(index)] < self.heap[index]:
            self.logger.debug(f"交換元素 {self.heap[index]} 和父節點 {self.heap[self.parent(index)]}")
            self.heap[index], self.heap[self.parent(index)] = self.heap[self.parent(index)], self.heap[index]
            index = self.parent(index)
        self.logger.info(f"堆化完成: {self.heap}")
    
    def extract_max(self) -> Optional[T]:
        """提取堆中的最大元素
        
        Returns:
            Optional[T]: 堆中的最大元素，如果堆為空則返回 None
        """
        if not self.heap:
            self.logger.warning("堆為空，無法提取最大元素")
            return None
        max_value = self.heap[0]
        self.logger.info(f"提取最大元素: {max_value}")
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return max_value
    
    def _heapify_down(self, index: int):
        """向下堆化
        
        將根元素向下移動到適當的位置
        
        Args:
            index: 根元素的索引
        """
        size = len(self.heap)
        while True:
            left = self.left_child(index)
            right = self.right_child(index)
            largest = index
            
            if left < size and self.heap[left] > self.heap[largest]:
                largest = left
            if right < size and self.heap[right] > self.heap[largest]:
                largest = right
            if largest == index:
                break
            self.logger.debug(f"交換元素 {self.heap[index]} 和子節點 {self.heap[largest]}")
            self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
            index = largest
        self.logger.info(f"堆化完成: {self.heap}")

class DataStructureFactory:
    """數據結構工廠類"""
    
    _structures = {
        "binary_tree": BinaryTree,
        "avl_tree": AVLTree,
        "union_find": UnionFind,
        "heap": Heap
    }
    
    @classmethod
    def create_structure(cls, structure_type: str, **kwargs) -> Any:
        """創建數據結構實例
        
        Args:
            structure_type: 數據結構類型
            **kwargs: 初始化參數
            
        Returns:
            創建的數據結構實例
        """
        if structure_type not in cls._structures:
            raise ValueError(f"不支援的數據結構: {structure_type}")
        return cls._structures[structure_type](**kwargs)

__all__ = [
    "BinaryTree",
    "AVLTree",
    "UnionFind",
    "Heap",
    "DataStructureFactory"
]
