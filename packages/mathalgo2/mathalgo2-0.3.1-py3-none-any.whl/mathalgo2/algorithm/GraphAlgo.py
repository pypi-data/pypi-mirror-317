from typing import List, Dict, Any, Optional, Tuple, Union, Callable
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import numpy as np
from mathalgo2.logger import setup_logger, logging
import os
from pathlib import Path
from collections import deque
import heapq

"""
# GraphAlgo 模組

提供圖論相關演算法的實作與視覺化功能。

## 主要功能
- 深度優先搜尋 (DFS)
- 廣度優先搜尋 (BFS) 
- 最短路徑算法 (Dijkstra)
- 最小生成樹 [待實現]
- 拓撲排序 [待實現]
- 強連通分量 [待實現]

每個演算法都提供:
- 基本功能實作
- 視覺化過程
- 詳細日誌記錄
- 效能分析
- 動畫控制
"""

# 設置根目錄和日誌
ROOT_DIR = Path(__file__).parent.parent.parent
log_file = ROOT_DIR / "__log__" / "GraphAlgo.log"
logger = setup_logger("GraphAlgo", log_file, level=logging.INFO)

class Algorithm(ABC):
    """演算法基礎抽象類別
    
    提供所有圖論演算法的共用介面和基本功能。
    """
    
    def __init__(self):
        """初始化基礎類別"""
        self.logger = logger
        
    @abstractmethod
    def visualize(self, *args, **kwargs):
        """視覺化方法的抽象介面"""
        pass

