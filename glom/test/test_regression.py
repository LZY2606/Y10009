"""Regression tests for three reported integration issues."""

from glom import glom, Coalesce, T
from glom.matching import Match, Optional
from glom.reduction import Merge, merge


def test_regression_coalesce_default_spec_is_evaluated():
    # default given as a spec (e.g. T[...]) must be evaluated against
    # the target, not returned as a raw spec object
    conf = {'defaults': {'timeout': 30}}
    spec = Coalesce('override.timeout', 'timeout', default=T['defaults']['timeout'])
    assert glom(conf, spec) == 30

    # earlier fallback paths still take precedence when present
    assert glom({'timeout': 5, 'defaults': {'timeout': 30}}, spec) == 5
    assert glom({'override': {'timeout': 1}, 'defaults': {'timeout': 30}}, spec) == 1


def test_regression_match_optional_default_does_not_clobber_present_value():
    spec = Match({'id': int, Optional('nickname', default='匿名'): str})

    # missing key still gets the default
    assert glom({'id': 7}, spec) == {'id': 7, 'nickname': '匿名'}

    # a present, valid value must survive instead of being replaced by the default
    assert glom({'id': 7, 'nickname': '阿元'}, spec) == {'id': 7, 'nickname': '阿元'}


def test_regression_merge_init_accepts_factory_callable():
    class Bag(dict):
        pass

    spec = Merge(init=lambda: Bag())
    result = glom([{'a': 1}, {'b': 2}, {'a': 3}], spec)
    assert result == {'a': 3, 'b': 2}
    assert isinstance(result, Bag)

    # the merge() function entry point shares the same code path
    result = merge([{'x': 1}, {'y': 2}], init=lambda: Bag())
    assert result == {'x': 1, 'y': 2}
    assert isinstance(result, Bag)

    # passing a type directly keeps working as before
    assert glom([{'a': 1}], Merge(init=dict)) == {'a': 1}
