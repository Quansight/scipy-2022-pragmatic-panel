import panel as pn
import holoviews as hv

from bokeh.models.widgets.tables import HTMLTemplateFormatter
pn.extension('tabulator', css_files=[pn.io.resources.CSS_URLS['font-awesome']])

class SolarSystemPage():

    def __init__(self, planets_df):
        self.planets_df = planets_df
        
        self.planets_colormap = {"Mercury" : "brown",
                                "Venus" : "pink", 
                                "Earth" : "blue", 
                                "Mars" : "red", 
                                "Jupiter" : "orange", 
                                "Saturn" : "brown",
                                "Uranus" : "green",
                                "Neptune" : "darkblue",
                                "Pluto" : "black"}


    def page(self):

        fields = ['link', 'mass', 'diameter', 'gravity', 'lengthOfDay', 'distanceFromSun']

        theme = 'default'
        try:
            if pn.state.session_args.get("theme")[0].decode("utf-8") == "dark":
                theme = 'midnight'
        except Exception as e:
            pass

        df_pane = pn.widgets.Tabulator(self.planets_df[ fields ], 
                                    formatters={'link':HTMLTemplateFormatter()},
                                    disabled=True,
                                    theme=theme)


        distance_points = hv.Points({ "x":self.planets_df.name,
                                      "y":self.planets_df.distanceFromSun,
                                      "diameter":self.planets_df.diameter / 1000,
                                    },
                                    vdims=['x', 'y', 'diameter'],
                                ).opts(width=800, 
                                        height=400, 
                                        color='x',
                                        cmap=self.planets_colormap,
                                        size=hv.dim('diameter'),
                                        alpha=0.8,
                                        title="Distance from the sun and diameter",
                                        legend_position='top_left',
                                    )

        return pn.Column(df_pane, distance_points)