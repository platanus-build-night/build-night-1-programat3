from flask import Flask, render_template, request

import json

from flask_googlemaps import get_coordinates, GoogleMaps


from wtforms import Form, BooleanField, StringField, validators

from functions_varias import get_zone, generate_prospect_tinder_profile, get_prospects, get_prospect_details

app = Flask(__name__)

app.config.from_file("config.json", load= json.load)

GoogleMaps(app, key=app.config["GOOGLEMAPS_KEY"])

class GeolocForm(Form):
    adress = StringField("Address", [validators.Length(min=1, max=200)])
    submit = BooleanField("Submit")


@app.route("/", methods=["GET", "POST"])
def geoloc():
    form = GeolocForm(request.form)
    if request.method == "POST" and form.validate():
        adress = form.adress.data
        coordinates = get_coordinates(address_text=adress, API_KEY=app.config["GOOGLEMAPS_KEY"])
        prospects = get_prospects(get_zone(coordinates["lat"], coordinates["lng"]))
        dict_prospect_profiles = {}
        for p in prospects:
            prospect_details = get_prospect_details(p)
            tinder_p = generate_prospect_tinder_profile(prospect_details, app.config["GEMINI_KEY"])
            dict_prospect_profiles[p] = tinder_p
        return render_template("coordinates.html",dict_prospects=dict_prospect_profiles)
    return render_template("index.html", form=form)