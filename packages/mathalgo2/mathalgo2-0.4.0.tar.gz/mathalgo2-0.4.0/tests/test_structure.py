import pytest
from mathalgo2.Structure import Tree, Stack, Queue, LinkedList, Graph

# Tree Tests
class TestTree:
    def test_tree_initialization(self):
        tree = Tree()
        assert tree.root is None
        
    def test_tree_insert_and_search(self):
        tree = Tree()
        tree.insert(5)
        tree.insert(3)
        tree.insert(7)
        
        assert tree.search(5).value == 5
        assert tree.search(3).value == 3
        assert tree.search(7).value == 7
        assert tree.search(10) is None
        
    def test_tree_traversals(self):
        tree = Tree()
        values = [5, 3, 7, 2, 4]
        for val in values:
            tree.insert(val)
            
        assert tree.inorder_traversal() == [2, 3, 4, 5, 7]
        assert tree.preorder_traversal() == [5, 3, 2, 4, 7]
        assert tree.level_order_traversal() == [[5], [3, 7], [2, 4]]
        
    def test_tree_serialization(self):
        tree = Tree()
        tree.insert(1)
        tree.insert(2)
        tree.insert(3)
        
        serialized = tree.serialize()
        new_tree = Tree.deserialize(serialized)
        assert new_tree.inorder_traversal() == tree.inorder_traversal()

# Stack Tests
class TestStack:
    def test_stack_operations(self):
        stack = Stack()
        assert stack.is_empty()
        
        stack.push(1)
        stack.push(2)
        assert stack.peek() == 2
        assert stack.pop() == 2
        assert stack.peek() == 1
        
    def test_stack_max_size(self):
        stack = Stack(max_size=2)
        stack.push(1)
        stack.push(2)
        
        with pytest.raises(OverflowError):
            stack.push(3)
            
    def test_stack_empty_pop(self):
        stack = Stack()
        with pytest.raises(IndexError):
            stack.pop()

# Queue Tests
class TestQueue:
    def test_queue_operations(self):
        queue = Queue()
        assert queue.is_empty()
        
        queue.enqueue(1)
        queue.enqueue(2)
        assert queue.peek() == 1
        assert queue.dequeue() == 1
        assert queue.peek() == 2
        
    def test_queue_max_size(self):
        queue = Queue(max_size=2)
        queue.enqueue(1)
        queue.enqueue(2)
        
        with pytest.raises(OverflowError):
            queue.enqueue(3)
            
    def test_queue_empty_dequeue(self):
        queue = Queue()
        with pytest.raises(IndexError):
            queue.dequeue()

# LinkedList Tests
class TestLinkedList:
    def test_linkedlist_operations(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        
        assert ll.display() == [1, 2, 3]
        assert ll.search(2) is not None
        assert ll.search(4) is None
        
        assert ll.delete(2) is True
        assert ll.display() == [1, 3]
        assert ll.delete(4) is False

# Graph Tests
class TestGraph:
    def test_graph_operations(self):
        graph = Graph()
        
        # Test adding vertices and edges
        graph.add_vertex('A')
        graph.add_vertex('B')
        graph.add_edge('A', 'B')
        
        assert 'A' in graph.graph
        assert 'B' in graph.graph
        assert 'B' in graph.graph['A']
        
        # Test removing edge and vertex
        graph.remove_edge('A', 'B')
        assert 'B' not in graph.graph['A']
        
        graph.remove_vertex('B')
        assert 'B' not in graph.graph 