class GraphAlgo(Algorithm):
    """圖論演算法類別
    
    實作各種圖論演算法並提供視覺化功能。
    
    Attributes:
        graph (Dict[Any, List[Any]]): 圖的鄰接表表示
        weights (Dict[Tuple[Any, Any], float]): 邊的權重
        colors (Dict[Any, str]): 節點顏色映射，用於視覺化
        pos (Dict): 節點位置映射，用於視覺化
        fig (Figure): matplotlib 圖形物件
        ax (Axes): matplotlib 座標軸物件
        animation_speed (float): 動畫速度控制
        node_colors (Dict[str, str]): 節點狀態對應的顏色
        edge_colors (Dict[str, str]): 邊狀態對應的顏色
    """
    
    def __init__(self, graph: Dict[Any, List[Any]], weights: Dict[Tuple[Any, Any], float] = None, animation_speed: float = 0.5):
        """初始化圖論演算法類別
        
        Args:
            graph: 以鄰接表形式表示的圖，key為節點，value為相鄰節點列表
            weights: 邊的權重字典，key為(u,v)表示邊，value為權重
            animation_speed: 視覺化動畫速度，預設0.5秒
        """
        super().__init__()
        self.graph = graph
        self.weights = weights if weights else {(u,v):1.0 for u in graph for v in graph[u]}
        self.colors = {}  # 節點顏色映射
        self.pos = None   # 節點位置映射
        self.fig = None
        self.ax = None
        self.animation_speed = animation_speed
        
        # 定義視覺化顏色方案
        self.node_colors = {
            'unvisited': 'white',
            'visiting': 'red',
            'visited': 'lightblue',
            'path': 'yellow',
            'start': 'green',
            'end': 'purple'
        }
        
        self.edge_colors = {
            'unvisited': 'black',
            'visiting': 'red',
            'visited': 'blue',
            'path': 'yellow'
        }
        
        self.logger.info(f"初始化圖論類別，節點數: {len(graph)}")
        
    def _validate_start_node(self, start: Any):
        """驗證起始節點是否有效
        
        Args:
            start: 起始節點
            
        Raises:
            KeyError: 當起始節點不在圖中時
        """
        if start not in self.graph:
            self.logger.error(f"起始節點 {start} 不在圖中")
            raise KeyError(f"節點 {start} 不存在")
            
    def _init_visualization(self, algorithm_name: str):
        """初始化視覺化設定
        
        Args:
            algorithm_name: 演算法名稱，用於設置視窗標題
        """
        try:
            import networkx as nx
            self.fig, self.ax = plt.subplots(figsize=(10, 8))
            G = nx.Graph(self.graph)
            self.pos = nx.spring_layout(G)
            self.colors = {node: self.node_colors['unvisited'] for node in self.graph}
            self.ax.set_title(f"{algorithm_name} Visualization")
        except ImportError:
            self.logger.warning("需要安裝networkx才能進行圖形視覺化")
            print("請安裝networkx: pip install networkx")
            
    def dijkstra(self, start: Any, end: Any = None) -> Tuple[Dict[Any, float], Dict[Any, Any]]:
        """Dijkstra最短路徑演算法
        
        原理: 使用優先隊列實現的Dijkstra算法，找出從起點到所有其他點的最短路徑
        時間複雜度: O((V + E)logV)
        空間複雜度: O(V)
        
        Args:
            start: 起始節點
            end: 目標節點(可選)，若指定則提前結束
            
        Returns:
            (distances, predecessors): 距離字典和前驅節點字典
        """
        self._validate_start_node(start)
        self.logger.info(f"開始Dijkstra算法，起始節點: {start}")
        
        distances = {node: float('infinity') for node in self.graph}
        distances[start] = 0
        predecessors = {node: None for node in self.graph}
        pq = [(0, start)]
        visited = set()
        
        while pq:
            current_distance, current = heapq.heappop(pq)
            
            if current in visited:
                continue
                
            visited.add(current)
            self.colors[current] = self.node_colors['visiting']
            
            if self.fig is not None:
                self._update_graph_plot()
                
            if current == end:
                break
                
            for neighbor in self.graph[current]:
                if neighbor in visited:
                    continue
                    
                weight = self.weights.get((current, neighbor)) or self.weights.get((neighbor, current), 1.0)
                distance = current_distance + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current
                    heapq.heappush(pq, (distance, neighbor))
                    
            self.colors[current] = self.node_colors['visited']
            
        self.logger.info("Dijkstra算法完成")
        return distances, predecessors
        
    def get_shortest_path(self, start: Any, end: Any) -> Tuple[List[Any], float]:
        """獲取兩點間的最短路徑
        
        Args:
            start: 起始節點
            end: 目標節點
            
        Returns:
            (path, distance): 最短路徑列表和總距離
        """
        distances, predecessors = self.dijkstra(start, end)
        
        if distances[end] == float('infinity'):
            return [], float('infinity')
            
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = predecessors[current]
        path.reverse()
        
        return path, distances[end]
        
    def dfs(self, start: Any, callback: Optional[Callable[[Any], None]] = None) -> List[Any]:
        """深度優先搜尋演算法
        
        原理: 從起始節點開始，盡可能深地搜尋圖的分支
        時間複雜度: O(V + E) - V為節點數，E為邊數
        空間複雜度: O(V) - 需要額外空間存儲訪問狀態
        
        Args:
            start: 起始節點
            callback: 可選的回調函數，用於自定義節點處理邏輯
            
        Returns:
            訪問順序列表
        """
        self._validate_start_node(start)
        self.logger.info(f"開始DFS搜尋，起始節點: {start}")
        
        visited = set()
        result = []
        
        def _dfs_helper(vertex: Any):
            visited.add(vertex)
            result.append(vertex)
            self.logger.debug(f"訪問節點: {vertex}")
            self.colors[vertex] = self.node_colors['visiting']
            
            if callback:
                callback(vertex)
                
            if self.fig is not None:
                self._update_graph_plot()
                
            for neighbor in self.graph[vertex]:
                if neighbor not in visited:
                    self.logger.debug(f"從 {vertex} 訪問鄰居節點 {neighbor}")
                    _dfs_helper(neighbor)
            
            self.colors[vertex] = self.node_colors['visited']
                    
        _dfs_helper(start)
        self.logger.info(f"DFS搜尋完成，訪問順序: {result}")
        return result
        
    def bfs(self, start: Any, callback: Optional[Callable[[Any], None]] = None) -> List[Any]:
        """廣度優先搜尋演算法 (Breadth-First Search, BFS)
        
        原理: 
        1. 從起始節點開始，逐層訪問圖中的節點
        2. 使用佇列(queue)來儲存待訪問的節點，確保按照"先進先出"的順序進行訪問
        3. 對於每個訪問的節點，將其未訪問過的相鄰節點加入佇列
        4. 重複此過程直到佇列為空
        
        特點:
        - 保證找到的路徑是最短路徑（以邊數計算）
        - 適合用於尋找最短路徑、層次遍歷等場景
        - 需要較大的記憶體空間來存儲佇列
        
        時間複雜度: O(V + E) 
        - V: 節點數，每個節點都需要訪問一次
        - E: 邊數，每條邊都需要檢查一次
        
        空間複雜度: O(V)
        - 需要額外空間存儲訪問狀態集合(visited)
        - 需要佇列空間存儲待訪問的節點，最差情況下可能包含所有節點
        
        Args:
            start: 起始節點，搜尋的起點。必須是圖中存在的節點。
            callback: 可選的回調函數，用於自定義節點處理邏輯。
                     函數簽名應為 callback(node)，其中node為當前訪問的節點。
                     在訪問每個節點時會被調用。
            
        Returns:
            List[Any]: 按照訪問順序排列的節點列表。
                      列表中的每個元素都是圖中的一個節點。
            
        Raises:
            KeyError: 當起始節點不在圖中時拋出此異常
            
        使用範例:
            >>> graph = GraphAlgo({'A': ['B', 'C'], 'B': ['A', 'D'], 'C': ['A'], 'D': ['B']})
            >>> result = graph.bfs('A')
            >>> print(result)  # 可能的輸出: ['A', 'B', 'C', 'D']
        """
        # 驗證起始節點是否合法
        self._validate_start_node(start)
        self.logger.info(f"開始BFS搜尋，起始節點: {start}")
        self.logger.info(f"圖的結構: {self.graph}")
        
        # 初始化資料結構
        visited = {start}  # 使用集合記錄已訪問的節點，保證O(1)的查詢時間
        result = []       # 存儲訪問順序的列表
        queue = deque([start])  # 使用雙端佇列實現FIFO，支援O(1)的頭尾操作
        
        self.logger.debug("初始化完成:")
        self.logger.debug(f"- 已訪問節點集合: {visited}")
        self.logger.debug(f"- 初始佇列狀態: {list(queue)}")
        self.logger.debug(f"- 訪問順序列表: {result}")
        
        # 主要搜尋迴圈 - 當佇列非空時持續執行
        iteration = 0
        while queue:
            iteration += 1
            self.logger.debug(f"\n=== 迭代 {iteration} 開始 ===")
            
            # 從佇列前端取出當前要訪問的節點
            vertex = queue.popleft()
            result.append(vertex)
            self.logger.debug(f"從佇列取出節點: {vertex}")
            self.logger.debug(f"當前佇列狀態: {list(queue)}")
            
            # 更新節點視覺化狀態為正在訪問
            self.colors[vertex] = self.node_colors['visiting']
            self.logger.debug(f"將節點 {vertex} 標記為正在訪問狀態 (顏色: {self.node_colors['visiting']})")
            
            # 如果提供了回調函數，執行自定義處理
            if callback:
                self.logger.debug(f"對節點 {vertex} 執行使用者提供的回調函數")
                try:
                    callback(vertex)
                except Exception as e:
                    self.logger.error(f"回調函數執行出錯: {str(e)}")
                    raise
                
            # 更新視覺化顯示
            if self.fig is not None:
                self.logger.debug("更新圖形視覺化顯示")
                self._update_graph_plot()
                
            # 處理當前節點的所有相鄰節點
            neighbors = self.graph[vertex]
            self.logger.debug(f"節點 {vertex} 的相鄰節點列表: {neighbors}")
            
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    self.logger.debug(f"發現未訪問的相鄰節點 {neighbor}:")
                    self.logger.debug(f"- 加入已訪問集合: {visited}")
                    self.logger.debug(f"- 加入佇列: {list(queue)}")
                else:
                    self.logger.debug(f"相鄰節點 {neighbor} 已被訪問，跳過")
                    
            # 更新節點視覺化狀態為已訪問
            self.colors[vertex] = self.node_colors['visited']
            self.logger.debug(f"將節點 {vertex} 標記為已訪問狀態 (顏色: {self.node_colors['visited']})")
            self.logger.debug(f"=== 迭代 {iteration} 結束 ===\n")
            
        # 搜尋完成，輸出統計信息
        self.logger.info("BFS搜尋完成:")
        self.logger.info(f"- 總迭代次數: {iteration}")
        self.logger.info(f"- 訪問節點數: {len(result)}")
        self.logger.info(f"- 訪問順序: {result}")
        self.logger.debug(f"- 最終已訪問集合: {visited}")
        
        return result
        
    def visualize(self, algorithm: str = "dfs", start: Any = None, 
                 end: Any = None, callback: Optional[Callable[[Any], None]] = None):
        """圖論演算法視覺化
        
        Args:
            algorithm: 要視覺化的算法，可選 "dfs"、"bfs" 或 "dijkstra"
            start: 起始節點，如果為None則使用第一個節點
            end: 目標節點(僅用於最短路徑算法)
            callback: 可選的回調函數，用於自定義節點處理邏輯
        """
        self.logger.info(f"開始視覺化 {algorithm} 搜尋")
        self._init_visualization(algorithm.upper())
        
        if start is None:
            start = list(self.graph.keys())[0]
            
        try:
            if algorithm.lower() == "dfs":
                self.dfs(start, callback)
            elif algorithm.lower() == "bfs":
                self.bfs(start, callback)
            elif algorithm.lower() == "dijkstra" and end is not None:
                path, distance = self.get_shortest_path(start, end)
                if path:
                    for node in path:
                        self.colors[node] = self.node_colors['path']
                        if self.fig is not None:
                            self._update_graph_plot()
            else:
                self.logger.error(f"不支援的算法: {algorithm}")
                raise ValueError(f"不支援的算法: {algorithm}")
                
            plt.close()
            
        except Exception as e:
            self.logger.error(f"視覺化過程發生錯誤: {str(e)}")
            raise
            
    def _update_graph_plot(self):
        """更新圖的視覺化"""
        try:
            import networkx as nx
            
            self.ax.clear()
            G = nx.Graph(self.graph)
            
            # 繪製節點
            nx.draw_networkx_nodes(G, self.pos, 
                                 node_color=[self.colors[node] for node in G.nodes()],
                                 node_size=500)
            
            # 繪製邊
            nx.draw_networkx_edges(G, self.pos)
            
            # 添加節點標籤
            nx.draw_networkx_labels(G, self.pos)
            
            # 添加邊權重標籤
            edge_labels = {(u,v): self.weights.get((u,v)) or self.weights.get((v,u), 1.0)
                         for u in self.graph for v in self.graph[u]}
            nx.draw_networkx_edge_labels(G, self.pos, edge_labels=edge_labels)
            
            self.ax.set_title("Graph Algorithm Visualization")
            plt.pause(self.animation_speed)
            
        except ImportError:
            self.logger.warning("需要安裝networkx才能進行圖形視覺化")

__all__ = [
    "GraphAlgo"
]
