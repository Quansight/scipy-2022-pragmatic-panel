from typing import final
import panel as pn
import param
import json

class PlanetsPage(param.Parameterized):

    def __init__(self, **params):
        super().__init__(**params)
        
        self.planets_ids = None
        self.planets_data = None
        

    def load_data(self):
        if self.planets_data is None:

            raw_data = json.load(open("../data/planets.json"))

            self.planets_ids = [  p['id'] for p in raw_data  ]
            self.planets_data = {  p['id']:p for p in raw_data }


    def page(self):

        try:
            planet_id = int(pn.state.session_args.get("planet_id")[0])
        except Exception:
            planet_id = None
            

        if planet_id is None or planet_id not in self.planets_ids:

            # builds a list of links to display in markdown.
            # Each link looks like : [Mercury](/planets?planet_id=1)
            links = ""
            for pid in self.planets_ids:
                links += f"[{ self.planets_data[pid]['name']  }](/planets?planet_id={pid})  \n"


            return pn.pane.Markdown(f'''## Planets \n {links}''')


        else:

            planet_name = self.planets_data[planet_id]['name']


            content = """|Property|Value|
|----|----|
"""
            for k,v in self.planets_data[planet_id].items():
                content += f"|{k}|{v}|\n"

            return pn.pane.Markdown(f'''## Planets > {planet_name}
{ content }

            ''')

