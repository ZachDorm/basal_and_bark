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

def add_search_control():
    marker = Marker(icon=AwesomeIcon(name="check", marker_color='green', icon_color='darkgreen'))

    this.add_control(SearchControl(
    position="topleft",
    url='https://nominatim.openstreetmap.org/search?format=json&q={s}',
    zoom=5,
    marker=marker
    ))


class Map(ipyleaflet.Map):
    def __init__(self, center, zoom, **kwargs):
        if("scroll_wheel_zoom" not in **kwargs):
            kwargs["scroll+wheel_zoom"]=True
        super().__init__(center = center, zoom = zoom, **kwargs)