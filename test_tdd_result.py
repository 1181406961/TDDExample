import pytest

'''
需求分析
-l -p 8080 -d /usr/logs
f   f v
happy path:
    -l true
    -d 8080
    -p /usr/logs
sad path:
    -l t
    -p 8080 9090
    -p 
    -d /usr/logs /usr
    -d 
default path:
    -l false
    -d ''
    -p 0
'''


class ParamsError(Exception):
    def __init__(self, flag):
        self.flag = flag


def parser_args(options, params):
    result = {}
    for key in options.keys():
        value = parse(key, options, params)
        result[key] = value
    return result


def parse(key, options, params):
    flag = f'-{key}'
    parse_func = {
        bool: parse_bool,
        int: parse_int,
        str: parse_str
    }.get(options[key])
    return parse_func(flag, params)


def parse_str(flag, params):
    exists = flag in params
    if exists:
        value = get_flag_value(flag, params)
        not_allow_next_item_is_value(flag, params, value)
        return value
    return ''


def not_allow_next_item_is_value(flag, params, param_item):
    item_index = params.index(param_item)
    if item_index + 1 < len(params) and \
            not params[item_index + 1].startswith('-'):
        raise ParamsError(flag=flag)


def get_flag_value(flag, params):
    flag_index = params.index(flag)
    value = params[flag_index + 1]
    return value


def parse_int(flag, params):
    return int(get_flag_value(flag, params))


def parse_bool(flag, params):
    exists = flag in params
    if exists:
        not_allow_next_item_is_value(flag, params, flag)
    return exists


# 大的测试逐一击破
def test_parser():
    options = {
        'l': bool,
        'p': int,
        'd': str
    }
    args = parser_args(options, ['-l', '-p', '8080', '-d', '/usr/logs'])
    assert args['l'] is True
    assert args['p'] == 8080
    assert args['d'] == '/usr/logs'


def test_parse_l():
    options = {
        'l': bool
    }
    args = parser_args(options, ['-l'])
    assert args['l'] is True


def test_parse_p():
    options = {
        'p': int
    }
    args = parser_args(options, ['-p', '8080'])
    assert args['p'] == 8080


def test_parse_d():
    options = {
        'd': str
    }
    args = parser_args(options, ['-d', '/usr/logs'])
    assert args['d'] == '/usr/logs'


def test_parse_empty_l():
    options = {
        'l': bool
    }
    args = parser_args(options, [])
    assert args['l'] is False


def test_parse_multi_l_value():
    options = {
        'l': bool
    }
    with pytest.raises(ParamsError) as e:
        parser_args(options, ['-l', 'abc'])
    assert e.value.flag == '-l'


def test_parse_empty_d():
    options = {
        'd': str
    }
    args = parser_args(options, [])
    assert args['d'] == ''


def test_parse_multi_d_value():
    options = {
        'd': str
    }
    with pytest.raises(ParamsError) as e:
        parser_args(options, ['-d', '/usr/logs', '/etc'])
    assert e.value.flag == '-d'
