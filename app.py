from flask import Flask, render_template, request

import json

from flask_googlemaps import get_coordinates, GoogleMaps
import random
from wtforms import Form, BooleanField, StringField, validators

from functions_varias import get_zone, generate_prospect_tinder_profile, get_prospects, get_prospect_details, get_img_url, get_valid_prospects, get_img_href

app = Flask(__name__)

app.config.from_file("config.json", load= json.load)

GoogleMaps(app, key=app.config["GOOGLEMAPS_KEY"])

class GeolocForm(Form):
    adress = StringField("Dirección Completa", [validators.Length(min=1, max=200)])
    submit = BooleanField("Submit")


@app.route("/", methods=["GET", "POST"])
def geoloc():
    form = GeolocForm(request.form)
    if request.method == "POST" and form.validate():
        adress = form.adress.data
        coordinates = get_coordinates(address_text=adress, API_KEY=app.config["GOOGLEMAPS_KEY"])
        zone = get_zone(coordinates["lat"], coordinates["lng"], apiKey=app.config["GEMINI_KEY"])[0]
        prospects_unfiltered = get_prospects(zone)
        # Filter out invalid prospects
        prospects = get_valid_prospects(prospects_unfiltered)
        prospects = list(set(prospects))  # Remove duplicates
        # Randomly select 5 prospects
        if len(prospects) > 5:
            prospects = random.sample(prospects, 5)
        else:
            prospects = random.sample(prospects, len(prospects))
        # Check if there are valid prospects
        profiles = []  # Initialize the dictionary correctly
        for p in prospects:
            href = get_img_href(p)
            url = get_img_url(href)
            prospect_details = get_prospect_details(p)
            if prospect_details:  # Ensure prospect details exist
                tinder_p = generate_prospect_tinder_profile(prospect_details, app.config["GEMINI_KEY"])
                profiles.append({  # Properly populate the dictionary
                    "description": tinder_p,
                    "img": url,
                    "name": p
                })
        return render_template("coordinates.html", profiles=profiles)
    return render_template("index.html", form=form)