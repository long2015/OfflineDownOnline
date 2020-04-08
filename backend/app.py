# --*-- coding:utf8 --*--

from urllib import parse, request as url_request
import base64
import os
import subprocess
import shutil
import tempfile

from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS

app = Flask(__name__, template_folder="templates", static_folder="static")

CORS(app)

DATA_DIR = "/tmp/www/file"
os.makedirs(DATA_DIR, exist_ok=True)

def download_file(url, filename=None):
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_path = tmp_dir.name
    p = subprocess.Popen(f"wget {url}", shell=True, stdout=subprocess.PIPE, cwd=tmp_path)
    p.wait()
    os.system(f"ls {tmp_path}")
    filename = os.listdir(tmp_path)[0]
    shutil.copyfile(f"{tmp_path}/{filename}", f"{DATA_DIR}/{filename}")

    tmp_dir.cleanup()

    return filename


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/offlinedown---<url>---<is_base64>", methods=["GET"])
def offlinedown(url, is_base64):
    print(url, is_base64)
    try:
        if is_base64 == "1":
            url = base64.b64decode(url)
            url = url.decode("utf8")
    except Exception as e:
        url = "None"
    url = parse.unquote(url)
    filename = download_file(url)
    print(f"{url} -> {filename}")
    return jsonify({
        "download_url": f"{request.host_url}download---{filename}"
    })


@app.route("/download---<filename>", methods=["GET"])
def download(filename):
    print(filename)
    return send_file(f"{DATA_DIR}/{filename}", as_attachment=True, attachment_filename=filename)


if __name__ == '__main__':
    app.run("0.0.0.0", port=5050, debug=True)
