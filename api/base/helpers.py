import django.http as http


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


def create_json_response(success=True, message="", status=200, data=None,
                         empty_data=False):
    payload = {
        "message": message,
        "success": success,
    }

    if data is not None or empty_data:
        payload["data"] = data

    return http.JsonResponse(payload, status=status)