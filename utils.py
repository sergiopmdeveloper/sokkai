def extract_keys_from_key_error(e: KeyError) -> list:
    """
    Extract keys from KeyError

    Parameters
    ----------
    e : KeyError
        Instance of KeyError

    Returns
    -------
    list
        List of missing keys
    """

    error_message = e.args[0]

    start = error_message.find("[") + 1
    end = error_message.find("]")

    return error_message[start:end].replace("'", "").replace(" ", "").split(",")
