"""Main module."""

import string
import random
import ipyleaflet
from ipyleaflet import GeoData, LayersControl

import geopandas

def generate_random_string(length):
    """Generates a random string

    Args:
        length (int): length of string of random characters

    Returns:
        string: string of random characters of specified length
    """    
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


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

# def add_search_control():
#     marker = Marker(icon=AwesomeIcon(name="check", marker_color='green', icon_color='darkgreen'))

#     this.add_control(SearchControl(
#     position="topleft",
#     url='https://nominatim.openstreetmap.org/search?format=json&q={s}',
#     zoom=5,
#     marker=marker
#     ))

def add_layer_control(m):
    """Add a layer controls to a basal_and_bark map

    Args:
        m (basal_and_bark map): The map to add layer controls to

    Returns:
        basal_and_bark map: The map with layer controls added to it
    """    
    try:
        control = LayersControl(position='topright')
        m.add_control(control)
        return m
    
    except:
        return None

def view_data(data, **kwargs):
    """View and explore data without adding it to a map

    Args:
        data (shp file): spatial data to be viewed

    Returns:
        ipyleaflet map: A map viewport for viewing and exploring data
    """    
    try:
        add_gdf = geopandas.read_file(data)
        return add_gdf.explore()
    
    except:
        return None
    

def add_data(map, data, **kwargs):
    """Add a shapefile to a map

    Args:
        map (basal_and_bark map): This will be the map that is being worked on
        data (any file type that is accepted by GeoData): Originally intended for vector files

    Returns:
        basal_and_bark map: basal_and_bark map with provided data added to it
    """    
    try:
        #m = Map(center = [40,-100], zoom = 4, test = "test", scroll_wheel_zoom = True)
        f = geopandas.read_file(data)
        geo = GeoData(geo_dataframe=f, name="TN Counties")
        m = map.add_layer(geo)
        return m
    
    except:
        return None
    


def summarize_data(data, type="mean"):
    """summarize a list of numbers using the specified method

    Args:
        data (list of int): list of numbers to be summarized
        type (str, optional): Method for summarization. Defaults to "mean".

    Returns:
        int: summary statistic
    """
    if type == "max":
        return max(data)
    elif type == "min":
        return min(data)
    elif type == "sum":
        return sum(data)
    
    return sum(data)/len(data)


class Map(ipyleaflet.Map):
    """create the Map class of basal_and_bark

    Args:
        ipyleaflet (Map): This is an ipyleaflet Map instance upon which basal_and_bark's functionality is built on
    """    
    def __init__(self, center, zoom, **kwargs):
        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll+wheel_zoom"]=True
        super().__init__(center = center, zoom = zoom, **kwargs)