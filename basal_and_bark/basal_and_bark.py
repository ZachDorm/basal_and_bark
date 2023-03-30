"""Main module."""

import string
import random
import ipyleaflet

def generate_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
    """_summary_
    """

def generate_lucky_number(length=1):
    """Generates a lucky number of given length

    Args:
        length (int, optional): _description_. Defaults to 1.

    Returns:
        str: the generated string
    """    
    numbers = ['1','2','3','4','5','6','7','8','9','0']
    result_str = ''.join(random.choice(numbers) for i in range(length))
    return result_str


class Map(ipyleaflet.Map):
    def __init__(self, center, zoom, **kwargs):
        super().__init__(center = center, zoom = zoom, **kwargs)