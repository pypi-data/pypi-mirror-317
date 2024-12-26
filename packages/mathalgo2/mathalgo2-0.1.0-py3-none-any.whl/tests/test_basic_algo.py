import pytest
from mathalgo2.basic_algo import BasicAlgorithm

class TestBasicAlgorithm:
    def setup_method(self):
        # 測試用的數據
        self.test_array = [64, 34, 25, 12, 22, 11, 90]
        self.sorted_array = [11, 12, 22, 25, 34, 64, 90]
        self.empty_array = []
        self.single_element = [1]
        self.duplicate_array = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        self.float_array = [3.14, 1.41, 2.71, 0.58]
    
    def test_bubble_sort(self):
        # 測試一般情況
        assert BasicAlgorithm.bubble_sort(self.test_array) == self.sorted_array
        # 測試空數組
        assert BasicAlgorithm.bubble_sort(self.empty_array) == []
        # 測試單一元素
        assert BasicAlgorithm.bubble_sort(self.single_element) == self.single_element
        # 測試浮點數
        assert BasicAlgorithm.bubble_sort(self.float_array) == sorted(self.float_array)

    def test_quick_sort(self):
        # 測試一般情況
        assert BasicAlgorithm.quick_sort(self.test_array) == self.sorted_array
        # 測試空數組
        assert BasicAlgorithm.quick_sort(self.empty_array) == []
        # 測試單一元素
        assert BasicAlgorithm.quick_sort(self.single_element) == self.single_element
        # 測試重複元素
        assert BasicAlgorithm.quick_sort(self.duplicate_array) == sorted(self.duplicate_array)

    def test_merge_sort(self):
        # 測試一般情況
        assert BasicAlgorithm.merge_sort(self.test_array) == self.sorted_array
        # 測試空數組
        assert BasicAlgorithm.merge_sort(self.empty_array) == []
        # 測試單一元素
        assert BasicAlgorithm.merge_sort(self.single_element) == self.single_element
        # 測試浮點數
        assert BasicAlgorithm.merge_sort(self.float_array) == sorted(self.float_array)

    def test_binary_search(self):
        sorted_arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # 測試存在的元素
        assert BasicAlgorithm.binary_search(sorted_arr, 5) == 4
        # 測試不存在的元素
        assert BasicAlgorithm.binary_search(sorted_arr, 11) is None
        # 測試邊界值
        assert BasicAlgorithm.binary_search(sorted_arr, 1) == 0
        assert BasicAlgorithm.binary_search(sorted_arr, 10) == 9

    def test_linear_search(self):
        # 測試存在的元素
        assert BasicAlgorithm.linear_search(self.test_array, 25) == 2
        # 測試不存在的元素
        assert BasicAlgorithm.linear_search(self.test_array, 100) is None
        # 測試空數組
        assert BasicAlgorithm.linear_search(self.empty_array, 1) is None
        # 測試重複元素（應該返回第一個匹配的索引）
        assert BasicAlgorithm.linear_search(self.duplicate_array, 5) == 4

    def test_input_validation(self):
        # 測試無效輸入
        with pytest.raises(ValueError):
            BasicAlgorithm.bubble_sort(None)
        with pytest.raises(ValueError):
            BasicAlgorithm.quick_sort("not a list")
        with pytest.raises(ValueError):
            BasicAlgorithm.merge_sort([1, "2", 3])  # 混合類型 