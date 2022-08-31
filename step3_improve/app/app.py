from solar_system import SolarSystemPage
from planet import PlanetPage
import pandas as pd
import requests

import panel as pn
pn.extension()


planets_df = None

solarsystem_page = None
planet_page = None


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
    planets_df = pd.read_json("../data/planets.json")
    planets_df["link"] = planets_df["name"].apply(lambda n: f"""<a href='/planet?planet_name={n}'/>{n}</a>""")


    planets_df['thumbnail'] = None
    for p in planets_df.name.to_list():
        thumbnail_url = get_wikimedia_thumbnail(p)
        planets_df.loc[ planets_df.name == p , 'thumbnail'] = thumbnail_url
    

    print("DATA LOADED")

def build_apps():
    global solarsystem_page, planet_page
    solarsystem_page = SolarSystemPage(planets_df=planets_df)
    planet_page = PlanetPage(planets_df=planets_df)
    print("PAGES BUILT")


def get_menu():

    # retrieve the current theme from the URL parameters, 
    # to pass it along the other pages and keep it active
    theme = None
    try:
        theme = pn.state.session_args.get("theme")[0].decode("utf-8")
    except Exception as e:
        pass

    theme_param = f"theme={theme}" if theme is not None else ''
    menu_md =  f"""[**Home**](/?{theme_param})\n"""

    for p in planets_df.name.to_list():
        menu_md += f"""[{p}](/planet?planet_name={p}&{theme_param})\n"""

    return pn.pane.Markdown(menu_md),

def solar_system_entry():
    template = pn.template.FastListTemplate(title='Solar System', 
                                        sidebar=get_menu(),
    )
    
    template.main.append(pn.Column(
                                solarsystem_page.page()
                            )
    )
    return template

def planet_entry():
    
    try:
        planet_name = pn.state.session_args.get("planet_name")[0].decode("utf-8")
    except Exception as e:
        raise e

    template = pn.template.FastListTemplate(title=planet_name, 
                                        sidebar=get_menu(),
    )
    
    template.main.append(pn.Column(
                                pn.pane.Markdown("""<a href='/'>&lt; Back</a>"""),
                                planet_page.page()
                            ))
    

    return template


if __name__ == "__main__":

    load_data()
    build_apps()

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
        autoreload=True,
        admin=True
    )