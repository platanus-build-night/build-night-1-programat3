from flask import Flask, render_template, request

import json

from flask_googlemaps import get_coordinates, GoogleMaps


from wtforms import Form, BooleanField, StringField, validators

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
        return render_template("coordinates.html",coordinates=coordinates)
    return render_template("index.html", form=form)