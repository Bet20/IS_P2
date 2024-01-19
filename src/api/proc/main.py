import os
import sys

from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS
import json
import xmlrpc.client


PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000
print(PORT)

app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

def rpc_call(method, *args):
    try:
        # get RPC_SERVER_PORT from env as arg to server proxy
        proxy = xmlrpc.client.ServerProxy('http://rpc-server:9000', allow_none=True)
        out = None
        if len(args) > 0:
            out = getattr(proxy, method)(*args)
        else:
            out = getattr(proxy, method)()

        return jsonify(out)
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)})

@app.route('/api/releases', methods=['GET'])
def get_releases():
    try:
        return rpc_call("get_releases")
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)})

@app.route('/api/labels', methods=['GET'])
def get_labels():
    return rpc_call("get_labels")

@app.route('/api/artists', methods=['GET'])
def get_artists():
    return rpc_call("get_artists")

@app.route('/api/genre', methods=['GET'])
def get_genre():
    arg = request.args.get('genre')
    return rpc_call("get_genre", arg)

@app.route('/api/music_before_seventies', methods=['GET'])
def get_music_before_seventies():
    return rpc_call("get_music_before_seventies")

@app.route('/api/music_from_artist', methods=['GET'])
def get_music_from_artist():
    arg = request.args.get('artist')
    return rpc_call("get_music_from_artist", arg)

if __name__ == '__main__':
    print("Starting API...")
    app.run(host="0.0.0.0", port=PORT)