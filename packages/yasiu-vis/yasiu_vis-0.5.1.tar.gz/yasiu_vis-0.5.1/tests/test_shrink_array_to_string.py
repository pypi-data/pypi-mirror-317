import numpy as np
import pytest

from yasiu_vis.ypandas import shrink_array_to_string


def test_1():
    ret = shrink_array_to_string([1, 2, 3, 4, 5])
    assert "[1,2,3,4,5]" == ret


data = [
    np.random.randint(0, 10, size)
    for i in range(20)
    for size in [5, 7, 9, 20]
]


@pytest.mark.parametrize("arr", data)
def test_2_generator(arr):
    max_size = 20
    ret = shrink_array_to_string(arr, max_size=max_size)
    assert len(
        ret) <= max_size, f"String must be shorter than {max_size}, but got {len(ret)}"


data_string = [
    ['a' * i, 'b' * i, 'c' * i]
    for i in range(1, 9)

]


@pytest.mark.parametrize("arr", data_string)
def test_3_string(arr):
    """Assert correct string size concatenation"""
    max_size = 24
    ret = shrink_array_to_string(arr, max_size=max_size)
    assert len(
        ret) <= max_size, f"String must be shorter than {max_size}, but got {len(ret)}"


data_string_too_long = [
    ['a' * i, 'b' * i, 'c' * i]
    for i in range(9, 12)

]


@pytest.mark.parametrize("arr", data_string_too_long)
def test_4_exception(arr):
    """Assert raise error if too long"""
    max_size = 20
    with pytest.raises(ValueError):
        shrink_array_to_string(arr, max_size=max_size)

    # assert len(ret) <= max_size, f"String must be shorter than {max_size}, but got {len(ret)}"


def test_5_problematic_array():
    # arr = np.array([0.00010120244818889734, 0.09788665233484561], dtype=float)
    arr = np.array(
        [0.003106288547295888, 0.0065768950032527584, 0.006818893006837579, 0.013399727690859953,
         0.016596271276446917, 0.01750872623148836, 0.02424437623122755, 0.027997778586513755,
         0.028663730824587175, 0.029011382820134934, 0.034152959789848, 0.04140316248185494,
         0.042961810009989554, 0.046594003032639386, 0.04688136016247346, 0.07042316938808879,
         0.07214030791311332, 0.07358005047484595, 0.08559379006548273, 0.08748798926270451,
         0.08935974852218753, 0.090136302628532], dtype=float)
    ret = shrink_array_to_string(arr)
    print(ret)
    print(len(ret))
