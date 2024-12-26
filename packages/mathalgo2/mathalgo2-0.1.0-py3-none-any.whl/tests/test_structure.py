import pytest
from mathalgo2.structure import Tree, Stack, Queue, LinkedList

# TreeNode 和 Tree 的測試
class TestTree:
    """測試二元樹的所有功能"""
    
    @pytest.fixture
    def sample_tree(self):
        """建立測試用的樹"""
        tree = Tree()
        values = [5, 3, 7, 2, 4, 6, 8]
        for value in values:
            tree.insert(value)
        return tree
    
    def test_tree_insertion(self):
        """測試樹的插入功能"""
        tree = Tree()
        tree.insert(5)
        assert tree.root.value == 5
        tree.insert(3)
        assert tree.root.left.value == 3
        tree.insert(7)
        assert tree.root.right.value == 7
    
    def test_tree_search(self, sample_tree):
        """測試樹的搜尋功能"""
        # 測試存在的值
        node = sample_tree.search(4)
        assert node is not None
        assert node.value == 4
        
        # 測試不存在的值
        node = sample_tree.search(10)
        assert node is None
    
    def test_tree_deletion(self, sample_tree):
        """測試樹的刪除功能"""
        # 刪除葉節點
        sample_tree.delete(2)
        assert sample_tree.search(2) is None
        
        # 刪除有一個子節點的節點
        sample_tree.delete(3)
        assert sample_tree.search(3) is None
        
        # 刪除有兩個子節點的節點
        sample_tree.delete(7)
        assert sample_tree.search(7) is None
    
    def test_tree_traversals(self, sample_tree):
        """測試樹的遍歷方法"""
        # 測試中序遍歷
        assert sample_tree.inorder_traversal() == [2, 3, 4, 5, 6, 7, 8]
        
        # 測試前序遍歷
        assert sample_tree.preorder_traversal() == [5, 3, 2, 4, 7, 6, 8]
        
        # 測試後序遍歷
        assert sample_tree.postorder_traversal() == [2, 4, 3, 6, 8, 7, 5]
        
        # 測試層序遍歷
        assert sample_tree.level_order_traversal() == [[5], [3, 7], [2, 4, 6, 8]]
    
    def test_tree_serialization(self, sample_tree):
        """測試樹的序列化和反序列化"""
        # 序列化
        serialized = sample_tree.serialize()
        
        # 反序列化
        new_tree = Tree.deserialize(serialized)
        
        # 驗證兩棵樹是否相同
        assert new_tree.inorder_traversal() == sample_tree.inorder_traversal()

# Stack 的測試
class TestStack:
    """測試堆疊的所有功能"""
    
    @pytest.fixture
    def empty_stack(self):
        """建立空堆疊"""
        return Stack()
    
    @pytest.fixture
    def filled_stack(self):
        """建立已填充的堆疊"""
        stack = Stack()
        for i in range(5):
            stack.push(i)
        return stack
    
    def test_stack_push(self, empty_stack):
        """測試堆疊的推入操作"""
        empty_stack.push(1)
        assert empty_stack.peek() == 1
        assert len(empty_stack) == 1
    
    def test_stack_pop(self, filled_stack):
        """測試堆疊的彈出操作"""
        assert filled_stack.pop() == 4
        assert len(filled_stack) == 4
    
    def test_stack_peek(self, filled_stack):
        """測試堆疊的查看操作"""
        assert filled_stack.peek() == 4
        assert len(filled_stack) == 5  # 確保peek不會移除元素
    
    def test_stack_empty_operations(self, empty_stack):
        """測試空堆疊的操作"""
        with pytest.raises(IndexError):
            empty_stack.pop()
        
        with pytest.raises(IndexError):
            empty_stack.peek()
    
    def test_stack_full_operations(self):
        """測試已滿堆疊的操作"""
        stack = Stack(max_size=2)
        stack.push(1)
        stack.push(2)
        
        with pytest.raises(OverflowError):
            stack.push(3)

# Queue 的測試
class TestQueue:
    """測試佇列的所有功能"""
    
    @pytest.fixture
    def empty_queue(self):
        """建立空佇列"""
        return Queue()
    
    @pytest.fixture
    def filled_queue(self):
        """建立已填充的佇列"""
        queue = Queue()
        for i in range(5):
            queue.enqueue(i)
        return queue
    
    def test_queue_enqueue(self, empty_queue):
        """測試佇列的加入操作"""
        empty_queue.enqueue(1)
        assert empty_queue.peek() == 1
        assert empty_queue.size() == 1
    
    def test_queue_dequeue(self, filled_queue):
        """測試佇列的移除操作"""
        assert filled_queue.dequeue() == 0
        assert filled_queue.size() == 4
    
    def test_queue_peek(self, filled_queue):
        """測試佇列的查看操作"""
        assert filled_queue.peek() == 0
        assert filled_queue.size() == 5
    
    def test_queue_empty_operations(self, empty_queue):
        """測試空佇列的操作"""
        with pytest.raises(IndexError):
            empty_queue.dequeue()
        
        with pytest.raises(IndexError):
            empty_queue.peek()
    
    def test_queue_visualization(self, filled_queue):
        """測試佇列的視覺化功能"""
        visual = filled_queue.visualize(show_details=True)
        assert isinstance(visual, str)
        assert "FRONT" in visual
        assert "REAR" in visual

# LinkedList 的測試
class TestLinkedList:
    """測試鏈結串列的所有功能"""
    
    @pytest.fixture
    def empty_list(self):
        """建立空鏈結串列"""
        return LinkedList()
    
    @pytest.fixture
    def filled_list(self):
        """建立已填充的鏈結串列"""
        linked_list = LinkedList()
        for i in range(5):
            linked_list.append(i)
        return linked_list
    
    def test_list_append(self, empty_list):
        """測試鏈結串列的添加操作"""
        empty_list.append(1)
        assert empty_list.display() == [1]
    
    def test_list_delete(self, filled_list):
        """測試鏈結串列的刪除操作"""
        assert filled_list.delete(2) is True
        assert 2 not in filled_list.display()
    
    def test_list_search(self, filled_list):
        """測試鏈結串列的搜尋操作"""
        node = filled_list.search(3)
        assert node is not None
        assert node.data == 3
        
        node = filled_list.search(10)
        assert node is None
    
    def test_list_display(self, filled_list):
        """測試鏈結串列的顯示操作"""
        assert filled_list.display() == [0, 1, 2, 3, 4] 