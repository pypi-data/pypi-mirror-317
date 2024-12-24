def get_json(response):
    """
    Get json from response

    :param response: urllib.response
    :return: JSON to PON (Python Object Notation)
    """
    return json.loads(response.read().decode('utf-8'))