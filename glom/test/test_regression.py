from glom import Coalesce, Match, Merge, T, glom, merge
from glom.matching import Optional


def test_regression_coalesce_evaluates_target_referencing_default():
    conf = {'defaults': {'timeout': 30}}

    result = glom(conf, Coalesce('override.timeout', 'timeout',
                                 default=T['defaults']['timeout']))

    assert result == 30


def test_regression_match_optional_default_does_not_replace_present_value():
    spec = Match({'id': int, Optional('nickname', default='匿名'): str})

    result = glom({'id': 7, 'nickname': '阿元'}, spec)

    assert result == {'id': 7, 'nickname': '阿元'}


def test_regression_merge_factory_init_result_uses_factory_instance():
    class Bag(dict):
        pass

    target = [{'a': 1}, {'b': 2}]
    expected = Bag({'a': 1, 'b': 2})

    result = glom(target, Merge(init=lambda: Bag()))

    assert result == expected
    assert type(result) is Bag

    result = merge(target, init=lambda: Bag())

    assert result == expected
    assert type(result) is Bag
