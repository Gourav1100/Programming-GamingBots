# import libraries
'''import asyncio'''
import discord
from discord.ext import tasks
import os
import json
import requests
from replit import db           # this is for our data base
# custom library
from keep_alive import keep_alive


# custom functions
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data=json.loads(response.text)
  quote=json_data[0]['q']+"\n - "+json_data[0]['a']
  return quote


def initcommands():
  # commands : response dictionary
  commands = {
  "$help"       : "Return description of all commands available",
  "$quote"      : "Return a quote with Author Name",
  "$start_quotes": "Start to send quotes on general channel with an interval of 1 hour",
  "$members"    : "Return the number of members on server"
  }
  db["commands"]=commands


# start a discord client
initcommands()
client = discord.Client()

#to tell if the bot is ready or not
@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))


# to wait asynchronously for message
@client.event
async def on_message(message):
  server_id=client.get_guild(836125212533456946)
  msg=str(message.content)
  msg=msg.lower()
  # for stoping bot from responding to itself
  if(message.author==client.user):
    return
  # defining functionality as per channel
  if(message.channel == client.get_channel(836125215393316887)):
    await message.delete()  # for keeping general channel clean
    await message.channel.send(f"{message.author.mention}, Please keep this channel clean.")
  elif(message.channel == client.get_channel(836162585975586837)):  
    if (msg.startswith("$help")):
      if(msg=="$help"):
        await message.channel.send("Following commands are available: ")
        for i in db["commands"].keys():
          await message.channel.send(i+" : "+db["commands"][i]+"\n")
      else:
        msg=msg.split()[1]
        if(str("$"+msg) in db["commands"].keys()):
          await message.channel.send("Description for $"+msg+" : \n"+db["commands"][str("$"+msg)])
        else:
          await message.channel.send("No Description found for $"+str(msg)+" \n Type $help to get list of all commands")
    elif(msg.startswith('$quote')):
      quote=get_quote()
      await message.channel.send(quote)
    elif(msg.startswith("$start_quotes")):
      await message.channel.send("started")
      await send_quotes.start()
    elif(msg.startswith("$members")):
      await message.channel.send(f"Number of members: {server_id.member_count}")
      
@tasks.loop(minutes = 1440.0)
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


# run bot
keep_alive() # keep bot up
client.run(os.getenv("TOKEN"))