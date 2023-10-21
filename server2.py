from quart import Quart, Request, render_template, abort
import pyatv
import asyncio

app = Quart(__name__)
cache = {}

