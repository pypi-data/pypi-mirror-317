def get_content_to_dict(**kwargs):
    """
    Converts the provided keyword arguments into a dictionary.

    This function takes any number of keyword arguments and returns them as a dictionary.
    It is a simple utility that can be used when you need to dynamically pass a set of
    named arguments and access them as a dictionary.

    Args:
        **kwargs: A variable number of keyword arguments (key-value pairs).

    Returns:
        dict: A dictionary containing all the keyword arguments passed to the function.

    Example:
        >>> get_content_to_dict(name="John", age=30)
        {'name': 'John', 'age': 30}
    """
    return kwargs
