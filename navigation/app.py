from planets import PlanetsPage
from moons import MoonsPage

import panel as pn
pn.extension()



def homepage():
    return pn.pane.Markdown("""# Homepage
    
## Summary 
[Planets](/planets)  
[Moons](/moons)  

""")


planets_page_app = None
moons_page_app = None

def build_apps():
    global planets_page_app, moons_page_app
    
    planets_page_app = PlanetsPage()
    planets_page_app.load_data()

    moons_page_app = MoonsPage()
    moons_page_app.load_data()


def planets_page():
    return planets_page_app.page()

def moons_page():
    return moons_page_app.page()


if __name__ == "__main__":

    build_apps()

    pn.serve(
        {
            "/": homepage,
            "planets": planets_page,
            "moons": moons_page,
        },
        titles={
            "/": "Home",
            "planets": "Planets of the solar system",
            "moons": "Moons (planetary satellites) of the Planets",
        },
        port=80,
        # websocket_origin=websocket_origin,
        start=True,
        location=True,
        show=False,
        autoreload=True
    )