import discord
import config
from discord.ext import commands
import random

token = config.BOT_CONFIG["discord_token"]
description = "Do not interfere."
client = commands.Bot(command_prefix="!", description=description)

extensions = ["quote", "essentials", "fun"]

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

  client.run(token)