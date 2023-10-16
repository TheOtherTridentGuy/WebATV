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
        result_html += f"<div>Name: {result.name} Address: {result.address}</div>"
    return render_template("scanner.html", results=result_html)


app.run("localhost", 8080)
