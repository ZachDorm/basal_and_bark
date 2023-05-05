"""Main module."""

import string
import random
import ipyleaflet
from ipyleaflet import GeoData, LayersControl, GeoJSON
# import folium
# from folium import TileLayer
import xyzservices.providers as xyz
import ipywidgets as widgets
from ipyleaflet import WidgetControl
import pandas
import geopandas
from geopandas import GeoDataFrame, GeoSeries
import requests


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
        # try:
            #m = Map(center = [40,-100], zoom = 4, test = "test", scroll_wheel_zoom = True)
        f = geopandas.read_file(data)
        geo = GeoData(geo_dataframe=f, name="TN Counties")
        self.add_layer(geo)
        return self
    
        # except:
        #     return None
        

    def add_geojson(self, data, **kwargs):
        try:
            #m = Map(center = [40,-100], zoom = 4, test = "test", scroll_wheel_zoom = True)
            self.add_shp(data)
            # f = geopandas.read_file(data)
            # geo = GeoData(geo_dataframe=f, name="TN Counties")
            # self.add_layer(geo)
            # return self
    
        except:
            return None
        
    def add_vector(self, data, **kwargs):
        """Accepts a file. Checks if it is a geopandas supported format. If not, then except silently.

        Args:
            data (vector data): Geopandas supported vector format.

        Returns:
            basal_and_bark map: basal_and_bark map with the vector data added.
        """     

        try:
            self.add_shp(data)
        except:

            try:
                geo = GeoData(geo_dataframe=data, name="New Data")
                self.add_layer(geo)
            except:

                try:
                    geo = GeoSeries(data=data, name="New Data")
                    self.add_layer(geo)
                except:
        
                    try:
                        geo = GeoDataFrame(data=data, name="New Data")
                        self.add_layer(geo)
                    except:

                        return "Not a supported file type"
                    

    def add_basemap(self, url = xyz.Esri.WorldImagery.build_url(), basemap="Esri.WorldImagery", **kwargs):
        """Add a basemap from xyz.services

        Args:
            url (string, optional: URL to xyz.services map. Defaults to xyz.Esri.WorldImagery.build_url().
            basemap (str, optional): Name of the basemap on xyz.services. Defaults to "Esri.WorldImagery".

        Raises:
            ValueError: If basemap does not exist.

        Returns:
            basal_and_bark map: basal_and_bark map with new basemap
        """        
        try:
            basemap = eval(f"xyz.{basemap}")
            url = basemap.build_url()
            attribution = basemap.attribution
            b = self.add_tile_layer(url, name = basemap.name, attribution=attribution, **kwargs)
            return b

        except:
            raise ValueError(f"Basemap '{basemap}' not found.")
        
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
        """Adds a raster to the basal_and_bark map

        Args:
            url (string): URL to raster you want to use.
            name (str, optional): Name of the raster. Defaults to "raster".
            fit_bound (bool, optional): Whether the bound of the map should be fit to the raster. Defaults to True.
        """        
        import httpx
        titiler_endpoint = "https://titiler.xyz"  # Developmentseed Demo endpoint. Please be kind

        r = httpx.get(f"{titiler_endpoint}/cog/info", params = {"url": url,}).json()
        bounds = r["bounds"]

        r = httpx.get(f"{titiler_endpoint}/cog/tilejson.json", params = {"url": url,}).json()
        tile = r["tiles"][0]

        bbox = [[bounds[1], bounds[0]], [bounds[3], bounds[2]]]
        self.fit_bounds(bbox)
        self.add_tile_layer(url=tile, name=name, **kwargs)

    def add_image(self, url, **kwargs):
        """Add a static image to the bottom right corner of a basal_and_bark map.

        Args:
            url (String): The url where the image to add is located.
        """        
        # import ipywidgets as widgets
        # from ipyleaflet import WidgetControl

        output_widget = widgets.Output(layout={'border': '1px solid black'})
        output_widget.clear_output()
        output_control = WidgetControl(widget=output_widget, position='bottomright')
        self.add_control(output_control)
        logo = widgets.HTML(
            value='<img src="https://wvstateparks.com/wp-content/uploads/2017/03/Ascend-WV-Brand-Photo-Coopers-Rock-State-Forest-Morgantown-scaled.jpg" width="200" height="200">'
            )
        with output_widget:
            output_widget.display(logo)

    def add_interactive_basemap(self, **kwargs):
        """Add a dropdown ipywidget that provides options for a basemap from xyz.services

        Args:
            self: basal_and_bark map: Map the user wants to add the interactive basemap to.

        Returns:
            basal_and_bark map: basal_and_bark map with new basemap, function is observing for change in value
        """        
        output_widget = widgets.Output(layout={'border': '1px solid black'})
        output_widget.clear_output()
        basemap_ctrl = WidgetControl(widget=output_widget, position='bottomright')
        self.add_control(basemap_ctrl)

        dropdown = widgets.Dropdown(
            options = ["Topo", "ShadeRelief", "Gray"], 
            value=None,
            description='Basemap',
            )

        close_button = widgets.ToggleButton(
            value=True,
            tooltip="Open or close basemap selector",
            icon="desktop",
            button_style="primary",
            #layout=widgets.Layout(height="28px", width="28px", padding=padding),
        )
        close_button

        h = widgets.VBox([close_button, dropdown])


        with output_widget:
            # if basemap_ctrl not in leaflet_map.controls:
            output_widget.display(h)

        def change_basemap(change):
            if change["new"] == "Topo":
                self.add_basemap(basemap= "Esri.WorldTopoMap")
            if change["new"] == "ShadeRelief":
                self.add_basemap(basemap= "Esri.WorldShadedRelief")
            if change["new"] == "Gray":
                self.add_basemap(basemap= "Esri.WorldGrayCanvas")
        
        dropdown.observe(change_basemap, "value")

        def close_basemap(change):
    
            if change["new"] == True:
                output_widget.clear_output()
                with output_widget:
            # if basemap_ctrl not in leaflet_map.controls:
                    output_widget.display(h)
            else:
                output_widget.clear_output()
                with output_widget:
            # if basemap_ctrl not in leaflet_map.controls:
                    output_widget.display(close_button)
        
        close_button.observe(close_basemap, "value")



    def makeStateDict():
        states = {"AL": "01",
        "AR": "05",
        "FL": "12",
        "GA": "13",
        "KY": "21",
        "LA": "22",
        "MS": "28",
        "NC": "37",
        "OK": "40",
        "SC": "45",
        "TN": "47",
        "TX": "48",
        "VA": "51"
        }

    def createWidgetA4API(self):
        output_widget = widgets.Output(layout={'border': '1px solid black'})
        output_widget.clear_output()
        basemap_ctrl = WidgetControl(widget=output_widget, position='bottomright')
        self.add_control(basemap_ctrl)

        dropdown = widgets.Dropdown(
            options = ["2020", "2021", "2022"], 
            value="2020",
            description='Year',
            )

        with output_widget:
            display(dropdown)

        return output_widget
    
    def createWidgets4API(self):
        output_widget = widgets.Output(layout={'border': '1px solid black'})
        output_widget.clear_output()
        basemap_ctrl = WidgetControl(widget=output_widget, position='bottomright')
        self.add_control(basemap_ctrl)

        dropdown = widgets.Dropdown(
            options = ["2020", "2021", "2022"], 
            value="2020",
            description='Year',
            )

        with output_widget:
            display(dropdown)

        return output_widget


    def makePointsFromClick(self, coords):
        latlon = coords
        ##Make points from click
        lat = coords[0]
        lon = coords[1]

        df = pandas.DataFrame({'longitude': [lon], 'latitude': [lat]})

        geometry = geopandas.points_from_xy(df.longitude, df.latitude, crs="EPSG:4326")

        gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.longitude, df.latitude), crs="EPSG:4326")
        geo_data = GeoData(geo_dataframe = gdf,
            style={'color': 'black', 'radius':8, 'fillColor': '#3366cc', 'opacity':0.5, 'weight':1.9, 'dashArray':'2', 'fillOpacity':0.6},
            hover_style={'fillColor': 'red' , 'fillOpacity': 0.2},
            point_style={'radius': 5, 'color': 'red', 'fillOpacity': 0.8, 'fillColor': 'blue', 'weight': 3}, name="test")
        
        self.add_layer(geo_data)

        return gdf

    def addRefData(self):
        tn_counties = geopandas.read_file("https://github.com/ZachDorm/basal_and_bark/raw/main/docs/examples/data/tl_2022_us_state.zip")
        tn_counties_gd = geopandas.GeoDataFrame(tn_counties)#, crs="EPSG:4326")

        tn_counties = tn_counties.set_crs("EPSG:4326", allow_override=True)
        tn_counties_gd = tn_counties_gd.set_crs("EPSG:4326", allow_override=True)
        return tn_counties_gd

    def statesDict(self):
        states = {"AL": "01",
            "AR": "05",
            "FL": "12",
            "GA": "13",
            "KY": "21",
            "LA": "22",
            "MS": "28",
            "NC": "37",
            "OK": "40",
            "SC": "45",
            "TN": "47",
            "TX": "48",
            "VA": "51"
            }
        return states
    
    def getAPIdata(self, state, year):
        states = self.statesDict()
        state_name=state
        url = f"https://apps.fs.usda.gov/fiadb-api/fullreport?rselected=Land%20Use%20-%20Major&cselected=Land%20use&snum=79&wc={states[str(state)]}{year}&outputFormat=NJSON"    


        resp = requests.get(url)
        data = resp.json()
 # create output dictionary and populate it with estimate data frames
        outDict = {}
    # append estimates
        outDict['estimates'] = pandas.DataFrame(data['estimates'])

    # append subtotals and totals if present
        if 'subtotals' in data.keys():
            subT = {}
            for i in data['subtotals'].keys():
                subT[i] = pandas.DataFrame(data['subtotals'][i])
        
            outDict['subtotals'] = subT
            outDict['totals'] = pandas.DataFrame(data['totals'])

    # append metadata
        outDict['metadata'] = data['metadata']
        return outDict["estimates"]







    


