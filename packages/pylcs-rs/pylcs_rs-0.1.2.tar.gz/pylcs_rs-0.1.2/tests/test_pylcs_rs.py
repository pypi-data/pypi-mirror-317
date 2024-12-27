import pytest

import pylcs_rs


def test_lcs_sequence():
    assert pylcs_rs.lcs("aaa", "") == 0
    assert pylcs_rs.lcs("", "bbb") == 0
    assert pylcs_rs.lcs("aaa", "bbb") == 0
    assert pylcs_rs.lcs("你好", "中国") == 0
    assert pylcs_rs.lcs_sequence_length("aaa", "aabbbaa") == 3
    assert pylcs_rs.lcs_sequence_length("aaa你好", "你好呀") == 2


def test_lcs_sequence_of_list():
    assert pylcs_rs.lcs_of_list("aaa", ["aabbbaa"] * 10) == [3] * 10
    assert pylcs_rs.lcs_of_list("aaa你好", ["你好呀"] * 10) == [2] * 10
    assert pylcs_rs.lcs_sequence_of_list("aaa", ["aabbbaa"] * 10) == [3] * 10
    assert pylcs_rs.lcs_sequence_of_list("aaa你好", ["你好呀"] * 10) == [2] * 10


def test_lcs_sequence_idx():
    assert pylcs_rs.lcs_sequence_idx("", "bbb") == []
    assert pylcs_rs.lcs_sequence_idx("aaa", "") == [-1, -1, -1]
    assert pylcs_rs.lcs_sequence_idx("aaa", "bbb") == [-1, -1, -1]
    assert pylcs_rs.lcs_sequence_idx("你好", "中国") == [-1, -1]
    res = pylcs_rs.lcs_sequence_idx("aaa", "aabbbaa")
    assert all([x in [0, 1, 5, 6] for x in res]) and res == sorted(res)
    assert pylcs_rs.lcs_sequence_idx("aaa你好", "你好呀") == [-1, -1, -1, 0, 1]


def test_lcs_string():
    assert pylcs_rs.lcs2("aaa", "") == 0
    assert pylcs_rs.lcs2("", "bbb") == 0
    assert pylcs_rs.lcs2("aaa", "bbb") == 0
    assert pylcs_rs.lcs2("你好", "中国") == 0
    assert pylcs_rs.lcs_string_length("aaa", "aabbbaa") == 2
    assert pylcs_rs.lcs_string_length("aaa你好", "好呀你") == 1


def test_lcs_string_of_list():
    assert pylcs_rs.lcs2_of_list("aaa", ["aabbbaa"] * 10) == [2] * 10
    assert pylcs_rs.lcs2_of_list("aaa你好", ["好呀你"] * 10) == [1] * 10
    assert pylcs_rs.lcs_string_of_list("aaa", ["aabbbaa"] * 10) == [2] * 10
    assert pylcs_rs.lcs_string_of_list("aaa你好", ["好呀你"] * 10) == [1] * 10


def test_lcs_string_idx():
    assert pylcs_rs.lcs_string_idx("", "bbb") == []
    assert pylcs_rs.lcs_string_idx("aaa", "") == [-1, -1, -1]
    assert pylcs_rs.lcs_string_idx("aaa", "bbb") == [-1, -1, -1]
    assert pylcs_rs.lcs_string_idx("你好", "中国") == [-1, -1]
    assert pylcs_rs.lcs_string_idx("aaa", "aabbbaa") in (
        [0, 1, -1],
        [-1, 0, 1],
        [5, 6, -1],
        [-1, 5, 6],
    )
    assert pylcs_rs.lcs_string_idx("aaa", "aabbbaaa") == [5, 6, 7]
    assert pylcs_rs.lcs_string_idx("aaa你好", "你好呀") == [-1, -1, -1, 0, 1]
