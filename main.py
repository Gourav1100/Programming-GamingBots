# import libraries
import discord
import os
import json
import requests
import asyncio
from keep_alive import keep_alive
# start a discord client
client = discord.Client()
# 
from discord.ext import tasks
#to tell if the bot is ready or not
@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

# to wait asynchronously for message
@client.event
async def on_message(message):
  server_id=client.get_guild(836125212533456946)
  msg=message.content
  if(message.author==client.user):
    return
  if(message.channel == client.get_channel(836125215393316887)):
    await message.delete()
    await message.channel.send(f"{message.author.mention}, Please keep this channel clean.")
  elif(message.channel == client.get_channel(836162585975586837)):  
    if(msg.startswith('$help')):
      await message.channel.send("Help will be available soon!")
    elif(msg.startswith('$quote')):
      quote=get_quote()
      await message.channel.send(quote)
    elif(msg.startswith("$start_quotes")):
      await message.channel.send("started")
      await send_quotes()
    elif(msg.startswith("$members")):
      await message.channel.send(f"Number of members: {server_id.member_count}")
@tasks.loop(seconds=3600.0)
async def send_quotes():
  channel = client.get_channel(836125215393316887)
  quote=get_quote()
  await channel.send(quote)

# when new user joins the server
@client.event
async def on_member_join(member):
  print("here")
  server = member.server
  channel = client.get_channel(836125215393316887)
  message = f"Hello {member.mention}, Welcome to {server.name}"
  await channel.send(message)


# custom functions
def get_quote(author="random"):
  response = requests.get("https://zenquotes.io/api/"+author)
  json_data=json.loads(response.text)
  quote=json_data[0]['q']+"\n - "+json_data[0]['a']
  return quote
# run bot
keep_alive() # keep bot up
client.run(os.getenv("TOKEN"))