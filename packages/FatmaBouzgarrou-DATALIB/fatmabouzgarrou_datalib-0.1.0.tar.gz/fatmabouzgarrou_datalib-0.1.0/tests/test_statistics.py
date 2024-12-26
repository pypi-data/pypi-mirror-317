import pytest
from src.datalib.statistics import calculate_mean, calculate_median, calculate_correlation

def test_calculate_mean():
    data = [1, 2, 3, 4]
    assert calculate_mean(data) == 2.5

def test_calculate_median():
    data = [1, 2, 3, 4]
    assert calculate_median(data) == 2.5

def test_calculate_correlation():
    data1 = [1, 2, 3]
    data2 = [4, 5, 6]
    assert calculate_correlation(data1, data2) == 1.0
