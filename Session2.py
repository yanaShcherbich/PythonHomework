def get_digits(num: int) -> tuple:
    """Return a tuple of a given integer's digits"""

    tup = tuple(map(int, str(num)))
    return tup

def get_pairs(lst: list) -> list:
    """Return a list of tuples containing pairs of elements"""

    return None if len(lst) == 1 else list(zip(lst, lst[1:]))

def get_shortest_word(s:str)->str:
    """Return the longest word in the given string"""

    l = s.split()
    return max(l, key=len)

def foo(lst: list) -> list:
    """Return a new list of products of all elements except current"""

    prod = 1
    for i in lst:
        prod *= i
    return [0 for i in lst] if prod == 0 else [prod//i for i in lst]

def palindrom(s: str) -> bool:
    """Check whether a string is palindrom or not"""
    return s == s[::-1]

def replace_quotes(s: str) -> str:
    """Replace all " symbols with ' and vise versa"""

    return s.translate(s.maketrans({"'":'"','"': "'"}))

def split(input_string: str, sep=" ") -> list:
    """Function which works the same as str.split method"""

    split_list = []
    index_of_last_sep = input_string.find(sep)
    while index_of_last_sep != -1:
        split_list.append(input_string[:index_of_last_sep])
        input_string = input_string[index_of_last_sep + len(sep):]
        index_of_last_sep = input_string.find(sep)
    split_list.append(input_string)
    return split_list

def split_by_index(s: str, indexes: list]) -> list:
    """Splits the s string by indexes specified in indexes"""

    split_list = []
    start_index = 0
    for index in indexes:
        sub_str = s[start_index : index]
        if sub_str:
            split_list.append(sub_str)
        start_index = index
    sub_str = s[start_index:]
    if sub_str:
        split_list.append(sub_str)
    return split_list
