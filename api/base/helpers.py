def validate_positive_int(data, include_zero=False):
    if include_zero:
        return data.isdigit()

    # Catch any decimals
    if "." in data:
        return False

    try:
        num = int(data)
        return num > 0
    except ValueError:
        return False


def has_keys(keys, d):
    dict_keys = set(d.keys())
    return keys.issubset(dict_keys)
