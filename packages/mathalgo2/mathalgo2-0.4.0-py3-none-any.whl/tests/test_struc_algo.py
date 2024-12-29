import pytest
from mathalgo2.algorithm.StrucAlgo import (
    BinaryTree, AVLTree, UnionFind, Heap, DataStructureFactory
)
import os
from pathlib import Path

# ====== Fixtures ======
@pytest.fixture
def binary_tree():
    """創建二元樹實例"""
    return BinaryTree()

@pytest.fixture
def avl_tree():
    """創建 AVL 樹實例"""
    return AVLTree()

@pytest.fixture
def heap():
    """創建堆實例"""
    return Heap()

@pytest.fixture
def union_find():
    """創建並查集實例"""
    return UnionFind(10)  # 創建大小為 10 的並查集

@pytest.fixture
def temp_dir(tmp_path):
    """創建臨時目錄用於存儲可視化文件"""
    return tmp_path

# ====== Binary Tree Tests ======
class TestBinaryTree:
    @pytest.fixture
    def binary_tree_instance(self):
        """建立基本的二元樹測試實例"""
        return BinaryTree(test_mode=True)

    def test_initialization(self, binary_tree_instance):
        """測試二元樹初始化"""
        assert binary_tree_instance.root is None
        assert binary_tree_instance.fig is None
        assert binary_tree_instance.ax is None

    def test_insert(self, binary_tree_instance):
        """測試插入操作"""
        values = [5, 3, 7, 2, 4, 6, 8]
        for value in values:
            binary_tree_instance.insert(value)
        
        # 驗證插入後的樹結構
        root = binary_tree_instance.root
        assert root.val == 5
        assert root.left.val == 3
        assert root.right.val == 7
        assert root.left.left.val == 2
        assert root.left.right.val == 4
        assert root.right.left.val == 6
        assert root.right.right.val == 8

    def test_search(self, binary_tree_instance):
        """測試搜尋操作"""
        values = [5, 3, 7, 2, 4, 6, 8]
        for value in values:
            binary_tree_instance.insert(value)
            
        assert binary_tree_instance.search(5) is True
        assert binary_tree_instance.search(3) is True
        assert binary_tree_instance.search(9) is False

    def test_animation(self, binary_tree_instance):
        """測試動畫功能"""
        # 在測試模式下，動畫相關操作應該被跳過
        values = [5, 3, 7]
        for value in values:
            binary_tree_instance.insert(value)
        
        # 確保不會拋出 Tkinter 相關錯誤
        binary_tree_instance.animate()

    def test_visualization(self, binary_tree_instance, tmp_path):
        """測試視覺化功能"""
        values = [5, 3, 7]
        for value in values:
            binary_tree_instance.insert(value)
            
        if not binary_tree_instance.test_mode:  # 只在非測試模式下執行視覺化
            viz_file = tmp_path / "tree.png"
            binary_tree_instance.visualize(str(viz_file))
            assert viz_file.exists()

# ====== AVL Tree Tests ======
class TestAVLTree:
    @pytest.fixture
    def avl_tree_instance(self):
        """建立基本的 AVL 樹測試實例"""
        return AVLTree(test_mode=True)

    def test_initialization(self, avl_tree_instance):
        """測試 AVL 樹初始化"""
        assert avl_tree_instance.root is None
        assert avl_tree_instance.fig is None
        assert avl_tree_instance.ax is None

    def test_balance(self, avl_tree):
        """測試 AVL 樹的平衡性"""
        # 測試左-左情況
        values = [30, 20, 10]
        for value in values:
            avl_tree.insert(value)
        
        # 驗證樹的結構
        assert avl_tree.root.value == 20
        assert avl_tree.root.left.value == 10
        assert avl_tree.root.right.value == 30

    def test_complex_balance(self):
        """測試複雜的平衡操作"""
        tree = AVLTree(test_mode=True)  # 確保使用測試模式
        values = [10, 20, 30, 40, 50, 25]
        for value in values:
            tree.insert(value)
            
        # 驗證樹的平衡性
        assert tree.root.val == 30
        assert tree.root.left.val == 20
        assert tree.root.right.val == 40
        assert tree.root.left.left.val == 10
        assert tree.root.left.right.val == 25
        assert tree.root.right.right.val == 50

# ====== Heap Tests ======
class TestHeap:
    def test_insertion(self, heap):
        """測試堆的插入操作"""
        values = [4, 8, 2, 6, 1]
        for value in values:
            heap.insert(value)
        
        # 驗證最大值在頂部
        assert heap.heap[0] == 8

    def test_extract_max(self, heap):
        """測試提取最大值"""
        values = [4, 8, 2, 6, 1]
        for value in values:
            heap.insert(value)
        
        # 驗證提取的順序
        assert heap.extract_max() == 8
        assert heap.extract_max() == 6
        assert heap.extract_max() == 4

# ====== Union Find Tests ======
class TestUnionFind:
    def test_union_find(self, union_find):
        """測試並查集的基本操作"""
        # 合併操作
        union_find.union(1, 2)
        union_find.union(2, 3)
        
        # 驗證連通性
        assert union_find.find(1) == union_find.find(3)
        assert union_find.find(1) != union_find.find(4)

# ====== Factory Tests ======
class TestDataStructureFactory:
    def test_factory_creation(self):
        """測試工廠創建各種資料結構"""
        binary_tree = DataStructureFactory.create_structure("binary_tree", test_mode=True)
        avl_tree = DataStructureFactory.create_structure("avl_tree", test_mode=True)
        heap = DataStructureFactory.create_structure("heap", test_mode=True)
        union_find = DataStructureFactory.create_structure("union_find", test_mode=True)
        
        assert isinstance(binary_tree, BinaryTree)
        assert isinstance(avl_tree, AVLTree)
        assert isinstance(heap, Heap)
        assert isinstance(union_find, UnionFind)

    def test_invalid_structure(self):
        """測試創建無效的數據結構"""
        with pytest.raises(ValueError):
            DataStructureFactory.create_structure("invalid_structure") 