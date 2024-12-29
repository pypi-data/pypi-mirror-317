import pytest
from mathalgo2.algorithm.SearchAlgo import Searching

@pytest.fixture
def search_instance():
    """創建搜尋實例"""
    arr = [1, 3, 5, 7, 9, 11, 13, 15]
    return Searching(arr, test_mode=True)

class TestSearching:
    def test_initialization(self, search_instance):
        """測試初始化"""
        assert len(search_instance.arr) == 8  # 修改為正確的數組長度
        assert search_instance.fig is None  # 測試模式下應為 None
        assert search_instance.ax is None   # 測試模式下應為 None

    def test_binary_search(self, search_instance):
        """測試二分搜尋"""
        # 測試存在的元素
        assert search_instance.search("binary", 7) == 3
        # 測試不存在的元素
        assert search_instance.search("binary", 8) is None

    def test_linear_search(self, search_instance):
        """測試線性搜尋"""
        # 測試存在的元素
        assert search_instance.search("linear", 7) == 3
        # 測試不存在的元素
        assert search_instance.search("linear", 8) is None

    def test_empty_array(self):
        """測試空數組"""
        search = Searching([], test_mode=True)
        assert search.search("binary", 1) is None
        assert search.search("linear", 1) is None

    def test_single_element(self):
        """測試單一元素數組"""
        search = Searching([5], test_mode=True)
        assert search.search("binary", 5) == 0
        assert search.search("linear", 5) == 0

    def test_duplicate_elements(self):
        """測試重複元素"""
        search = Searching([2, 2, 2, 2], test_mode=True)
        # 應該返回第一個匹配的索引
        assert search.search("binary", 2) in [0, 1, 2, 3]
        assert search.search("linear", 2) == 0

    def test_register_algorithm(self, search_instance):
        """測試註冊新算法"""
        def custom_search(self, target):
            return 0 if target in self.arr else None
            
        Searching.register_algorithm("custom", custom_search)
        assert search_instance.search("custom", 7) == 0

    def test_array_not_modified(self, search_instance):
        """測試原數組不被修改"""
        original = search_instance.arr.copy()
        search_instance.search("binary", 7)
        assert search_instance.arr == original

    @pytest.mark.parametrize("algorithm", ["binary", "linear"])
    def test_edge_cases(self, algorithm):
        """測試邊界情況"""
        # 大數組
        large_arr = list(range(1000))  # 減少數組大小以加快測試
        search = Searching(large_arr, test_mode=True)
        assert search.search(algorithm, 999) == 999

    def test_invalid_algorithm(self, search_instance):
        """測試無效的算法名稱"""
        with pytest.raises(ValueError):
            search_instance.search("invalid", 7) 