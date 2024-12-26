import pytest
import numpy as np

from yasiu_vis.ypandas import cluster_keys


@pytest.fixture()
def letters_list():
    data = [chr(i) for i in range(65, 106)]
    return data


@pytest.mark.parametrize("max_keys", list(range(1, 20)))
def test_1_return_size(letters_list, max_keys):
    """Check if return dictionary is withing tolerance and not empty!"""

    ret = cluster_keys(letters_list, max_groups=max_keys)
    assert len(ret) <= max_keys, "Too many groups returned"


@pytest.mark.parametrize("max_keys", list(range(1, 20)))
def test_1b_return_expected_groups(letters_list, max_keys):
    """"""
    ret = cluster_keys(letters_list, max_groups=max_keys)
    assert len(
        ret) == max_keys, f"Expected group size does not match, {len(ret)} != {max_keys}"


@pytest.mark.parametrize("max_keys", list(range(1, 20)))
def test_2_included_in_result(letters_list, max_keys):
    """Check if all keys are in return dict"""

    ret = cluster_keys(letters_list, max_groups=max_keys)
    for letter in letters_list:
        not_found = True
        for key, value in ret.items():
            if letter in value:
                not_found = False
                break

        if not_found:
            raise ValueError(f"Not found key `{letter}` in output dict: {ret}")


@pytest.mark.parametrize("max_keys", list(range(1, 20)))
def test_3_no_duplicates(letters_list, max_keys):
    """Check for any duplicates"""

    ret = cluster_keys(letters_list, max_groups=max_keys)
    for letter in letters_list:
        found = False
        for key, value in ret.items():
            if letter in value:
                if found:
                    raise ValueError(
                        f"Found duplicated key `{letter}` in output dict: {ret}")
                else:
                    found = True


@pytest.mark.parametrize("max_keys", list(range(1, 20)))
def test_4_quality_distribution(letters_list, max_keys):
    """Check if groups are equally distributed"""
    ret = cluster_keys(letters_list, max_groups=max_keys)
    desired = len(letters_list) / max_keys
    low = np.round(desired) - 1
    high = np.round(desired) + 1

    for key, val in ret.items():
        assert low <= len(
            val) <= high, f"Should be withing range {low} <= {len(val)} <= {high}"


@pytest.mark.parametrize("max_keys", list(range(1, 30)))
def test_5_quality_no_empty(letters_list, max_keys):
    ret = cluster_keys(letters_list, max_groups=max_keys)

    for key, val in ret.items():
        # print(len(val))
        assert len(val) > 0, f"Found empty group, {key}: {val}"


@pytest.mark.parametrize("max_keys", list(range(100, 102)))
def test_6_single_element_groups(letters_list, max_keys):
    """Too many centers, more than max_groups"""

    ret = cluster_keys(letters_list, max_groups=max_keys)
    assert len(letters_list) == len(
        ret), "Each keys should have separated group"
