from typing import Any, Optional, List, Union
from collections import deque
import logging
from mathalgo2.logger import setup_logger
import os
from pathlib import Path

# 獲取當前文件所在目錄的根目錄
ROOT_DIR = Path(__file__).parent.parent

# 設置日誌文件路徑
log_file = os.path.join(ROOT_DIR, "__log__", "structure.log")
logger = setup_logger("structure", log_file, level=logging.INFO)

class TreeNode:
    """樹節點類別"""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class Tree:
    """
    # 二元樹類別
    
    實現基本的二元樹操作。
    """
    
    def __init__(self):
        """初始化空樹"""
        self.root = None
        logger.info("樹結構初始化成功")
    
    def insert(self, value):
        """
        # 插入節點
        
        ## 參數
        * `value`: 要插入的值
        """
        if not self.root:
            self.root = TreeNode(value)
            logger.info(f"插入根節點: {value}")
            return
            
        def _insert_recursive(node, value):
            if value < node.value:
                if node.left is None:
                    node.left = TreeNode(value)
                    logger.info(f"插入左子節點: {value}")
                else:
                    _insert_recursive(node.left, value)
            else:
                if node.right is None:
                    node.right = TreeNode(value)
                    logger.info(f"插入右子節點: {value}")
                else:
                    _insert_recursive(node.right, value)
                    
        _insert_recursive(self.root, value)
    
    def search(self, value) -> Optional[TreeNode]:
        """
        # 搜尋節點
        
        ## 參數
        * `value`: 要搜尋的值
        
        ## 返回
        * TreeNode: 找到的節點
        * None: 如果沒找到
        """
        def _search_recursive(node, value):
            if node is None or node.value == value:
                return node
            
            if value < node.value:
                return _search_recursive(node.left, value)
            return _search_recursive(node.right, value)
            
        result = _search_recursive(self.root, value)
        if result:
            logger.info(f"找到節點: {value}")
        else:
            logger.info(f"未找到節點: {value}")
        return result
    
    def delete(self, value):
        """
        # 刪除節點
        
        ## 參數
        * `value`: 要刪除的值
        """
        def _find_min(node):
            current = node
            while current.left:
                current = current.left
            return current
            
        def _delete_recursive(node, value):
            if node is None:
                return None
                
            if value < node.value:
                node.left = _delete_recursive(node.left, value)
            elif value > node.value:
                node.right = _delete_recursive(node.right, value)
            else:
                # 節點有一個或沒有子節點
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left
                    
                # 節點有兩個子節點
                temp = _find_min(node.right)
                node.value = temp.value
                node.right = _delete_recursive(node.right, temp.value)
                
            return node
            
        self.root = _delete_recursive(self.root, value)
        logger.info(f"刪除節點: {value}")
    
    def inorder_traversal(self) -> List[Any]:
        """
        # 中序遍歷
        
        ## 返回
        * 遍歷結果列表
        """
        result = []
        
        def _inorder(node):
            if node:
                _inorder(node.left)
                result.append(node.value)
                _inorder(node.right)
                
        _inorder(self.root)
        logger.info(f"中序遍歷結果: {result}")
        return result
    
    def preorder_traversal(self) -> List[Any]:
        """
        # 前序遍歷
        
        ## 返回
        * 遍歷結果列表
        """
        result = []
        
        def _preorder(node):
            if node:
                result.append(node.value)
                _preorder(node.left)
                _preorder(node.right)
                
        _preorder(self.root)
        logger.info(f"前序遍歷結果: {result}")
        return result
    
    def postorder_traversal(self) -> List[Any]:
        """
        # 後序遍歷
        
        ## 返回
        * 遍歷結果列表
        """
        result = []
        
        def _postorder(node):
            if node:
                _postorder(node.left)
                _postorder(node.right)
                result.append(node.value)
                
        _postorder(self.root)
        logger.info(f"後序遍歷結果: {result}")
        return result
    
    def is_balanced(self) -> bool:
        """
        # 檢查樹是否平衡
        
        ## 返回
        * bool: 是否平衡
        """
        def _height(node):
            if not node:
                return 0
            return 1 + max(_height(node.left), _height(node.right))
            
        def _is_balanced_recursive(node):
            if not node:
                return True
                
            left_height = _height(node.left)
            right_height = _height(node.right)
            
            if abs(left_height - right_height) > 1:
                return False
                
            return _is_balanced_recursive(node.left) and _is_balanced_recursive(node.right)
            
        result = _is_balanced_recursive(self.root)
        logger.info(f"樹平衡檢查結果: {'平衡' if result else '不平衡'}")
        return result
    
    def level_order_traversal(self) -> List[List[Any]]:
        """
        # 層序遍歷
        
        ## 返回
        * 按層組織的節點值列表
        """
        if not self.root:
            return []
            
        result = []
        queue = [self.root]
        
        while queue:
            level = []
            level_size = len(queue)
            
            for _ in range(level_size):
                node = queue.pop(0)
                level.append(node.value)
                
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
                    
            result.append(level)
            
        logger.info(f"層序遍歷結果: {result}")
        return result
    
    def serialize(self) -> str:
        """
        # 序列化樹結構
        
        ## 返回
        * 樹的字符串表示
        """
        if not self.root:
            return "[]"
            
        result = []
        queue = [self.root]
        
        while queue:
            node = queue.pop(0)
            if node:
                result.append(str(node.value))
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append("null")
                
        # 移除尾部的 null
        while result[-1] == "null":
            result.pop()
            
        return "[" + ",".join(result) + "]"
    
    @classmethod
    def deserialize(cls, data: str) -> 'Tree':
        """
        # 從字符串創建樹
        
        ## 參數
        * `data`: 樹的字符串表示
        
        ## 返回
        * 新的樹實例
        """
        if data == "[]":
            return cls()
            
        values = data[1:-1].split(",")
        tree = cls()
        tree.root = TreeNode(int(values[0]))
        queue = [tree.root]
        i = 1
        
        while queue and i < len(values):
            node = queue.pop(0)
            
            # 左子節點
            if i < len(values) and values[i] != "null":
                node.left = TreeNode(int(values[i]))
                queue.append(node.left)
            i += 1
            
            # 右子節點
            if i < len(values) and values[i] != "null":
                node.right = TreeNode(int(values[i]))
                queue.append(node.right)
            i += 1
            
        return tree

