import discord
import config
from discord.ext import commands
import random
import json
import asyncio
import re
import typing

class Quotes:
  """
  Quote Cog involving every command surrounding the stored quotes

  Each quote is stored in a quotes.json file that can be converted
  into a list of dictionaries where each quote yields the quote itself
  the discord id of the author and and the amount of toots and boots

  Attributes:
    client: the main discord client
    quote_list: list of dictionaries with each quote
  """
  def __init__(self,client):
    self.client = client
    try:
      with open('quotes.json') as json_data:
        self.quote_list = json.load(json_data)
        print('Loaded {} quotes.'.format(len(self.quote_list)))
    except Exception as e:
      self.quote_list = {}
      print('Error loading quotes. [{}]'.format(e))

  @commands.group(pass_context=True, invoke_without_command=True)
  async def quote(self, ctx, id: int = None):
    """
    Quoting command for getting a quote from the storage.
  
    Args:
      id: Identificational value

    Returns:
      A random quote or a quote of a certain user or id

    Raises:
      KeyError: Raises an exception.
    """
    await self.client.delete_message(message=ctx.message)
    quotes = self.quote_list
    quote = random.choice(quotes)

    if id:
      quote = next((quote for quote in quotes if quote["id"] == int(id)), random.choice(quotes))
      

    author = ctx.message.server.get_member(str(quote["author_id"]))

    if author:
      embed=discord.Embed(title="von: " + author.nick, color=author.color)
      embed.set_thumbnail(url=author.avatar_url)
    else:
      embed=discord.Embed(title="von: Mr. X", color=ctx.message.author.color)

    embed.set_author(name= "[#" +  str(quote["id"]) + "] \"" + quote["quote"] + "\"", icon_url=ctx.message.author.avatar_url)
    embed.set_footer(text="Toots: " + str(quote["toots"]) + " | Boots: " + str(quote["boots"]) + "")
    sent_msg = await self.client.say(embed = embed)
    reactions = ["🔥", "👢"]
    for emoji in reactions: 
      await self.client.add_reaction(sent_msg, emoji)

    asyncio.sleep(1)
    toot_counter = 0
    while (toot_counter < 12):  
      toot = await self.client.wait_for_reaction(emoji=["🔥","👢"], message=sent_msg, timeout=60)
      if toot:
        if (toot.reaction.emoji == "👢") and (toot.user.id != "544835802811727872"):
          quote["boots"] += 1
        if (toot.reaction.emoji == "🔥") and (toot.user.id != "544835802811727872"):
          quote["toots"] += 1
        with open('quotes.json', 'w') as outfile:
          json.dump(quotes, outfile, ensure_ascii=False, indent = 4)
        embed.set_footer(text="Toots: " + str(quote["toots"]) + " | Boots: " + str(quote["boots"]) + "")
        await self.client.edit_message(message = sent_msg, embed = embed)
        toot_counter += 1

  @quote.error
  async def quote_handler(self, error, ctx):
    """
    Handler for errors in the quote command
    """
    if isinstance(error, commands.BadArgument): 
      await self.client.say("💔 [KeineZahl] **Usage: **`!quote (#)`")
      print(error)


  @quote.command(pass_context=True)
  async def user(self, ctx, user: discord.User):
    """
    Gets a quote of a certain user

    Args:
      *quote: String sequence with the author at the end

    Returns:
      The formatted quote
    """
    await self.client.delete_message(message=ctx.message)
    quotes = self.quote_list
    quote = random.choice(quotes)

    if user:
      user_quotes = [x for x in quotes if x["author_id"] == int(user.id)]
      quote = random.choice(user_quotes)
      

    author = ctx.message.server.get_member(str(quote["author_id"]))

    if author:
      embed=discord.Embed(title="von: " + author.nick, color=author.color)
      embed.set_thumbnail(url=author.avatar_url)
    else:
      embed=discord.Embed(title="von: Mr. X", color=ctx.message.author.color)

    embed.set_author(name= "[#" +  str(quote["id"]) + "] \"" + quote["quote"] + "\"", icon_url=ctx.message.author.avatar_url)
    embed.set_footer(text="Toots: " + str(quote["toots"]) + " | Boots: " + str(quote["boots"]) + "")
    sent_msg = await self.client.say(embed = embed)
    reactions = ["🔥", "👢"]
    for emoji in reactions: 
      await self.client.add_reaction(sent_msg, emoji)

    asyncio.sleep(1)
    toot_counter = 0
    while (toot_counter < 12):  
      toot = await self.client.wait_for_reaction(emoji=["🔥","👢"], message=sent_msg, timeout=60)
      if toot:
        if (toot.reaction.emoji == "👢") and (toot.user.id != "544835802811727872"):
          quote["boots"] += 1
        if (toot.reaction.emoji == "🔥") and (toot.user.id != "544835802811727872"):
          quote["toots"] += 1
        with open('quotes.json', 'w') as outfile:
          json.dump(quotes, outfile, ensure_ascii=False, indent = 4)
        embed.set_footer(text="Toots: " + str(quote["toots"]) + " | Boots: " + str(quote["boots"]) + "")
        await self.client.edit_message(message = sent_msg, embed = embed)
        toot_counter += 1

  @quote.command(pass_context=True)
  async def add(self, ctx, author: discord.User, *, quote):
    """
    Adds new quotes to the json file (Put author at the end of the invocation)

    Args:
      *quote: String sequence with the author at the end

    Returns:
      The formatted quote
    """
    new_quote = {}
    quote_only = "".join(quote)

    await self.client.delete_message(message=ctx.message)

    for char in ("\":-"):
      quote_only = quote_only.replace(char,"")

    new_quote["id"] = self.quote_list[-1]["id"]+1
    new_quote["quote"] = quote_only
    new_quote["author_id"] = author.id
    new_quote["toots"] = 0
    new_quote["boots"] = 0  
    self.quote_list.append(new_quote)
    with open('quotes.json', 'w') as outfile:
          json.dump(self.quote_list, outfile, ensure_ascii=False, indent = 4)
    embed=discord.Embed(title="von: " + author.nick + " erfolgreich hinzugefügt!", color=author.color)
    embed.set_thumbnail(url=author.avatar_url)
    embed.set_author(name= "[#" +  str(new_quote["id"]) + "] \"" + new_quote["quote"] + "\"", icon_url=ctx.message.author.avatar_url)
    embed.set_footer(text="Toots: " + str(new_quote["toots"]) + " | Boots: " + str(new_quote["boots"]) + "")
    await self.client.say(embed = embed)


def setup(client):
  client.add_cog(Quotes(client))