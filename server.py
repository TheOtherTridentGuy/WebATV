# pylint: disable-all
from quart import Quart, Request, render_template
import pyatv
import asyncio
import json
from random import randint



app = Quart(__name__)
cache = {}

async def ignore(tv):
    pair = await pyatv.pair(appletv, pyatv.const.Protocol.AirPlay, asyncio.get_event_loop())

async def connect(appletv):
    print("connection start")
    pair = await pyatv.pair(appletv, pyatv.const.Protocol.AirPlay, asyncio.get_event_loop())
    await pair.begin()
    if pair.device_provides_pin:
        pair.pin(int(input("Enter pin:")))
    else:
        pin = randint(1000,9999)
        pair.pin(pin) # wait lets try this for now
    await pair.finish()
    print(await appletv.stream.play_url("http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"))
     

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

@app.route("/control/<string:id>/<string:action>")
async def action(id, action):
    await connect(cache[id])
    return("d")

@app.route("/scan")
async def scan():
    global cache
    result_html = ""
    n = "\n"
    for result in await pyatv.scan(loop=asyncio.get_event_loop()):
        cache[result.identifier] = result
        result_html += str(f"""{cache[result.identifier].name}<br>{str(cache[result.identifier]).replace(n, "<br>")}<br><a href="/control/{cache[result.identifier].identifier}/connect"<button>Turn On</button></a><hr>""")
    if result_html:
        return await render_template("scanner.html", results=result_html)
    return await render_template("scanner.html", results="<h3>There are no Apple TVs on your network.</h3><a href='/'>Go Home</a>")

app.run("localhost", 8080)