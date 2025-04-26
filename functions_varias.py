import json
import pandas as pd
import os
def get_zone(latitude, longitude):
   pass
def get_prospects(zone, nombre):
    with open("/data/especies_zona.json", "r") as file:
        data = json.load(file)
        prospects = data[zone]
        for subregion, subzonas in prospects.items():
            if isinstance(subzonas, list):
                for subzona in subzonas:
                    if subzona.get("nombre") == nombre:
                        return subzona.get("especies", [])
    return []


def get_prospect_details(prospect):
    df = pd.read_csv("./data/RasgosCL_aggregatedspp.csv")
    df = df[df["accepted_species"] == prospect]
    if df.empty:
        return None
    else:
        df = df.to_dict()
        return df
def generate_prospect_tinder_profile(prospect_dict):
