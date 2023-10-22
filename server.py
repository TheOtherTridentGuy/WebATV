# pylint: disable-all
from quart import Quart, Request, render_template
from werkzeug.exceptions import HTTPException
import pyatv
import asyncio
import json
from random import randint



app = Quart(__name__)
cache = {}
pairs = {}
pairs_in_progress = {}


@app.route("/")
async def index():
    return await render_template("index.html")

@app.route("/beginpair/<string:id>")
async def begin_pair(id):
    tv = cache.get(id)
    if tv:
        pair = await pyatv.pair(tv, pyatv.const.Protocol.AirPlay, asyncio.get_event_loop())
        await pair.begin()
        pairs_in_progress[id] = [pair, tv]
    return "TV Not in cache.", 404

@app.route("/finishpair/<string:id>")
async def finish_pair(id):
    pair = pairs_in_progress.get(id)
    pin = Request.values.get("pin")
    if pair and pin:
        await pair[0].pin(pin) # index 0 is the pair object
        await pair[0].finish()
        pairs[id] = pair[1] # index 1 is the tv itself
    return "TV Has not yet started pair or you didn't provide a pin.", 404

# hi?
# anyone there?
# I'm working on a better error handler
# Cool
# error texts are in a hash table? I see


@app.errorhandler(Exception)
async def wrong_lever(e):
    # The hash table:
    # aww, i gotta go, have fun with 
    #how bout i commit and u fork
    # u can use codespaces if your not on a good computer
    #can you leave it open
    # and make a new terminal so i can run the server

    # Okay
    
    errors = {
        "400": "request",
        "401": "user",
        "402": "price", # its for payment required idk what to put should i delete?
        "403": "permissions",
        "404": "url"
        "405": "method"
        "406"
    }
    if isinstance(e, HTTPException):
        print()
        return await render_template("error.html", textual=errors.get(str(e.code), default="something"), code=e.code)
    print(e)
    return await render_template("error.html", textual="server code", code=500)

@app.route("/scan")
async def scan():
    global cache
    result_html = ""
    n = "\n"
    for result in await pyatv.scan(loop=asyncio.get_event_loop()):
        cache[result.identifier] = result
        result_html += str(f"""
    <div>
        {result.name}
        <br>
        {str(result).replace(n, "<br>")}
        <br>
        <div>
            <button onclick="begin_pair('id', this.parentElement)">Pair</button>
        </div>
        <hr>
    </div>""")
    if result_html:
        return await render_template("scanner.html", results=result_html)
    return await render_template("scanner.html", results="<h3>There are no Apple TVs on your network.</h3><a href='/'>Go Home</a>")

app.run("localhost", 8080)