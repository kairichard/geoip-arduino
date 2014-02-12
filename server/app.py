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
display.clear()
display.write("Initializing")
time.sleep(1)
display.clear()

def locate_lat_lng(ip):
    geoinfo = gi.record_by_addr(ip)
    lat = geoinfo['latitude']
    lng = geoinfo['longitude']
    lat = decimalDegrees2DMS(lat, "Latitude")
    lng = decimalDegrees2DMS(lng, "Longitude")
    return lat, lng

@app.route("/connect")
def connect():
    display.clear()
    display.write("Chrome connected")
    return "OK"

@app.route("/locate", methods=['POST'])
def locate():
    o = urlparse(request.form["url"])
    try:
        display.clear()
        display.write("Locating...")
        display.second_row()
        display.write(o.netloc)
        time.sleep(1.5)
        ip = socket.gethostbyname(o.netloc)
        lat, lng = locate_lat_lng(ip)
        display.write("Lat: " + lat)
        display.second_row()
        display.write("Lng: " + lng)
        return jsonify(netloc=o.netloc, nslookup=ip, lat=lat, lng=lng)
    except Exception as e:
        print e
        abort(500)


if __name__ == "__main__":
    app.run(port=9000, debug=False)
