import random
import string


def generate_password(length=16):

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    all_characters = (
        lowercase +
        uppercase +
        digits +
        symbols
    )

    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(symbols)
    ]

    for _ in range(length - 4):
        password.append(
            random.choice(all_characters)
        )

    random.shuffle(password)

    return "".join(password)