import time
import pygeoip
import socket

from utils import decimalDegrees2DMS
from arduino import ArduinoDisplay
from flask import Flask, jsonify, request, abort
from urlparse import urlparse

gi = pygeoip.GeoIP('GeoLiteCity.dat')
app = Flask(__name__)

display = ArduinoDisplay()

@app.route("/connect")
def connect():
    return "Hello World!"

@app.route("/locate", methods=['POST'])
def locate():
    o = urlparse(request.form["url"])
    try:
        res = socket.gethostbyname(o.netloc)
        display.clear()
        display.write("Locating..")
        display.newline()
        display.write(o.netloc)
        time.sleep(1.5)
        display.clear()
        geoinfo = gi.record_by_addr(res)
        lat = geoinfo['latitude']
        lng = geoinfo['longitude']
        lat = decimalDegrees2DMS(lat, "Latitude")
        lng = decimalDegrees2DMS(lng, "Longitude")
        display.write(lat)
        display.newline()
        display.write(lng)
        return jsonify(netloc=o.netloc, nslookup=res, lat=lat, lng=lng)
    except Exception as e:
        print e
        abort(500)


if __name__ == "__main__":
    app.run(port=9000, debug=True)
