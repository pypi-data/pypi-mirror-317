import pytest
from mathalgo2.algorithm.string.RabinKarp import RabinKarp

class TestRabinKarp:
    def test_initialization(self):
        """測試初始化"""
        # 正常初始化
        rk = RabinKarp("test")
        assert rk.pattern == "test"
        assert rk.pattern_length == 4
        assert rk.d == 256
        assert rk.q == 101

        # 空模式字串
        with pytest.raises(ValueError):
            RabinKarp("")

    def test_basic_search(self):
        """測試基本的搜尋功能"""
        # 簡單匹配
        rk = RabinKarp("test")
        text = "this is a test string"
        matches = rk.search(text)
        assert matches == [10]

        # 多重匹配
        rk = RabinKarp("aa")
        text = "aaa"
        matches = rk.search(text)
        assert matches == [0, 1]

    def test_no_match(self):
        """測試無匹配的情況"""
        rk = RabinKarp("xyz")
        text = "this is a test string"
        matches = rk.search(text)
        assert matches == []

    def test_pattern_longer_than_text(self):
        """測試模式字串長於文本的情況"""
        rk = RabinKarp("testing")
        text = "test"
        matches = rk.search(text)
        assert matches == []

    def test_special_characters(self):
        """測試特殊字符"""
        # 包含空格
        rk = RabinKarp("ing ")
        text = "testing cat"  # 使用一個確定只有一個 "ing " 的文本
        matches = rk.search(text)
        assert matches == [4]  # "testing" 後面的空格位置

        # 包含標點符號
        rk = RabinKarp("test!")
        text = "this is a test! string"
        matches = rk.search(text)
        assert matches == [10]

    def test_overlapping_patterns(self):
        """測試重疊的模式"""
        rk = RabinKarp("aaa")
        text = "aaaa"
        matches = rk.search(text)
        assert matches == [0, 1]

    def test_case_sensitivity(self):
        """測試大小寫敏感性"""
        rk = RabinKarp("Test")
        text = "this is a test string"
        matches = rk.search(text)
        assert matches == []  # 不應匹配小寫的 "test"

    def test_empty_text(self):
        """測試空文本"""
        rk = RabinKarp("test")
        matches = rk.search("")
        assert matches == []

    def test_single_character(self):
        """測試單字符模式和文本"""
        # 單字符模式
        rk = RabinKarp("a")
        text = "banana"
        matches = rk.search(text)
        assert matches == [1, 3, 5]

        # 單字符文本
        rk = RabinKarp("ab")
        text = "a"
        matches = rk.search(text)
        assert matches == []

    def test_unicode_characters(self):
        """測試Unicode字符"""
        # 中文字符
        rk = RabinKarp("測試")
        text = "這是一個測試字串"
        matches = rk.search(text)
        assert matches == [4]

        # 表情符號
        rk = RabinKarp("😊")
        text = "Hello 😊 World"
        matches = rk.search(text)
        assert matches == [6] 