import time
import serial
import pygeoip
import socket
from socket import gethostbyaddr

from flask import Flask, jsonify, request, abort
from urlparse import urlparse

gi = pygeoip.GeoIP('GeoLiteCity.dat')
arduino = serial.Serial('/dev/tty.usbmodemfa131', 9600)
app = Flask(__name__)


def decimalDegrees2DMS(value,type):
    """
        Converts a Decimal Degree Value into
        Degrees Minute Seconds Notation.

        Pass value as double
        type = {Latitude or Longitude} as string

        returns a string as D:M:S:Direction
        created by: anothergisblog.blogspot.com
    """
    degrees = int(value)
    submin = abs( (value - int(value) ) * 60)
    minutes = int(submin)
    subseconds = abs((submin-int(submin)) * 60)
    direction = ""
    if type == "Longitude":
        if degrees < 0:
            direction = "W"
        elif degrees > 0:
            direction = "E"
        else:
            direction = ""
    elif type == "Latitude":
        if degrees < 0:
            direction = "S"
        elif degrees > 0:
            direction = "N"
        else:
            direction = ""
    notation = str(degrees) + "*" + str(minutes) + "'" +\
               str(subseconds)[0:2] + "''" + direction
    return notation


def traceroute(dest_name):
    dest_addr = socket.gethostbyname(dest_name)
    port = 33434
    max_hops = 30
    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')
    ttl = 1
    res = list()
    while True:
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
        send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        recv_socket.bind(("", port))
        send_socket.sendto("", (dest_name, port))
        curr_addr = None
        curr_name = None
        try:
            _, curr_addr = recv_socket.recvfrom(512)
            curr_addr = curr_addr[0]
            try:
                curr_name = socket.gethostbyaddr(curr_addr)[0]
            except socket.error:
                curr_name = curr_addr
        except socket.error:
            pass
        finally:
            send_socket.close()
            recv_socket.close()

        if curr_addr is not None:
            curr_host = "%s (%s)" % (curr_name, curr_addr)
        else:
            curr_host = "*"
        res.append([ttl, curr_host])

        ttl += 1
        if curr_addr == dest_addr or ttl > max_hops:
            break
    return res

def send_to_arduino(msg):
    map(arduino.write,list(str(msg)))


@app.route("/connect")
def connect():
    return "Hello World!"

@app.route("/locate", methods=['POST'])
def locate():
    o = urlparse(request.form["url"])
    try:
        res = socket.gethostbyname(o.netloc)
        geoinfo = gi.record_by_addr(res)
        lat = geoinfo['latitude']
        lng = geoinfo['longitude']
        lat = decimalDegrees2DMS(lat, "Latitude")
        lng = decimalDegrees2DMS(lng, "Longitude")
        send_to_arduino(lat)
        send_to_arduino(lng)
        return jsonify(netloc=o.netloc, nslookup=res, lat=lat, lng=lng)
    except Exception as e:
        print e
        abort(500)


if __name__ == "__main__":
    app.run(port=9000, debug=True)