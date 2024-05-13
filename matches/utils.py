def generate_match_filters(
    date: str,
    league: str,
) -> dict[str, str]:
    """
    Generate match filters.

    Parameters
    ----------
    request : HttpRequest
        The request object.

    Returns
    -------
    dict[str, str]
        The match filters.
    """

    filters = {}

    filters["date"] = date

    if league != "All leagues":
        filters["league"] = league

    return filters
