def clean_and_convert(value):
    if not value:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return float(value.replace(",", ""))

# function that will convert the market cap value to a float
def convert_market_cap(market_cap_str):
    """
    Convert a market cap string to its numeric representation.

    :param market_cap_str: String representing the market cap, e.g., "116.624M", "2.5B", "1T".
    :return: Numeric representation of the market cap.
    """
    try:
        # Convert based on suffix
        if "M" in market_cap_str:
            return round(float(market_cap_str.replace("M", "").replace(",", "")) * 1e6, 2)
        elif "B" in market_cap_str:
            return round(float(market_cap_str.replace("B", "").replace(",", "")) * 1e9, 2)
        elif "T" in market_cap_str:
            return round(float(market_cap_str.replace("T", "").replace(",", "")) * 1e12, 2)
        else:
            # If no suffix, assume the number is already in its numeric representation
            return round(float(market_cap_str.replace(",", "")), 2)
    except ValueError:
        # Handle any error in conversion
        return None
