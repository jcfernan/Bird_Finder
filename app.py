from flask import Flask, Response, redirect, url_for
import requests
import os


app = Flask(__name__, static_url_path='', static_folder='static')


@app.route('/location/<query>')
def location(query):
    url = "http://nominatim.openstreetmap.org/search?q=" + query + "&format=json"
    r = requests.get(url, headers={'User-Agent': 'bird-finder'})
    return Response(r.text, mimetype='text/json')


@app.route('/observations/<lat>/<lng>/<dist>/<daysback>/<maxresults>')
@app.route('/observations/<lat>/<lng>/<dist>/<daysback>/<maxresults>/<species>')
def observations(lat, lng, dist, daysback, maxresults, species=None):
    token = 'cn9j4ts7dra2'
    url = 'https://api.ebird.org/v2/data/obs/geo/recent?lat={{lat}}&lng={{lng}}'
    if species:
        url = 'https://api.ebird.org/v2/data/obs/geo/recent/' + species + '?lat={{lat}}&lng={{lng}}'
    url += '&dist=' + dist
    url += '&back=' + daysback
    url += '&maxResults=' + maxresults
    url += '&lat=' + lat
    url += '&lng=' + lng
    url += '&includeProvisional=true'

    r = requests.get(url, headers={'X-eBirdApiToken': token})
    return Response(r.text, mimetype='text/json')


@app.route('/')
def root():
    return redirect(url_for('static', filename='index.html'))


if __name__ == '__main__':
    app.run()