class Stack:
    """
    # 堆疊類別
    
    實現後進先出(LIFO)的資料結構。
    """
    
    def __init__(self, max_size: int = None):
        """
        # 初始化空堆疊
        
        ## 參數
        * `max_size`: 堆疊最大容量，None 表示無限制
        """
        self.items = []
        self.max_size = max_size
    
    def __size__(self):
        """返回堆疊大小"""
        return len(self.items)
    
    def __iter__(self):
        """實現迭代器，從堆頂到堆底"""
        return iter(reversed(self.items))
    
    def __str__(self):
        """返回堆疊的字串表示"""
        return f"Stack({self.items})"
    
    def is_empty(self):
        """檢查堆疊是否為空"""
        return len(self.items) == 0
    
    def is_full(self):
        """檢查堆疊是否已滿"""
        return self.max_size is not None and len(self.items) >= self.max_size
    
    def push(self, item):
        """
        # 推入元素
        
        ## 參數
        * `item`: 要推入的元素
        
        ## 異常
        * OverflowError: 當堆疊已滿時
        """
        if self.is_full():
            raise OverflowError("Stack is full")
        self.items.append(item)
    
    def pop(self):
        """
        # 彈出元素
        
        ## 返回
        * 堆頂元素
        
        ## 異常
        * IndexError: 當堆疊為空時
        """
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items.pop()
    
    def peek(self):
        """
        # 查看堆頂元素
        
        ## 返回
        * 堆頂元素（不移除）
        
        ## 異常
        * IndexError: 當堆疊為空時
        """
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items[-1]
    
    def clear(self):
        """清空堆疊"""
        self.items.clear()
    
    def swap_top(self):
        """
        # 交換頂部兩個元素
        
        ## 異常
        * IndexError: 當堆疊元素少於2個時
        """
        if len(self.items) < 2:
            raise IndexError("Stack needs at least 2 elements to swap")
        self.items[-1], self.items[-2] = self.items[-2], self.items[-1]
    
    def rotate(self, n: int = 1):
        """
        # 旋轉堆疊元素
        
        ## 參數
        * `n`: 旋轉的元素數量
            * 正數：將頂部 n 個元素循環移動
            * 負數：將底部 n 個元素循環移動
        
        ## 異常
        * ValueError: 當n大於堆疊大小時
        
        ## 實現說明
        ### 向上旋轉 (n > 0)
        1. 取出頂部 n 個元素存入臨時列表
        2. 將剩餘元素轉為列表
        3. 清空當前堆疊
        4. 將臨時列表中的元素依序加入剩餘元素後
        5. 更新堆疊內容
        
        ### 向下旋轉 (n < 0)
        1. 獲取當前迭代順序（從頂到底）
        2. 取出最後 |n| 個元素存入臨時列表
        3. 清空當前堆疊
        4. 將臨時列表中的元素插入到迭代序列前端
        5. 反轉序列以保持正確的堆疊順序
        6. 依序將元素推入堆疊
        
        ## 範例
        ```python
        stack = Stack()
        # 向上旋轉
        [1,2,3,4] 旋轉 2 位
        1. temp = [4,3]
        2. remaining = [1,2]
        3. 結果 = [1,2,4,3]
        
        # 向下旋轉
        [1,2,3,4] 旋轉 -1 位
        1. re = [4,3,2,1]
        2. temp = [1]
        3. re = [1,4,3,2]
        4. 反轉後 = [2,3,4,1]
        ```
        """
        if abs(n) > len(self.items):
            raise ValueError("Rotation amount exceeds stack size")
            
        if n > 0:
            # 向上旋轉
            temp = []
            # 1. 取出頂部 n 個元素
            for _ in range(n):
                temp.append(self.items.pop())
            
            # 2. 將剩餘元素轉為列表
            remaining = list(self.items)
            
            # 3. 清空當前堆疊
            self.items = []
            
            # 4. 將臨時列表中的元素依序加入
            for item in temp:
                remaining.append(item)
            
            # 5. 更新堆疊內容
            self.items = remaining
        else:
            # 向下旋轉
            # 1. 獲取當前迭代順序（從頂到底）
            re = list(self)
            temp = []
            
            # 2. 取出最後 |n| 個元素
            for i in range(-n):
                temp.append(re.pop())
            
            # 3. 清空當前堆疊
            self.clear()

            # 4. 將臨時列表中的元素插入到前端
            for i in temp:
                re.insert(0, i)
                
            # 5. 反轉序列以保持正確的堆疊順序
            re.reverse()
            
            # 6. 依序將元素推入堆疊
            for i in re:
                self.push(i)

