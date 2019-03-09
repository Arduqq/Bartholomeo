import discord
import config
from discord.ext import commands
import random
import asyncio

class Info:
  """
  Essential Cog for basic commands

  Attributes:
  """
  def __init__(self,client):
    self.client = client

  @commands.command(pass_context = True)
  async def git(self, ctx):
    """
    SHOW ME YOUR GITHUB, BITCH
    """
    await self.client.delete_message(message=ctx.message)
    await self.client.say("Meinen Code findest du auf https://github.com/Arduqq/Bartholomeo 📎")

  @commands.command(pass_context = True)
  async def invictus(self, ctx):
    """
    Postet den Link zu unserer Webseite
    """
    await self.client.delete_message(message=ctx.message)
    await self.client.say("Alles zur Gilde findest du auf https://invictus.cool 🦅 [AKTUELL IN BEARBEITUNG]")

def setup(client):
  client.add_cog(Info(client))