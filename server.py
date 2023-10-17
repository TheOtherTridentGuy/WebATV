# pylint: disable-all
# Note that I'm using flask with async. Install with: pip install "Flask[async]"
from flask import Flask, Request, render_template
import pyatv
import asyncio


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/target/<string:id>")
async def target(id):
    pass

@app.errorhandler(404)
def wrong_lever():
    return f"Wrong URL Kronk! 404."

@app.route("/scan")
async def scan():
    result_html = ""
    for result in await pyatv.scan(loop=asyncio.get_event_loop()):
        result_html += str(f"<h3>{result.name}</h3><a href=/target/{result.identifier}>Pull the lever Kronk!</a><p><b>IP Address: </b>{result.address}</p><p><b>ID: </b>{result.identifier}</p><br><br>")
    return render_template("scanner.html", results=result_html)

app.run("localhost", 8080)
