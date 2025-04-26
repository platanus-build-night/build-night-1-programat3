import json
import pandas as pd
import os
import google.generativeai as genai

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
def generate_prospect_tinder_profile(prospect_dict, apiKey):
    genai.configure(api_key=apiKey)
    prompt = f"Genera un perfil similar a Tinder para la especie {prospect_dict['accepted_species']} con las siguientes características: {prospect_dict} redactadas de forma divertida y en español"
    generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }
    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    )
    response = model.generate(prompt)
    response = response.text
    return response