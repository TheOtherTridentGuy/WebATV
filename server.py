# pylint: disable-all
# Note that I'm using flask with async. Install with: pip install "Flask[async]"
from quart import Quart, Request, render_template
import pyatv
import asyncio


app = Quart(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/missioncontrol/<string:id>")
async def mission_control(id):
    pass

@app.errorhandler(404)
def wrong_lever(e):
    return render_template("text.html", text="Wrong URL Kronk! 404.")

@app.route("/scan")
async def scan():
    result_html = ""
    n = "\n"
    for result in await pyatv.scan(loop=asyncio.get_event_loop()):
        result_html += str(f"""
<h3>{result.name}</h3>
<br>
<p>{str(result).replace(n, "<br>")}</p>
<a href="/missioncontrol/{result.identifier}">Mission Control<a>
""")
    if result_html:
        return render_template("scanner.html", results=result_html)
    return render_template("scanner.html", results="<h3>There are no Apple TVs on your network.</h3><a href='/'>Go Home</a>")

app.run("localhost", 8080)
