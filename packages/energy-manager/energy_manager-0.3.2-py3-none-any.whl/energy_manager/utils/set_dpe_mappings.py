
def set_dpe_mappings():
    """
    Creates and returns a dictionary that maps certain keys to specific
    predefined values representing some DPE (Denoted Parameter Entity)
    mappings.

    Returns:
        dict: A dictionary where each key corresponds to a specific letter
        ('A' to 'F') and each value is a string representing a predefined
        numeric value associated with that letter.
    """
    dpe_mappings = {
        "A": "70",
        "B": "110",
        "C": "180",
        "D": "250",
        "E": "330",
        "F": "420"
    }
    return dpe_mappings
