from flask import Flask, render_template, request

import json

from flask_googlemaps import get_coordinates, GoogleMaps


from wtforms import Form, BooleanField, StringField, validators

app = Flask(__name__)

app.config.from_file("config.json", load= json.load)

GoogleMaps(app, key=app.config["GOOGLEMAPS_KEY"])

class GeolocForm(Form):
    address = StringField("Address", [validators.Length(min=1, max=200)])
    submit = BooleanField("Submit")
    def validate(self):
        if not super().validate():
            return False
        if not self.address.data:
            self.address.errors.append("Address is required.")
            return False
        return True
@app.route("/", methods=["GET", "POST"])
def geoloc():
    form = GeolocForm(request.form)
    if request.method == "POST" and form.validate():
        address = form.address.data
        coordinates = get_coordinates(address)
        return render_template("geoloc.html", form=form, coordinates=coordinates)
    return render_template("index.html", form=form)