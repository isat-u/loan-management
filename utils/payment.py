import random
import string


def random_string_digits(string_length=8):
    """Generate a random string of letters and digits """
    alphanumeric = string.ascii_letters + string.digits
    return ''.join(random.choice(alphanumeric) for i in range(string_length))
