import discord
import config
from discord.ext import commands
import random
import asyncio
import aiohttp

class Fun:
  """
  Fun Cog for simple fun responses

  Attributes:
  """
  def __init__(self,client):
    self.client = client

  @commands.command()
  async def rant(self):
    rant_responses = [
      "Nicht im Ernst?!",
      "Ich frage mich wie andere Leute dazu stehen.",
      "Gut, dass du das ansprichst! Bin komplett bei dir. :rolling_eyes:",
      "You go girl! :fire:",
      ":triumph: Das macht mich auch so wütend!",
      "Oder?! Mega dumm.",
      "Ja, wtf man.",
      "Wtf. Wie ätzend.",
      "Nicht, dass dich das noch weiter kaputt macht. :cry:",
      "Sag Bescheid, wenn man irgendwas für dich tun kann!",
      "Schön, dass du das mit uns teilst. :slight_smile:",
      "Endlich spricht jemand die wichtigen Dinge im Leben an.",
      "Ist schon gut, lass alles raus. :wind_blowing_face: ",
      "Keine Sorge, Bartholomeo ist ja da."
      ]

    await self.client.say(random.choice(rant_responses))
    """
    Says whatever you want Batholomeo to say
    """
    asyncio.sleep(1)

    needs_something_cute = random.choice([True, False])

    if needs_something_cute:
      needs_a = random.choice(["Doggo", "Kitty", "Capybara", "Shibe", "Punch"])
      if needs_a == "Kitty":
        await self.client.say("Ich übernehme das, keine Sorge! Hier ein Kätzchen. :cat:")
        cat = await self.get_cat()
        em = discord.Embed()
        em = em.set_image(url=cat["file"])
        sent_msg = await self.client.say(embed=em)
        await self.client.add_reaction(sent_msg, "😻")
      elif needs_a == "Doggo":
        await self.client.say("Ich glaube, du brauchst jetzt ein Hündchen. :dog:")
        dog = await self.get_dog()
        em = discord.Embed()
        em = em.set_image(url=dog["message"])
        sent_msg = await self.client.say(embed=em)
        await self.client.add_reaction(sent_msg, "🐶")
      elif needs_a == "Shibe":
        await self.client.say("Oh, ich hab die Idee, um dich aufzuheitern!")
        dog = await self.get_shibe()
        em = discord.Embed()
        em = em.set_image(url=dog[0])
        sent_msg = await self.client.say(embed=em)
        await self.client.add_reaction(sent_msg, "💕")


  async def get_cat(self):
    async with aiohttp.ClientSession() as session:
      async with session.get('http://aws.random.cat/meow') as file:
        session.close()
        res = await file.json()
        return res

  async def get_dog(self):
    async with aiohttp.ClientSession() as session:
      async with session.get('https://dog.ceo/api/breeds/image/random') as file:
        session.close()
        res = await file.json()
        return res

  async def get_shibe(self):
    async with aiohttp.ClientSession() as session:
      async with session.get('http://shibe.online/api/shibes') as file:
        session.close()
        res = await file.json()
        return res

  @commands.command(pass_context = True)
  async def puss(self, ctx):
    """
    Posts a cute cat
    """
    await self.client.delete_message(message=ctx.message)
    cat = await self.get_cat()
    em = discord.Embed()
    em = em.set_image(url=cat["file"])
    sent_msg = await self.client.say(embed=em)
    await self.client.add_reaction(sent_msg, "😻")

  @commands.command(pass_context = True)
  async def doggo(self, ctx):
    """
    Posts a cute dog
    """
    await self.client.delete_message(message=ctx.message)
    dog = await self.get_dog()
    em = discord.Embed()
    em = em.set_image(url=dog["message"])
    sent_msg = await self.client.say(embed=em)
    await self.client.add_reaction(sent_msg, "🐶")

  @commands.command(pass_context = True)
  async def shibe(self, ctx):
    """
    Posts a cute shibe
    """
    await self.client.delete_message(message=ctx.message)
    dog = await self.get_shibe()
    em = discord.Embed()
    em = em.set_image(url=dog[0])
    sent_msg = await self.client.say(embed=em)
    await self.client.add_reaction(sent_msg, "💕")

  @commands.command(pass_context = True, tts=True)
  async def dab(self, ctx):
    dab_messages = [
      "Lösch dich, {}.",
      "{}, Du bist peinlich. 🙄",
      "Kann jemand {} kurz schlagen?",
      "Ergh, halt endlich dein Maul, {}. 🤦‍",
      "Dabbe auf die Haters, Bruder.",
      "{} hat's nicht verstanden.",
      "Was für 1 overused Command. Oder, {}? 🤨",
      "Halt die Fresse, {}.",
      "Wieso ist {} immer noch hier?",
      "Könnte nur von Laufamholzer kommen.",
      "Kein Bock mehr, {}."
    ]
    await self.client.send_message(ctx.message.channel, random.choice(dab_messages).format(ctx.message.author.name), tts=True)


def setup(client):
  client.add_cog(Fun(client))