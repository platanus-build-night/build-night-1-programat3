import json
import pandas as pd
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

def get_zone(latitude, longitude, apiKey):
    genai.configure(api_key=apiKey)
    with open("./data/coordinates_zona.json", "r") as file:
        data = json.load(file)
    prompt = f"De qué zona es la siguiente coordenada: {latitude}, {longitude}?, considerando que las zonas tienen como centroide las siguientes coordenadas: {data}, retorna la zona a la que pertenece la coordenada  y si no pertenece a ninguna zona retorna None, sólo la zona, no más datos!"
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

def normalize_parameter(parameter):
    parameter = parameter.replace("\'", "")
    parameter = parameter.lower()
    parameter = parameter.replace("á", "a")
    parameter = parameter.replace("é", "e")
    parameter = parameter.replace("í", "i")
    parameter = parameter.replace("ó", "o")
    parameter = parameter.replace("ú", "u")
    return parameter

def get_prospects(subZone):
    with open("./data/especies_zona.json", "r") as file:
        data = json.load(file)
    subZone = normalize_parameter(subZone)
    prospects_full = []
    for r in data:
        try:
            chosen_sr = r[subZone]
            for i in chosen_sr:
                prospects = i["especies"]
                for j in prospects:
                    if j not in prospects_full:
                        prospects_full.append(j)
        except:
            pass
    return prospects_full


def get_prospect_details(prospect):
    df = pd.read_csv("./data/RasgosCL_aggregatedspp.csv")
    df = df[df["accepted_species"] == prospect]
    if df.empty:
        return None
    else:
        df = df.to_dict()
        return df
def get_valid_prospects(prospects):
    valid_prospects = []
    for prospect in prospects:
        df = pd.read_csv("./data/RasgosCL_aggregatedspp.csv")
        df = df[df["accepted_species"] == prospect]
        if not df.empty:
            valid_prospects.append(prospect)
    return valid_prospects
def generate_prospect_tinder_profile(prospect_dict, apiKey):
    genai.configure(api_key=apiKey)
    prompt = f"Genera un perfil similar a Tinder para la especie {prospect_dict['accepted_species']} con las siguientes características: {prospect_dict} redactadas de forma divertida y en español, un solo string, no en formato mark down, no más de 150 palabras, no hagas connotaciones románticas, sólo la descripción, no más datos!"
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

def get_img_href(prospect):
    prospect = prospect.replace(" ", "+")
    url_busqueda = f"https://www.herbariodigital.cl/catalog/?search={prospect}&select_category=species&send=Search"
    try:
        response = requests.get(url_busqueda)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tag = soup.find_all('a', class_='text-dark', )
        for img in img_tag:
            if img and img.get('href'):
                img_url = img.get('href')
                if img_url.startswith('/catalog/details/'):
                    img_url = 'https://www.herbariodigital.cl' + img_url
                    return img_url
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
def get_img_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tag = soup.find_all('img', {'data-target': '#galleryCarousel'})
        for img in img_tag:
            if img and img.get('src'):
                img_url = img.get('src')
                if img_url.startswith('https://images.herbariodigital.cl/gallery/'):
                    return img_url
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