class Queue:
    """
    # 佇列類別
    
    實現先進先出(FIFO)的資料結構。
    """
    def __init__(self, max_size: Optional[int] = None):
        """
        初始化佇列
        
        ## 參數
        * `max_size`: 佇列最大容量，None 表示無限制
        """
        self._queue = deque()
        self.max_size = max_size
        logger.info("佇列初始化成功")

    def enqueue(self, item: Any) -> None:
        """
        # 加入元素到佇列
        
        ## 參數
        * `item`: 要加入的元素
        
        ## 異常
        * OverflowError: 當佇列已滿時
        """
        if self.is_full():
            logger.error("佇列已滿")
            raise OverflowError("Queue is full")
        self._queue.append(item)
        logger.info(f"元素 {item} 加入佇列")

    def dequeue(self) -> Any:
        """
        # 從佇列移除並返回元素
        
        ## 返回
        * 佇列首個元素
        
        ## 異常
        * IndexError: 當佇列為空時
        """
        if self.is_empty():
            logger.error("佇列為空")
            raise IndexError("Queue is empty")
        item = self._queue.popleft()
        logger.info(f"元素 {item} 從佇列移除")
        return item

    def peek(self) -> Any:
        """
        # 查看佇列首個元素
        
        ## 返回
        * 佇列首個元素（不移除）
        
        ## 異常
        * IndexError: 當佇列為空時
        """
        if self.is_empty():
            logger.error("佇列為空")
            raise IndexError("Queue is empty")
        return self._queue[0]

    def is_empty(self) -> bool:
        """檢查佇列是否為空"""
        return len(self._queue) == 0

    def is_full(self) -> bool:
        """檢查佇列是否已滿"""
        return self.max_size is not None and len(self._queue) >= self.max_size

    def size(self) -> int:
        """返回佇列中的元素數量"""
        return len(self._queue)

    def __str__(self) -> str:
        """
        將佇列轉換為字串表示
        
        ## 返回
        * str: 佇列的字串表示
        """
        return f"Queue({list(self._queue)})"

    def visualize(self, show_details: bool = False) -> str:
        """
        # 視覺化佇列狀態
        
        ## 參數
        * show_details: 是否顯示詳細資訊
        
        ## 返回
        * str: 佇列的視覺化表示
        """
        if self.is_empty():
            return "Queue is empty: ║║"

        # 基本視覺化
        items = list(self._queue)
        visual = "║ " + " <- ".join(str(item) for item in items) + " ║"
        
        if not show_details:
            return visual
            
        # 詳細資訊
        size_info = f"\nSize: {self.size()}"
        capacity_info = f"\nCapacity: {'unlimited' if self.max_size is None else self.max_size}"
        status_info = f"\nStatus: {'full' if self.is_full() else 'not full'}"
        
        # 添加指示器
        front_pointer = "  ↑ FRONT"
        rear_pointer = "  ↑ REAR"
        pointers = " " * len(str(items[0])) + front_pointer + " " * (len(visual) - len(str(items[0])) - len(front_pointer) - len(rear_pointer)) + rear_pointer
        
        return f"{visual}\n{pointers}{size_info}{capacity_info}{status_info}"

    def print_state(self):
        """
        # 視覺化佇列
        
        使用 visualize() 方法以視覺化方式顯示佇列的當前狀態，包含:
        - 佇列內容
        - 前端和後端指示器
        - 大小資訊
        - 容量資訊 
        - 狀態資訊
        """
        self.visualize(show_details=True)
        logger.info("\n" + self.visualize(show_details=True))

