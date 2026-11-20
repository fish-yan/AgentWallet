def format_units(amount: int, decimals: int) -> str:
    if amount < 0:
        raise ValueError("Amount cannot be negative")

    if decimals < 0 or decimals > 255:
        raise ValueError("精度必须在 0 到 255 之间")

    whole, fraction = divmod(amount, 10**decimals)

    if fraction == 0:
        return str(whole)
    
    fraction_text = f"{fraction:0{decimals}d}".rstrip("0")
    return f"{whole}.{fraction_text}"

def format_wei_as_eth(balance_wei: int) -> str:
    return format_units(balance_wei, 18)