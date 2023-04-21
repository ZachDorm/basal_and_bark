"""Main module."""

import string
import random
# import ipyleaflet
# from ipyleaflet import GeoData, LayersControl, GeoJSON
import folium
from folium import TileLayer
import xyzservices.providers as xyz

import geopandas
from geopandas import GeoDataFrame, GeoSeries

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



class Map_Folium(folium.Map):
    """create the Map_Folium class of basal_and_bark

    Args:
        folium (Map): This is a folium Map instance upon which basal_and_bark's functionality is built on
    """    
    def __init__(self, location, tiles, zoom_start, **kwargs):
        super().__init__(location=location, tiles=tiles, zoom_start=zoom_start, **kwargs)

    def add_tile_layer_folium(self, url = xyz.Esri.WorldImagery.build_url(), name="", attribution="Esri.WorldImagery", **kwargs):
        """Adds a tile layer to the map.
        Args:
            url (str): The URL of the tile layer.
            name (str): The name of the tile layer.
            attribution (str, optional): The attribution of the tile layer. Defaults to "".
        """
        tile_layer = folium.TileLayer(
            tiles=url,
            attr=attribution,
            name=name,
            **kwargs
        )
        tile_layer.add_to(self)

    def add_basemap(self, url = xyz.Esri.WorldImagery.build_url(), basemap="Esri.WorldImagery", **kwargs):
        """Add a basemap from xyz.services

        Args:
            url (string, optional: URL to xyz.services map. Defaults to xyz.Esri.WorldImagery.build_url().
            basemap (str, optional): Name of the basemap on xyz.services. Defaults to "Esri.WorldImagery".

        Raises:
            ValueError: If basemap does not exist.

        Returns:
            basal_and_bark map_folium: basal_and_bark map_folium with new basemap
        """        
        try:
            basemap = eval(f"xyz.{basemap}")
            url = basemap.build_url()
            attribution = basemap.attribution
            b = self.add_tile_layer_folium(url, name = basemap.name, attribution=attribution, **kwargs)
            return b

        except:
            raise ValueError(f"Basemap '{basemap}' not found.")


    def add_raster(self, url, name="raster", fit_bound = True, **kwargs):
        """Adds a raster to the basal_and_bark map_folium

        Args:
            url (string): URL to raster you want to use.
            name (str, optional): Name of the raster. Defaults to "raster".
            fit_bound (bool, optional): Whether the bound of the map should be fit to the raster. Defaults to True.
        """        
        import httpx
        titiler_endpoint = "https://titiler.xyz"  # Developmentseed Demo endpoint. Please be kind

        r = httpx.get(f"{titiler_endpoint}/cog/tilejson.json", params = {"url": url,}).json()
        bounds = r["bounds"]

        r = httpx.get(f"{titiler_endpoint}/cog/info", params = {"url": url,}).json()
        tile = r["tiles"][0]
        self.add_tile_layer(url=tile, name=name, **kwargs)

    def add_geojson_folium(self, data, **kwargs):
        """Add GeoJSON to a map_folium

        Args:
            data (GeoJSON file): GeoJSON

        Returns:
            basal_and_bark map_folium: basal_and_bark map_folium with provided data added to it
        """        
        # try:
        f = geopandas.read_file(data)
        geo = folium.GeoJson(data=data, name="TN Counties")
        m = geo.add_to(self)
        return m
    
        # except:
        #     return None
        

    def add_shp_folium(self, data, **kwargs):
        """Add a shapefile to a map_folium

    Args:
        map_folium (basal_and_bark map_folium): This will be the map that is being worked on
        data (any file type that is accepted by GeoData): Originally intended for vector files

    Returns:
        basal_and_bark map_folium: basal_and_bark map_folium with provided data added to it
    """  
        data=data 
        f = geopandas.read_file(data)
        geo = f["geometry"].simplify(tolerance=0.001)
        json = geo.to_json()
        geo_j = folium.GeoJson(data=json)
        geo_j.add_to(self)
        
        #     for _, r in f.iterrows():
        # # Without simplifying the representation of each borough,
        # # the map might not be displayed
        #      sim_geo = geopandas.GeoSeries(r['geometry'])#.simplify(tolerance=0.001)
        #     geo_j = sim_geo.to_json()
        #     geo_j = folium.GeoJson(data=geo_j)
        #     geo_j.add_to(self)
        # # geo = GeoData(geo_dataframe=f, name="TN Counties")
        # # m = map.add_layer(geo)
        self



    def add_vector_folium(self, data, **kwargs):
        """Accepts a file. Checks if it is a geopandas supported format. If not, then except silently.

        Args:
            data (vector data): Geopandas supported vector format.

        Returns:
            basal_and_bark map_folium: basal_and_bark map_folium with the vector data added.
        """        
        count = 0

        try:
            self.add_shp_folium(data)
        except:
            count = count +1
            try:
                self.add_geojson_folium(data)
            except:
                count = count +1
        
                try:
                    json = data.to_json()
                    geo_j = folium.GeoJson(data=json)
                    geo_j.add_to(self)
                except:
                    count = count +1

        # if(count==3):
                    return "Not a supported file type"
        # else:
        #     pass




    


