import json
import pandas as pd
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

def get_zone(latitude, longitude, apiKey):
    genai.configure(api_key=apiKey)
    with open("./data/coordinates_zona.json", "r") as file:
        data = json.load(file)
    prompt = f"De qué zona y sub zona es la siguiente coordenada: {latitude}, {longitude}?, considerando que las zonas tienen como centroide las siguientes coordenadas: {data}, retorna la zona y subzona a la que pertenece la coordenada como una tupla (zona, subzona) y si no pertenece a ninguna zona retorna (None, None)"
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
    response = model.generate_content(prompt)
    response = response.text.split(",")
    response = list(map(str.strip, response))
    return response

def get_prospects(zone, nombre):
    with open("./data/especies_zona.json", "r") as file:
        data = json.load(file)
    for r in data:
        if r.get("Región") == zone:
            subregiones = r.get("Sub-Región")
            for subregion in subregiones:
                if subregion.get("nombre") == nombre:
                    prospects = subregion.get("especies")
                    if prospects:
                        return prospects
                    else:
                        return []
            break
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
    "temperature": 0.1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }
    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    )
    response = model.generate_content(prompt)
    response = response.text
    return response

def get_img_url(prospect):
    prospect = prospect.replace(" ", "-")
    prospect = prospect.tolower()
    url_busqueda = f"https://fundacionphilippi.cl/catalogo/{prospect}"
    try:
        response = requests.get(url_busqueda)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tag = soup.find('img')
        if img_tag and 'src' in img_tag.attrs:
            img_url = img_tag['src']
            if not img_url.startswith('http'):
                img_url = requests.compat.urljoin(url_busqueda, img_url)
            return img_url
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
