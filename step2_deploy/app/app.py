from solar_system import SolarSystemPage
from planet import PlanetPage
import pandas as pd
import requests

import panel as pn
pn.extension()

import holoviews as hv
hv.extension('bokeh')

planets_df = None

solarsystem_page_app = None
planet_page_app = None

def get_wikimedia_thumbnail(planet_name, suffix=False):
    
    if suffix:
        planet_name = f"{planet_name}_(planet)"
    
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={planet_name}&prop=pageimages&format=json&pithumbsize=400"
    
    r = requests.get(url)

    pages = r.json()['query']['pages']
    page_id = list(pages.keys())[0]
    if 'thumbnail' not in pages[page_id] and not suffix:
        return get_wikimedia_thumbnail(planet_name, True)
    elif 'thumbnail' not in pages[page_id]:
        return None
    
    return pages[page_id]['thumbnail']['source']


def load_data():
    global planets_df

    # Loads data
    planets_df = pd.read_json("../data/planets.json")

    # transform data
    planets_df["link"] = planets_df["name"].apply(lambda n: f"""<a href='/planet?planet_name={n}'/>{n}</a>""")

    planets_df['thumbnail'] = None
    for p in planets_df.name.to_list():
        thumbnail_url = get_wikimedia_thumbnail(p)
        planets_df.loc[ planets_df.name == p , 'thumbnail'] = thumbnail_url
    
    print( planets_df[['name', 'thumbnail']])
    print("DATA LOADED")


def build_pages():
    global solarsystem_page, planet_page
    
    solarsystem_page = SolarSystemPage(planets_df=planets_df)
    planet_page = PlanetPage(planets_df=planets_df)
    print("PAGES BUILT")

def solar_system_entry():
    return solarsystem_page.page()

def planet_entry():
    return planet_page.page()


if __name__ == "__main__":

    load_data()
    build_pages()

    pn.serve(
        {
            "/": solar_system_entry,
            "solar_system": solar_system_entry,
            "planet": planet_entry,
        },
        titles={
            "/": "Overview of the solar system",
            "solar_system": "Overview of the solar system",
            "planet": "Detailled page of a given planet",
        },
        port=80,
        start=True,
        location=True,
        show=False,
        autoreload=True
    )