def bytes_to_human_readable(byte_value):
    """
    Convert bytes to a human-readable format.

    This function takes a value in bytes and converts it to a string representation
    in the appropriate unit (bytes, KB, MB, GB, TB) with two decimal places.

    Parameters:
        byte_value (int): The number of bytes to convert. Should be a non-negative integer.

    Returns:
        str: The equivalent size in a human-readable format with the appropriate unit.

    Raises:
        ValueError: If byte_value is None or a negative integer.
    """
    # Validate input
    if byte_value is None:
        raise ValueError("Input value cannot be None.")
    if byte_value < 0:
        raise ValueError("Input value cannot be negative.")

    # Define size units
    units = ["bytes", "KB", "MB", "GB", "TB"]
    unit_index = 0

    # If the byte value is 0, return "0 bytes"
    if byte_value == 0:
        return "0 bytes"

    # Convert bytes to the appropriate unit
    while byte_value >= 1024 and unit_index < len(units) - 1:
        byte_value /= 1024.0
        unit_index += 1

    # Round to 2 decimal places and format the output
    return f"{round(byte_value, 2)} {units[unit_index]}"
