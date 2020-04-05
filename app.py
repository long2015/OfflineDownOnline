# --*-- coding:utf8 --*--

from urllib import parse, request as url_request
import base64
import subprocess
from time import sleep

from flask import Flask, request


app = Flask(__name__)


def download_file(url, filename=None):
    p = subprocess.Popen(f"wget {url}", shell=True, stdout=subprocess.PIPE)
    sleep(1)

    while True:
        if p.stdout.readable():
            break

    for line in p.stdout.readlines():
        if line.find(b"Saving to"):
            filename = line[10:]
            print("download to:", filename)
            break

    return filename


@app.route("/offlinedown---<url>---<is_base64>", methods=["GET"])
def offlinedown(url, is_base64):
    print(url, is_base64)
    if is_base64 == "1":
        url = base64.b64decode(url)
    url = url.decode("utf8")
    url = parse.unquote(url)
    filename = download_file(url)
    print(f"{url} -> {filename}")
    return f"Downloading: <a blank='_' href='{request.host_url}/download---{filename}' />"


@app.route("/download---<url>", methods=["GET"])
def download(url):
    print(url)
    return f"finished: {url}"


if __name__ == '__main__':
    app.run("0.0.0.0", port=5050)
