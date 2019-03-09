import discord
import config
from discord.ext import commands
import random
import asyncio

class Essentials:
  """
  Essential Cog for basic commands

  Attributes:
  """
  def __init__(self,client):
    self.client = client

  @commands.command(pass_context = True)
  async def say(self, ctx, *, content):
    """
    Repeats what the user says

    Args:
      content: Includes everything written after the invocation
  
    Returns:
      The content
    """
    await self.client.delete_message(message=ctx.message)
    await self.client.say(content)

  @commands.command(pass_context = True)
  async def choose(self, ctx, *options):
    """
    Chooses between some items
    """
    options = list(options)
    sent_message = await self.client.say(":four_leaf_clover: `[{}]`".format(" | ".join('{}'.format(option[1]) for option in enumerate(options))))
    while len(options) != 1:
      options.pop(random.randrange(len(options)))
      await self.client.edit_message(sent_message, ":four_leaf_clover: `[{}]`".format(" | ".join('{}'.format(option[1]) for option in enumerate(options))))
      await asyncio.sleep(1)
    await self.client.edit_message(sent_message, ":round_pushpin: **{}**".format(" | ".join('{}'.format(option[1]) for option in enumerate(options))))
            

def setup(client):
  client.add_cog(Essentials(client))