class LinkedListNode:
    """鏈結串列節點"""
    def __init__(self, data: Any):
        self.data = data
        self.next = None

class LinkedList:
    """
    # 鏈結串列類別
    
    實現基本的單向鏈結串列操作。
    """
    def __init__(self):
        """初始化空鏈結串列"""
        self.head = None
        logger.info("鏈結串列初始化成功")

    def append(self, data: Any) -> None:
        """
        # 添加節點到尾部
        
        ## 參數
        * `data`: 要添加的數據
        """
        if not self.head:
            self.head = LinkedListNode(data)
            logger.info(f"添加首個節點: {data}")
            return

        current = self.head
        while current.next:
            current = current.next
        current.next = LinkedListNode(data)
        logger.info(f"添加節點到尾部: {data}")

    def delete(self, data: Any) -> bool:
        """
        # 刪除指定數據的節點
        
        ## 參數
        * `data`: 要刪除的數據
        
        ## 返回
        * bool: 是否成功刪除
        """
        if not self.head:
            logger.info("鏈結串列為空，無法刪除")
            return False

        if self.head.data == data:
            self.head = self.head.next
            logger.info(f"刪除首個節點: {data}")
            return True

        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                logger.info(f"刪除節點: {data}")
                return True
            current = current.next

        logger.info(f"未找到要刪除的節點: {data}")
        return False

    def search(self, data: Any) -> Optional[LinkedListNode]:
        """
        # 搜尋指定數據的節點
        
        ## 參數
        * `data`: 要搜尋的數據
        
        ## 返回
        * LinkedListNode: 找到的節點
        * None: 如果未找到
        """
        current = self.head
        while current:
            if current.data == data:
                logger.info(f"找到節點: {data}")
                return current
            current = current.next
        logger.info(f"未找到節點: {data}")
        return None

    def display(self) -> List[Any]:
        """
        # 顯示鏈結串列內容
        
        ## 返回
        * 包含所有節點數據的列表
        """
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        logger.info(f"鏈結串列內容: {elements}")
        return elements

