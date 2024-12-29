import pytest
from mathalgo2.algorithm.StrAlgo import StrAlgo

class TestStrAlgo:
    @pytest.fixture
    def str_algo_instance(self):
        """建立基本的 StrAlgo 測試實例"""
        text = "ABABDABACDABABCABAB"
        pattern = "ABABC"
        return StrAlgo(text, pattern, test_mode=True)

    def test_initialization(self, str_algo_instance):
        """測試 StrAlgo 初始化"""
        assert str_algo_instance.text == "ABABDABACDABABCABAB"
        assert str_algo_instance.pattern == "ABABC"
        assert str_algo_instance.fig is None
        assert str_algo_instance.ax is None

    def test_kmp_search(self, str_algo_instance):
        """測試 KMP 搜尋演算法"""
        matches = str_algo_instance.kmp_search()
        assert isinstance(matches, list)
        assert matches == [10]  # ABABC 在文本中的位置

    def test_rabin_karp_search(self, str_algo_instance):
        """測試 Rabin-Karp 搜尋演算法"""
        matches = str_algo_instance.rabin_karp_search()
        assert isinstance(matches, list)
        assert matches == [10]  # ABABC 在文本中的位置

    def test_empty_pattern(self):
        """測試空模式字串的情況"""
        with pytest.raises(ValueError):
            StrAlgo("test text", "", test_mode=True)

    def test_pattern_longer_than_text(self):
        """測試模式字串長度大於文本的情況"""
        text = "short"
        pattern = "longer pattern"
        algo = StrAlgo(text, pattern, test_mode=True)
        assert len(algo.kmp_search()) == 0
        assert len(algo.rabin_karp_search()) == 0

    def test_multiple_matches(self):
        """測試多重匹配的情況"""
        text = "ABABABABAB"
        pattern = "ABA"
        algo = StrAlgo(text, pattern, test_mode=True)
        kmp_matches = algo.kmp_search()
        rk_matches = algo.rabin_karp_search()
        
        assert len(kmp_matches) == 4  # 應該找到4個匹配
        assert kmp_matches == [0, 2, 4, 6]  # ABA 在 ABABABABAB 中出現的位置
        assert rk_matches == kmp_matches 