# pylint: disable-all
from quart import Quart, Request, render_template, abort
import pyatv
import asyncio
import json


app = Quart(__name__)
cache = {}

@app.route("/")
async def index():
    return await render_template("index.html")

@app.route("/control/<string:id>")    
async def control(id):
    global cache
    atv = cache.get(id)
    if atv:
        print (atv.name)
        return await render_template("control.html", name=atv.name, data=str(atv).replace("\n", "<br>"))
    return await render_template("error.html", textual="Apple TV", code=404)

@app.errorhandler(404)
async def wrong_lever(e):
    return await render_template("error.html", textual="URL", code=404)

@app.route("/scan")
async def scan():
    global cache
    result_html = ""
    n = "\n"
    for result in await pyatv.scan(loop=asyncio.get_event_loop()):
        cache[result.identifier] = result
        result_html += str(f"""
<h3><a href="/control/{result.identifier}">{result.name}</a></h3>
<p>{str(result).replace(n, "<br>")}</p><hr>
""")
    if result_html:
        return await render_template("scanner.html", results=result_html)
    return await render_template("scanner.html", results="<h3>There are no Apple TVs on your network.</h3><a href='/'>Go Home</a>")

app.run("localhost", 8080)