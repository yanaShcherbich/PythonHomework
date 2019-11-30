import string


def test_1_1(*strings) -> set:
    """receive a changeable number of strings.
    return characters that appear in all strings"""

    set_of_strings = set(*strings)
    result = set(set_of_strings.pop())
    for item in set_of_strings:
        result = result.intersection(item)
    return result


def test_1_2(*strings) -> set:
    """receive a changeable number of strings.
    return characters that appear in at least one string"""

    alphabet_lowercase = set(string.ascii_lowercase)
    set_of_strings = set(*strings)
    result = set()
    for str in set_of_strings:
        result.update(ascii_set.intersection(str))
    return result


def test_1_3(*strings) -> set:
    """receive a changeable number of strings.
    return characters that appear at least in two strings"""

    set_of_strings = set(*strings)
    result = set()
    temp_set = set(set_of_strings.pop())
    for item in set_of_strings:
        result.update(temp_set.intersection(set(item)))
        temp_set = set(item)
    return result


def test_1_4(*strings) -> set:
    """receive a changeable number of strings.
    return characters of alphabet, that were not used in any string"""

    alphabet_lowercase = set(list(string.ascii_lowercase))
    return alphabet.difference(test_1_2(*strings))

def generate_squares(key1: int) -> dict:
    """returns a dictionary of squares

    function takes a number as an argument and returns a dictionary,
    where the key is a number and the value is the square of that number."""

    return {a: a ** 2 for a in range(1, key1 + 1)}

def count_letters(string: str) -> dict:
    """returns a dictionary, that contains letters as keys and a number of their occurrence as values"""

    lst = list(string)
    c = list([lst.count(x) for x in lst])
    return dict(zip(lst, c))

def combine_dicts(*args: dict) -> dict:
    """Combine dictionaries into one dictionary

    function, that receives changeable number of dictionaries (keys - letters, values -
    numbers) and combines them into one dictionary. Dict values should be summarized in case of
    identical keys"""

    final = {}
    for temp_dict in args:
        for temp_key in temp_dict:
            if temp_key in final:
                final[temp_key] += temp_dict[temp_key]
            else:
                final[temp_key] = temp_dict[temp_key]
    return final
