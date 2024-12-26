from mathalgo2.structure import Stack

class DFS:
    """
    # 深度優先搜尋演算法
    
    實現圖的深度優先搜尋功能。
    """
    
    def __init__(self, graph: dict):
        """
        # 初始化圖結構
        
        ## 參數
        * `graph`: 以字典表示的圖，其中鍵為節點，值為相鄰節點列表
        """
        self.graph = graph
        
    def search(self, start: str, target: str) -> list:
        """
        # 執行深度優先搜尋
        
        ## 參數
        * `start`: 起始節點
        * `target`: 目標節點
        
        ## 返回
        * 從起始節點到目標節點的路徑列表
        """
        visited = set()
        path = []
        
        def dfs_recursive(current: str, target: str, path: list) -> bool:
            visited.add(current)
            path.append(current)
            
            if current == target:
                return True
                
            for neighbor in self.graph[current]:
                if neighbor not in visited:
                    if dfs_recursive(neighbor, target, path):
                        return True
            
            path.pop()
            return False
            
        dfs_recursive(start, target, path)
        return path if path and path[-1] == target else []

def dfs_iterative(graph, start):
    # # 使用棧實現的深度優先搜索
    #
    # ## Args
    # - graph (dict): 圖的鄰接表表示
    # - start: 起始節點
    #
    # ## Returns
    # - list: 遍歷順序的節點列表
    #
    # ## Example
    # ```python
    # graph = {
    #     'A': ['B', 'C'],
    #     'B': ['A', 'D', 'E'],
    #     'C': ['A', 'F'],
    #     'D': ['B'],
    #     'E': ['B', 'F'],
    #     'F': ['C', 'E']
    # }
    # result = dfs_iterative(graph, 'A')
    # # result: ['A', 'C', 'F', 'E', 'B', 'D']
    # ```
    stack = Stack()
    visited = set()
    result = []
    
    stack.push(start)
    
    while not stack.is_empty():
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            result.append(vertex)
            
            # 將相鄰節點按照逆序壓入棧中（為了保持遍歷順序與遞歸版本類似）
            for next_node in reversed(graph[vertex]):
                if next_node not in visited:
                    stack.push(next_node)
    
    return result

def find_path_dfs(graph, start, end, visited=None):
    # # 使用DFS尋找從起點到終點的路徑
    #
    # ## Args
    # - graph (dict): 圖的鄰接表表示
    # - start: 起始節點
    # - end: 目標節點
    # - visited (set): 已訪問節點的集合
    #
    # ## Returns
    # - list: 如果存在路徑，返回路徑列表；否則返回空列表
    #
    # ## Example
    # ```python
    # graph = {
    #     'A': ['B', 'C'],
    #     'B': ['A', 'D', 'E'],
    #     'C': ['A', 'F'],
    #     'D': ['B'],
    #     'E': ['B', 'F'],
    #     'F': ['C', 'E']
    # }
    # path = find_path_dfs(graph, 'A', 'F')
    # # path: ['A', 'C', 'F']
    # ```
    if visited is None:
        visited = set()
    
    if start == end:
        return [start]
    
    visited.add(start)
    
    for next_node in graph[start]:
        if next_node not in visited:
            path = find_path_dfs(graph, next_node, end, visited)
            if path:
                return [start] + path
    
    return []
