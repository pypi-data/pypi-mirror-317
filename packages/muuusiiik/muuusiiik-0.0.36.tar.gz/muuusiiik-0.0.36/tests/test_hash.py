import muuusiiik.util as msk
import random
from   pytest import raises


class RandomMock:
    _tb = {1: 1, 2: 2, 3: 3}
    def n():
        rd = random.choice([1,2,3])
        return RandomMock._tb[rd]


# -----------------------------
# TEST CASES FOR HASHER.HASH()
# -----------------------------

def test_hash_string():
    obj    = 'demo text'
    result = msk.hasher.hash(obj)
    assert type(obj) == str
    assert result    == '5c40f9622c9489a25dd71a15374a04fe'


def test_hash_dict():
    obj    = {'type': 'dict', 'value': 'some value'}
    result = msk.hasher.hash(obj)
    assert type(obj) == dict
    assert result    == '2f7a3110878f1c45dcafa9f62b428171'


def test_hash_dict_with_array():
    obj    = {'type': 'dict', 'value': [1, 2, 3, '4']}
    result = msk.hasher.hash(obj)
    assert type(obj) == dict
    assert result    == '84c9de9707639d7a2d28140add70dc97'


def test_hash_dict_with_spaceing_array_should_have_the_same_result_as_normal_array():
    obj    = {'type': 'dict', 'value': [1,   2,     3,     '4']}
    result = msk.hasher.hash(obj)
    assert type(obj) == dict
    assert result    == '84c9de9707639d7a2d28140add70dc97'


def test_hash_for_4_digit():
    obj    = 'demo text'
    result = msk.hasher.hash(obj, n=4)
    assert type(obj)   == str
    assert len(result) == 4
    assert result      == '5c40'


def test_hash_for_n_digits():
    n_digit = RandomMock.n()
    obj     = 'demo text'
    result  = msk.hasher.hash(obj, n=n_digit)
    assert type(obj)   == str
    assert len(result) == n_digit
    assert result      == '5c40f9622c9489a25dd71a15374a04fe'[:n_digit]


def test_exception_attribute_error_when_obj_is_int():
    obj     = 404
    with raises(AttributeError):
        result  = msk.hasher.hash(obj)


def test_exception_attribute_error_when_obj_is_list():
    obj     = [404]
    with raises(AttributeError):
        result  = msk.hasher.hash(obj)


def test_exception_type_error_when_n_is_not_int():
    obj     = 'demo text'
    with raises(TypeError):
        result  = msk.hasher.hash(obj, n=[4])


# ------------------------------------
# TEST CASES FOR HASHER.RANDOM_HASH()
# ------------------------------------

def test_random_hash_return_tuple_of_string():
    prefix = 'this_is_prefix'
    result = msk.hasher.random_hash(prefix)
    assert len(result) == 2


def test_random_hash_return_4_digits():
    prefix = 'this_is_prefix'
    n      = 4
    result = msk.hasher.random_hash(prefix, n=n)
    assert len(result[1]) == n


def test_random_hash_return_prefix_concated_with_two_digit():
    prefix = 'this_is_prefix'
    hash_key, hash_value = msk.hasher.random_hash(prefix)
    assert hash_key[:-2]           == prefix
    assert hash_key[-2:].isdigit() == True


def test_random_hash_also_raise_type_error_if_prefix_is_not_string():
    with raises(TypeError):
        prefix = 404
        msk.hasher.hash(prefix=prefix)


def test_random_hash_also_raise_type_error_if_n_is_not_int():
    with raises(TypeError):
        n = '4'
        msk.hasher.random_hash(n=n)
