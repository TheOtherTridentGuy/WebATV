import asyncio
from jinja2 import Template
import os
import pyatv

routes = web.RouteTableDef()

templateDir = "templates"
staticDir = "static"


templates = {}
cache = {}


def dumpFile(fileName): 
    file = open(fileName, "r")
    return file.read()

def html(text):
    return web.Response(text=text, content_type='text/html')

# Build templates from templates directory
for filename in os.listdir(templateDir):
    fullPath = os.path.join(templateDir, filename)
    if os.path.isfile(fullPath):
          templates[filename] = Template(dumpFile(fullPath))

@routes.get('/style.css')
async def css(request):
    return web.Response(text=dumpFile("static/style.css"), content_type='text/css')

@routes.get('/')
async def index(request):
    return web.Response(text="Hello, world!")

@routes.get('/debug/{variable}')
async def hello(request):
    variable = request.match_info['variable']
    print(eval(variable))
    return web.Response(text="Printed to server console")

@routes.get('/renderTemplate')
async def render(request):

    return html(templates["index.html"].render(name="d"))


@routes.get('/cache')
async def scanPage(request):
    print(cache)
    return html(templates["scan.html"].render(cache=cache))

@routes.get('/scan')
async def scan(request):
    for result in await pyatv.scan(loop=asyncio.get_event_loop()):
        cache[result.identifier] = result
    return html("<a href='/cache'><button>Go To Results</button></a>")

# Run server with all the routes
app = web.Application()
app.add_routes(routes)
web.run_app(app)
