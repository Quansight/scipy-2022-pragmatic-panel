import panel as pn
import pandas as pd

import holoviews as hv

class PlanetPage():

    def __init__(self, planets_df):
        self.planets_df = planets_df

        self.planets_colormap = colors = {"Mercury" : "brown",
                                        "Venus" : "pink", 
                                        "Earth" : "blue", 
                                        "Mars" : "red", 
                                        "Jupiter" : "orange", 
                                        "Saturn" : "brown",
                                        "Uranus" : "green",
                                        "Neptune" : "darkblue",
                                        "Pluto" : "black"}
        
    def get_distance_sun_plot(self, planet_name):

        self.planets_df['alpha'] = self.planets_df.name.apply(lambda p: 0.8 if p == planet_name else 0.2)

        distance_points = hv.Points({"x":self.planets_df.name,
                                    "y":self.planets_df.distanceFromSun,
                                    "diameter":self.planets_df.diameter / 1000,
                                    "alpha":self.planets_df.alpha
                                    },
                                    vdims=['x', 'y', 'diameter', 'alpha'],

                                ).opts( width=800, 
                                        height=400, 
                                        color='x',
                                        cmap=self.planets_colormap,
                                        size=hv.dim('diameter'),
                                        alpha='alpha',
                                        title="Distance from the sun and planet diameter",
                                        legend_position='top_left',
                                        toolbar=None
                                )
        
        return distance_points

    def get_other_plots(self, planet_name):
        mean_temp = hv.Points({"x":1, 
                     "y":self.planets_df.meanTemperature,
                     "diameter":self.planets_df.diameter / 1000,
                     "name":self.planets_df.name,
                     "alpha":self.planets_df.alpha
                   },
                  vdims=['name', 'alpha'],

                  ).opts(color='name',
                         cmap=self.planets_colormap,
                         size=10,
                         alpha=('alpha'),
                         show_legend=False,
                         xlabel="Mean temperature"
                        )

        nbr_moons = hv.Points({"x":1, 
                     "y":self.planets_df.numberOfMoons,
                     "name":self.planets_df.name,
                     "alpha":self.planets_df.alpha
                   },
                  vdims=['name', 'alpha'],
                  ).opts(color='name',
                         cmap=self.planets_colormap,
                         size=10,
                         alpha=('alpha'),
                         show_legend=False,
                         xlabel="Number of moons"
                        )

        return (mean_temp + nbr_moons).opts(shared_axes=False, toolbar=None)

    def page(self):


        try:
            planet_name = pn.state.session_args.get("planet_name")[0].decode("utf-8")
        except Exception as e:
            raise e
            

        # Data wrangling

        # select only the data for the given planet_name
        planet_data = self.planets_df[ self.planets_df.name == planet_name ]

        # don't display the "link" value
        planet_data = planet_data.loc[:, planet_data.columns != 'link']
        thumbnail = planet_data.iloc[0]['thumbnail']


        # Pivot values and colums to have one row per characteristic of a planet
        planet_data = planet_data.unstack(level=0).reset_index().drop(columns=["level_1"])

        planet_data = pd.DataFrame(planet_data)\
                        .rename(columns={"level_0":"Characteristic", 0:"Value"})


        theme = 'default'
        try:
            if pn.state.session_args.get("theme")[0].decode("utf-8") == "dark":
                theme = 'midnight'
        except Exception as e:
            pass

        df_pane = pn.widgets.Tabulator(planet_data, 
                                        disabled=True,
                                        theme=theme
                                        )

        #style = """{:width="400px"}"""
        content = pn.Row(
            df_pane, 
            pn.Column(
                #pn.pane.Markdown(f"""![{planet_name}]({thumbnail}){style} <br />"""),
                pn.pane.HTML(f"""<img src="{thumbnail}" height="300px" style="display:block;" /> <br />"""),
                self.get_distance_sun_plot(planet_name=planet_name),
                self.get_other_plots(planet_name=planet_name)
            )

        )

        return content
