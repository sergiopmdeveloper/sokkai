from django import template

register = template.Library()


@register.filter
def multiply(value: int | float, arg: int | float) -> int | float:
    """
    Multiply the value by the argument

    Parameters
    ----------
    value : int | float
        Value to multiply
    arg : int | float
        Argument to multiply the value by

    Returns
    -------
    int | float
        Result of the multiplication
    """

    return round(value * arg, 2)
