import discord
import json
import config
from threading import Thread
from flask import Flask
from flask import Response
from flask_cors import CORS
from functools import partial
from discord.ext import commands
from cors import crossdomain
import random

token = config.BOT_CONFIG["discord_token"]
description = "Do not interfere."

app = Flask(__name__)
CORS(app, origins=["http://localhost:5000", "http://invictus.cool"])
client = commands.Bot(command_prefix="!", description=description)

extensions = ["quote", "essentials", "fun", "info"]

@app.route("/")
def hello():
  return("Hello from {}".format(client.user.name))


@app.route("/quotes", methods=["GET"])
@crossdomain(origin='*')
def quotes():
  with open('quotes.json') as json_data:
    quotelist = json.load(json_data)
    for value in quotelist:
      for server in client.servers:
        author = server.get_member(str(value["author_id"]))
        if author:
          value["author_id"] = author.name
  return(Response(json.dumps(quotelist),  mimetype='application/json'))


@client.event
async def on_ready():
  print("------")
  print("Mother has arrived.")
  print("client: " + client.user.name)
  print("ID: " + client.user.id)
  print("------")

@client.command()
async def load():
  for extension in extensions:
    try:
      client.load_extension(extension)
      print("{} cog loaded successfully".format(extension))
    except Exception as error:
      print("{} could not be loaded. [{}]".format(extension,error))

@client.command()
async def unload():
  for extension in extensions:
    try:
      client.unload_extension(extension)
      print("{} cog unloaded successfully".format(extension))
    except Exception as error:
      print("{} could not be unloaded. [{}]".format(extension,error))


if __name__ == "__main__":
  for extension in extensions:
    try:
      client.load_extension(extension)
      print("{} cog loaded successfully".format(extension))
    except Exception as error:
      print("{} could not be loaded. [{}]".format(extension,error))

  partial_run = partial(app.run, host="0.0.0.0", port=5000, debug=True, use_reloader=False, threaded=True)
  t = Thread(target=partial_run)
  t.start()
  client.run(token)
