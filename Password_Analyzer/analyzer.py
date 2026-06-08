import math


def analyze_password(password):

    length = len(password)

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(not c.isalnum() for c in password)

    score = 0

    if length >= 8:
        score += 1

    if length >= 12:
        score += 1

    if has_upper:
        score += 1

    if has_lower:
        score += 1

    if has_digit:
        score += 1

    if has_symbol:
        score += 1

    if score <= 2:
        strength = "WEAK"
    elif score <= 4:
        strength = "MEDIUM"
    elif score <= 5:
        strength = "STRONG"
    else:
        strength = "VERY STRONG"

    charset = 0

    if has_lower:
        charset += 26

    if has_upper:
        charset += 26

    if has_digit:
        charset += 10

    if has_symbol:
        charset += 33

    combinations = charset ** length if charset > 0 else 0

    brute_seconds = combinations / 1_000_000_000 if combinations > 0 else 0

    brute_years = brute_seconds / (
        60 * 60 * 24 * 365
    )

    simple_hash = sum(ord(c) for c in password) % 101

    return {
        "length": length,
        "strength": strength,
        "upper": has_upper,
        "lower": has_lower,
        "digit": has_digit,
        "symbol": has_symbol,
        "charset": charset,
        "combinations": combinations,
        "years": brute_years,
        "hash": simple_hash
    }