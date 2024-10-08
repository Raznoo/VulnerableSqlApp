def apply_many_filters(user_input: str, filters: list) -> str:
    for func in filters:
        user_input = func(user_input)
    return user_input

def cyclic_apply_filters(user_input: str, filters: list) -> str:
    """recursive filter application that will keep filtering until no changes are made"""
    temp = apply_many_filters(user_input, filters)
    if temp == user_input:
        return temp
    else:
        return cyclic_apply_filters(temp, filters)

def crash_filter(user_input: str, filters: list) -> str:
    """if ANY changes were made due to filtering, then crash"""
    temp = user_input
    for func in filters:
        user_input = func(user_input)
        if temp != user_input:
            print(func)
            break
    return temp == user_input

def filter_whitespace(user_input: str) -> str:
    return user_input.replace(" ", "")


def filter_single_quote(user_input: str) -> str:
    return user_input.replace("'", "")


def filter_double_quote(user_input: str) -> str:
    return user_input.replace('"', "")


def filter_select_bad(user_input: str) -> str:
    user_input = user_input.replace("SELECT", "")
    return user_input.replace("select", "")


def filter_union_bad(user_input: str) -> str:
    user_input = user_input.replace("UNION", "")
    return user_input.replace("union", "")


def filter_bar(user_input: str) -> str:
    user_input.replace("|", "")


def filter_dashes(user_input: str) -> str:
    return user_input.replace("-", "")


def lower_transform(user_input: str) -> str:
    return user_input.lower()


def filter_select_good(user_input: str) -> str:
    user_input = lower_transform(user_input)
    return user_input.replace("select", "")


def filter_union_good(user_input: str) -> str:
    user_input = lower_transform(user_input)
    return user_input.replace("union", "")
