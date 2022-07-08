from typing import final
import panel as pn
import param
import json

class MoonsPage(param.Parameterized):

    def __init__(self, **params):
        super().__init__(**params)
        
        self.moons_ids = None
        self.moons_data = None
        

    def load_data(self):
        if self.moons_data is None:

            raw_data = json.load(open("../data/satellites.json"))

            self.moons_ids = [  p['id'] for p in raw_data  ]
            self.moons_data = {  p['id']:p for p in raw_data }


    def page(self):

        try:
            moon_id = int(pn.state.session_args.get("moon_id")[0])
        except Exception:
            moon_id = None
            

        if moon_id is None or moon_id not in self.moons_ids:

            # builds a list of links to display in markdown.
            # Each link looks like : [Mercury](/moons?moon_id=1)
            links = ""
            for pid in self.moons_ids:
                links += f"[{ self.moons_data[pid]['name']  }](/moons?moon_id={pid})  \n"


            return pn.pane.Markdown(f'''## moons \n {links}''')

        else:

            moon_name = self.moons_data[moon_id]['name']


            content = """|Property|Value|
|----|----|
"""
            for k,v in self.moons_data[moon_id].items():
                content += f"|{k}|{v}|\n"

            return pn.pane.Markdown(f'''## moons > {moon_name}
{ content }

            ''')