class Graph:
    """
    # 圖類別
    
    實現基本的圖操作，包含新增節點、新增邊、刪除節點、刪除邊等功能。
    使用相鄰列表(adjacency list)表示法儲存圖結構。
    
    ## 屬性
    * `graph`: 儲存圖的相鄰列表字典，鍵為節點，值為相鄰節點列表
    """
    
    def __init__(self):
        """初始化空圖"""
        self.graph = {}
        logger.info("圖結構初始化成功")
        
    def add_vertex(self, vertex: Any) -> None:
        """
        # 新增節點
        
        ## 參數
        * `vertex`: 要新增的節點值
        """
        if vertex not in self.graph:
            self.graph[vertex] = []
            logger.info(f"新增節點: {vertex}")
            
    def add_edge(self, vertex1: Any, vertex2: Any) -> None:
        """
        # 新增邊
        
        ## 參數
        * `vertex1`: 第一個節點
        * `vertex2`: 第二個節點
        """
        if vertex1 not in self.graph:
            self.add_vertex(vertex1)
        if vertex2 not in self.graph:
            self.add_vertex(vertex2)
            
        if vertex2 not in self.graph[vertex1]:
            self.graph[vertex1].append(vertex2)
            logger.info(f"新增邊: {vertex1} -> {vertex2}")
            
    def remove_vertex(self, vertex: Any) -> None:
        """
        # 刪除節點
        
        ## 參數
        * `vertex`: 要刪除的節點
        """
        if vertex in self.graph:
            del self.graph[vertex]
            for v in self.graph:
                if vertex in self.graph[v]:
                    self.graph[v].remove(vertex)
            logger.info(f"刪除節點: {vertex}")
            
    def remove_edge(self, vertex1: Any, vertex2: Any) -> None:
        """
        # 刪除邊
        
        ## 參數
        * `vertex1`: 第一個節點
        * `vertex2`: 第二個節點
        """
        if vertex1 in self.graph and vertex2 in self.graph[vertex1]:
            self.graph[vertex1].remove(vertex2)
            logger.info(f"刪除邊: {vertex1} -> {vertex2}")
    
    def visualize(self) -> None:
        """
        視覺化圖結構
        
        使用 networkx 和 matplotlib 將圖結構視覺化。
        
        Raises:
            ImportError: 未安裝 networkx 或 matplotlib 套件
        """
        logger.info("開始視覺化圖結構")
        
        try:
            import networkx as nx
            import matplotlib.pyplot as plt
            logger.debug("成功導入 networkx 和 matplotlib 模組")
        except ImportError as e:
            error_msg = "需要安裝 networkx 和 matplotlib 套件才能使用視覺化功能"
            logger.error(f"{error_msg}: {str(e)}")
            raise ImportError(error_msg) from e

        # 建立 NetworkX 圖物件
        G = nx.DiGraph()
        
        # 加入所有節點和邊
        for vertex in self.graph:
            G.add_node(vertex)
            for neighbor in self.graph[vertex]:
                G.add_edge(vertex, neighbor)
        
        # 設定視覺化參數
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G)
        
        # 繪製節點
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
        
        # 繪製邊
        nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=20)
        
        # 加入節點標籤
        nx.draw_networkx_labels(G, pos)
        
        plt.title("Graph Visualization")
        plt.axis('off')
        
        logger.debug("完成圖結構視覺化")
        plt.show()

__all__ = [
    "Tree",
    "TreeNode",
    "Stack",
    "Queue",
    "LinkedList",
    "LinkedListNode",
    "Graph"
]

