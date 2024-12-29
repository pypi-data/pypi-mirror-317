import pytest
import numpy as np
from mathalgo2.algorithm.GraphAlgo import GraphAlgo

@pytest.fixture
def simple_graph():
    """創建一個簡單的測試圖"""
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D'],
        'C': ['A', 'D'],
        'D': ['B', 'C']
    }
    weights = {
        ('A', 'B'): 1.0,
        ('A', 'C'): 2.0,
        ('B', 'D'): 3.0,
        ('C', 'D'): 1.0
    }
    return graph, weights

@pytest.fixture
def graph_algo(simple_graph):
    """創建GraphAlgo實例"""
    graph, weights = simple_graph
    return GraphAlgo(graph, weights, animation_speed=0)  # 設置動畫速度為0以避免視覺化延遲

class TestGraphAlgo:
    def test_initialization(self, graph_algo, simple_graph):
        """測試圖算法類的初始化"""
        graph, weights = simple_graph
        assert graph_algo.graph == graph
        assert all(
            graph_algo.weights.get((u, v)) == w or graph_algo.weights.get((v, u)) == w
            for (u, v), w in weights.items()
        )

    def test_validate_start_node(self, graph_algo):
        """測試起始節點驗證"""
        # 有效節點
        graph_algo._validate_start_node('A')
        
        # 無效節點
        with pytest.raises(KeyError):
            graph_algo._validate_start_node('X')

    def test_bfs(self, graph_algo):
        """測試廣度優先搜尋"""
        result = graph_algo.bfs('A')
        # 檢查所有節點都被訪問
        assert set(result) == {'A', 'B', 'C', 'D'}
        # 檢查起始節點是否為第一個
        assert result[0] == 'A'
        # 檢查相鄰節點是否在第二層
        assert set(result[1:3]) == {'B', 'C'}

    def test_dfs(self, graph_algo):
        """測試深度優先搜尋"""
        result = graph_algo.dfs('A')
        # 檢查所有節點都被訪問
        assert set(result) == {'A', 'B', 'C', 'D'}
        # 檢查起始節點是否為第一個
        assert result[0] == 'A'

    def test_dijkstra(self, graph_algo):
        """測試Dijkstra最短路徑算法"""
        distances, predecessors = graph_algo.dijkstra('A')
        
        # 檢查距離
        assert distances['A'] == 0
        assert distances['B'] == 1.0
        assert distances['C'] == 2.0
        assert distances['D'] == min(4.0, 3.0)  # 可能通過B或C到達D

        # 檢查路徑存在性
        assert all(node in predecessors for node in ['A', 'B', 'C', 'D'])

    def test_get_shortest_path(self, graph_algo):
        """測試獲取最短路徑"""
        path, distance = graph_algo.get_shortest_path('A', 'D')
        
        # 檢查路徑是否有效
        assert path[0] == 'A'
        assert path[-1] == 'D'
        assert len(path) >= 2
        
        # 檢查路徑連續性
        for i in range(len(path)-1):
            assert path[i+1] in graph_algo.graph[path[i]]

        # 檢查不存在的路徑
        with pytest.raises(KeyError):
            graph_algo.get_shortest_path('A', 'X')

    def test_callback_functionality(self, graph_algo):
        """測試回調函數功能"""
        visited_nodes = []
        def callback(node):
            visited_nodes.append(node)
        
        # 測試BFS的回調
        graph_algo.bfs('A', callback)
        assert len(visited_nodes) == len(graph_algo.graph)
        
        # 重置並測試DFS的回調
        visited_nodes.clear()
        graph_algo.dfs('A', callback)
        assert len(visited_nodes) == len(graph_algo.graph)

    @pytest.mark.skip(reason="視覺化測試在CI環境中可能不穩定")
    def test_visualization_initialization(self, graph_algo):
        """測試視覺化初始化"""
        graph_algo._init_visualization("TEST")
        if graph_algo.fig is not None:  # 如果有networkx
            assert graph_algo.colors['A'] == graph_algo.node_colors['unvisited']
            assert graph_algo.pos is not None 