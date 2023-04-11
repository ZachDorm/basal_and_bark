"""Main module."""

import string
import random
import ipyleaflet
from ipyleaflet import GeoData, LayersControl, GeoJSON
import folium
import xyzservices.providers as xyz

import geopandas

def generate_random_string(length):
    """Generates a random string

    Args:
        length (int): length of string of random characters

    Returns:
        string: string of random characters of specified length
    """    
    # letters = string.ascii_lowercase
    # result_str = ''.join(random.choice(letters) for i in range(length))
    # return result_str
    return "test"


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



def add_vector(map, data, **kwargs):
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

    def add_layer_control(self):
        """Add a layer controls to a basal_and_bark map

    Args:
        m (basal_and_bark map): The map to add layer controls to

    Returns:
        basal_and_bark map: The map with layer controls added to it
    """    
        try:
            control = LayersControl(position='topright')
            self.add_control(control)
    
        except:
            return None
        
    def add_shp(self, data, **kwargs):
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
            m = self.add_layer(geo)
            return m
    
        except:
            return None
        

    def add_geojson(self, data, **kwargs):
        try:
            #m = Map(center = [40,-100], zoom = 4, test = "test", scroll_wheel_zoom = True)
            f = geopandas.read_file(data)
            geo = GeoJSON(geo_dataframe=f, name="TN Counties")
            m = self.add_layer(geo)
            return m
    
        except:
            return None
        
    def add_vector(map, data, **kwargs):
        return None  
        

    def add_basemap(self, url = xyz.Esri.WorldImagery.build_url(), basemap="Esri.WorldImagery", **kwargs):
        try:
            basemap = eval(f"xyz.{basemap}")
            url = basemap.build_url()
            attribution = basemap.attribution
            b = self.add_tile_layer(url, name = basemap.name, attribution=attribution, **kwargs)
            return b

        except:
            return None
        
    def add_tile_layer(self, url, name, attribution="", **kwargs):
        """Adds a tile layer to the map.
        Args:
            url (str): The URL of the tile layer.
            name (str): The name of the tile layer.
            attribution (str, optional): The attribution of the tile layer. Defaults to "".
        """
        tile_layer = ipyleaflet.TileLayer(
            url=url,
            name=name,
            attribution=attribution,
            **kwargs
        )
        self.add_layer(tile_layer)




class Map_Folium(folium.Map):
    """create the Map class of basal_and_bark

    Args:
        ipyleaflet (Map): This is an ipyleaflet Map instance upon which basal_and_bark's functionality is built on
    """    
    def __init__(self, location, tiles, zoom_start, **kwargs):
        super().__init__(location=location, tiles=tiles, zoom_start=zoom_start, **kwargs)

    def add_tile_layer(self, url, name, attribution="", **kwargs):
        """Adds a tile layer to the map.
        Args:
            url (str): The URL of the tile layer.
            name (str): The name of the tile layer.
            attribution (str, optional): The attribution of the tile layer. Defaults to "".
        """
        tile_layer = ipyleaflet.TileLayer(
            url=url,
            name=name,
            attribution=attribution,
            **kwargs
        )
        self.add_layer(tile_layer)


    def add_raster(self, url, name="raster", fit_bound = True, **kwargs):
        import httpx
        titiler_endpoint = "https://titiler.xyz"  # Developmentseed Demo endpoint. Please be kind.

        r = httpx.get(f"{titiler_endpoint}/cog/tilejson.json", params = {"url": url,}).json()
        bounds = r["bounds"]

        r = httpx.get(f"{titiler_endpoint}/cog/info", params = {"url": url,}).json()
        tile = r["tiles"][0]
        self.add_tile_layer(url=tile, name=name, **kwargs)

    def add_geojson_folium(map, data, **kwargs):
        try:
            #m = Map(center = [40,-100], zoom = 4, test = "test", scroll_wheel_zoom = True)
            f = geopandas.read_file(data)
            geo = folium.GeoJson(data=data, name="TN Counties")
            m = geo.add_to(map)
            return m
    
        except:
            return None
        

    def add_shp_folium(map, data, **kwargs):
        """Add a shapefile to a map

    Args:
        map (basal_and_bark map): This will be the map that is being worked on
        data (any file type that is accepted by GeoData): Originally intended for vector files

    Returns:
        basal_and_bark map: basal_and_bark map with provided data added to it
    """  
        m = map 
        data=data 
        try:
            #m = Map(center = [40,-100], zoom = 4, test = "test", scroll_wheel_zoom = True)
            f = geopandas.read_file(data)
        
            for _, r in f.iterrows():
        # Without simplifying the representation of each borough,
        # the map might not be displayed
             sim_geo = geopandas.GeoSeries(r['geometry']).simplify(tolerance=0.001)
            geo_j = sim_geo.to_json()
            geo_j = folium.GeoJson(data=geo_j)
            geo_j.add_to(map)
        # geo = GeoData(geo_dataframe=f, name="TN Counties")
        # m = map.add_layer(geo)
            m
    
        except:
            None




    


