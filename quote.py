import discord
import config
from discord.ext import commands
import random
import json
import asyncio

class Quotes:
  def __init__(self,client):
    self.client = client
    try:
      with open('quotes.json') as json_data:
        self.quote_list = json.load(json_data)
        print('Loaded {} quotes.'.format(len(self.quote_list)))
    except Exception as e:
      self.quote_list = {}
      print('Error loading quotes. [{}]'.format(e))

  @commands.group(pass_context=True)
  async def quote(self, ctx, id=None):
    quotes = self.quote_list
    quote = random.choice(quotes)
    
    if (id):
      quote = next((quote for quote in quotes if quote["id"] == int(id)), None)

    author = ctx.message.server.get_member(str(quote["author_id"]))

    if (author):
      embed=discord.Embed(title=author.nick, color=author.color)
      embed.set_thumbnail(url=author.avatar_url)
    else:
      embed=discord.Embed(title="Mr. X", color=ctx.message.author.color)

    embed.set_author(name= "#" +  str(quote["id"]) + " \"" + quote["quote"] + "\"", icon_url=ctx.message.author.avatar_url)
    embed.set_footer(text="Toots: " + str(quote["toots"]) + " | Boots: " + str(quote["boots"]) + "")
    sent_msg = await self.client.say(embed = embed)
    reactions = ["🔥", "👢"]
    for emoji in reactions: 
        await self.client.add_reaction(sent_msg, emoji)

    asyncio.sleep(1)
    toot_counter = 0
    while (toot_counter < 12):  
      toot = await self.client.wait_for_reaction(emoji=["🔥","👢"], message=sent_msg, timeout=60)
      if (toot):
        if (toot.reaction.emoji == "👢") and (toot_counter > 2):
          quote["boots"] += 1
          print("boot")
        if (toot.reaction.emoji == "🔥") and (toot_counter > 2):
          quote["toots"] += 1
          print("toot")
        with open('quotes.json', 'w') as outfile:
          json.dump(quotes, outfile, ensure_ascii=False)
        toot_counter += 1

  @quote.command(pass_context=True)
  async def add(*args):
    return

def setup(client):
  client.add_cog(Quotes(client))