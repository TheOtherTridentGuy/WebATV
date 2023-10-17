# pylint: disable-all
# Note that I'm using flask with async. Install with: pip install "Flask[async]"
from flask import Flask, Request, render_template
import pyatv
import asyncio


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scan")
async def scan():
    result_html = ""
    for result in await pyatv.scan(loop=asyncio.get_event_loop()):
        result_html += str(f"<h3>{result.name}</h3><p><b>IP Address: </b>{result.address}</p><p><b>ID: </b>{result.identifier}</p><br><br>")
    return render_template("scanner.html", results=result_html)

app.run("localhost", 8080)