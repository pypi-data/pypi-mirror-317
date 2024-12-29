import pytest
from mathalgo2.algorithm.SortAlgo import Sorting

class TestSorting:
    @pytest.fixture
    def sorting_instance(self):
        """建立基本的排序測試實例"""
        arr = [64, 34, 25, 12, 22, 11, 90]
        return Sorting(arr, animation_speed=0)  # 設置動畫速度為0以加快測試

    def test_initialization(self, sorting_instance):
        """測試排序類初始化"""
        assert len(sorting_instance.arr) == 7
        assert sorting_instance.fig is None
        assert sorting_instance.ax is None
        assert sorting_instance.animation_speed == 0

    def test_bubble_sort(self, sorting_instance):
        """測試氣泡排序"""
        # 升序排序
        result = sorting_instance.bubble_sort()
        assert result == [11, 12, 22, 25, 34, 64, 90]
        
        # 降序排序
        result = sorting_instance.bubble_sort(reverse=True)
        assert result == [90, 64, 34, 25, 22, 12, 11]

    def test_quick_sort(self, sorting_instance):
        """測試快速排序"""
        # 升序排序
        result = sorting_instance.quick_sort()
        assert result == [11, 12, 22, 25, 34, 64, 90]
        
        # 降序排序
        result = sorting_instance.quick_sort(reverse=True)
        assert result == [90, 64, 34, 25, 22, 12, 11]

    def test_insertion_sort(self, sorting_instance):
        """測試插入排序"""
        # 升序排序
        result = sorting_instance.insertion_sort()
        assert result == [11, 12, 22, 25, 34, 64, 90]
        
        # 降序排序
        result = sorting_instance.insertion_sort(reverse=True)
        assert result == [90, 64, 34, 25, 22, 12, 11]

    def test_merge_sort(self, sorting_instance):
        """測試合併排序"""
        # 升序排序
        result = sorting_instance.merge_sort()
        assert result == [11, 12, 22, 25, 34, 64, 90]
        
        # 降序排序
        result = sorting_instance.merge_sort(reverse=True)
        assert result == [90, 64, 34, 25, 22, 12, 11]

    def test_empty_array(self):
        """測試空數組"""
        sorting = Sorting([], animation_speed=0)
        assert sorting.bubble_sort() == []
        assert sorting.quick_sort() == []
        assert sorting.insertion_sort() == []
        assert sorting.merge_sort() == []

    def test_single_element(self):
        """測試單一元素數組"""
        sorting = Sorting([1], animation_speed=0)
        assert sorting.bubble_sort() == [1]
        assert sorting.quick_sort() == [1]
        assert sorting.insertion_sort() == [1]
        assert sorting.merge_sort() == [1]

    def test_duplicate_elements(self):
        """測試重複元素"""
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        sorting = Sorting(arr, animation_speed=0)
        expected_asc = [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
        expected_desc = [9, 6, 5, 5, 5, 4, 3, 3, 2, 1, 1]
        
        assert sorting.bubble_sort() == expected_asc
        assert sorting.bubble_sort(reverse=True) == expected_desc
        assert sorting.quick_sort() == expected_asc
        assert sorting.quick_sort(reverse=True) == expected_desc
        assert sorting.insertion_sort() == expected_asc
        assert sorting.insertion_sort(reverse=True) == expected_desc
        assert sorting.merge_sort() == expected_asc
        assert sorting.merge_sort(reverse=True) == expected_desc

    def test_already_sorted(self):
        """測試已排序的數組"""
        arr = [1, 2, 3, 4, 5]
        sorting = Sorting(arr, animation_speed=0)
        assert sorting.bubble_sort() == [1, 2, 3, 4, 5]
        assert sorting.quick_sort() == [1, 2, 3, 4, 5]
        assert sorting.insertion_sort() == [1, 2, 3, 4, 5]
        assert sorting.merge_sort() == [1, 2, 3, 4, 5]

    def test_reverse_sorted(self):
        """測試反向排序的數組"""
        arr = [5, 4, 3, 2, 1]
        sorting = Sorting(arr, animation_speed=0)
        assert sorting.bubble_sort() == [1, 2, 3, 4, 5]
        assert sorting.quick_sort() == [1, 2, 3, 4, 5]
        assert sorting.insertion_sort() == [1, 2, 3, 4, 5]
        assert sorting.merge_sort() == [1, 2, 3, 4, 5] 