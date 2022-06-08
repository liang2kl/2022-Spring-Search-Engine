import base64
import json
import os
import tempfile
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from utils import ColorDescriptor, chi2_distance, distance_of_colors
import cv2
import time
from database import db_session, init_db
from models.image import Image
import redis
import hashlib

app = Flask(__name__)
CORS(app)

MAX_VALID_DISTANCE_DELTA = 2
MAX_RECORDS_RETURNED = 40
COLOR_DISTANCE_THRESHOLD = 50
REDIS_PREFIX = "image_search/"

CD = ColorDescriptor((8, 12, 3))

if os.path.isfile("env.local.json"):
    with open("env.local.json") as file:
        env = json.load(file)
else:
    with open("env.json") as file:
        env = json.load(file)

IMAGE_DIRECTORY = env["IMAGE_DIRECTORY"]
redis_host, redis_port = env["REDIS_HOST"], env["REDIS_PORT"]
redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)

init_db()

for k in redis_client.scan_iter(REDIS_PREFIX + "*"):
    redis_client.delete(k)


@app.route("/q", methods=["POST"])
def query():
    start_time = time.time()

    limit = request.args.get("limit", default=8, type=int)
    width_range = request.args.get("width", default=None, type=str)
    height_range = request.args.get("height", default=None, type=str)
    preferred_color = request.args.get("color", default=None, type=str)
    
    if width_range:
        width_range = [int(x) for x in width_range.split(",")]
    else:
        width_range = [0, 99999]
    if height_range:
        height_range = [int(x) for x in height_range.split(",")]
    else:
        height_range = [0, 99999]
    if preferred_color:
        preferred_color = [
            int(preferred_color[:2], 16),
            int(preferred_color[2:4], 16),
            int(preferred_color[4:6], 16)
        ]

    data = base64.b64decode(request.get_data())

    with tempfile.NamedTemporaryFile(delete=True) as tmpFile:
        tmpFile.write(data)
        image = cv2.imread(tmpFile.name)

    features = CD.describe(image)

    hash = hashlib.md5(data).hexdigest()
    ret_list = redis_client.get(REDIS_PREFIX + hash)

    if ret_list is not None:
        ret_list = json.loads(ret_list)
        results = []
        for id, score in ret_list:
            image = db_session.query(Image).filter_by(id=id).first()
            if image is not None:
                results.append((image, score))
    else:
        results = search(features)[:MAX_RECORDS_RETURNED]
        redis_client.set(REDIS_PREFIX + hash,
            json.dumps([(i.id, s) for i, s in results]), ex=120)

    results = filter_results(results, width_range, height_range, limit, preferred_color)
        
    ret = []
    for image, score in results[:limit]:
        url = "/i/" + image.file_name
        ret.append({
            "id": image.file_name,
            "distance": score,
            "url": url,
            "colors": image.colors
        })

    duration = time.time() - start_time

    return jsonify({
        "duration": "{:.2f}ms".format(duration * 1000),
        "results": ret
    }), 200


@app.route("/i/<path:path>", methods=["GET"])
def get_image(path):
    return send_from_directory(IMAGE_DIRECTORY, path)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


def search(query_features):
    results = []
    std_distance = chi2_distance(query_features, None)

    for image in db_session.query(Image).filter(
        # Filter out images whose std distance is out of range
        Image.distance < std_distance + MAX_VALID_DISTANCE_DELTA,
        Image.distance > std_distance - MAX_VALID_DISTANCE_DELTA):
        
        features = [float(x) for x in image.features.split(",")]
        d = chi2_distance(features, query_features)

        results.append((image, d))
    
    results = sorted(results, key=lambda r: r[1])

    return results

def filter_results(results, width_range, height_range, limit, preferred_color):
    ret = []
    for r in results:
        if len(ret) >= limit:
            break
        if not (width_range[0] <= r[0].width <= width_range[1]):
            continue
        if not (height_range[0] <= r[0].height <= height_range[1]):
            continue
        
        colors = json.loads(r[0].colors)
        
        color_valid = False
        for i, color in enumerate(colors):
            if preferred_color and not color_valid:
                if distance_of_colors(preferred_color, color) < COLOR_DISTANCE_THRESHOLD:
                    color_valid = True
            color_hex = "#" + "".join(["{:02x}".format(x) for x in color])
            colors[i] = color_hex
        
        if color_valid or not preferred_color:
            r[0].colors = colors
            ret.append(r)
    
    return ret
