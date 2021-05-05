# import libraries
'''import asyncio'''
import discord
from discord.ext import tasks
import os
import json
import requests
from replit import db           # this is for our data base
import random
# custom library
from keep_alive import keep_alive


# custom functions
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data=json.loads(response.text)
  quote=json_data[0]['q']+"\n - "+json_data[0]['a']
  return quote
def get_comp():
  option = ["Codeforces","CSES", "DMOJ", "LeetCode"]
  opt=random.choice(option)
  ranges = {
    "Codeforces":{
      " 800 1200":80,
      " 1200 1600":90,
      " 1600 2000":100,
      " 2000 2400":60,
      " 2400 2800":40,
      " 2800 3200":20,
      " 3200 3500":10
    },
    "DMOJ":{
      " 5 10":60,
      " 10 20":80,
      " 20 30":100,
      " 30 40":80,
      " 40 45":60,
    },
    "CSES":{
      " ":100
    },
    "LeetCode":{
      " 1": 60,
      " 2": 100,
      " 3": 70
    }
  }
  n=len(ranges[opt])
  probability=dict()
  for i in ranges[opt].keys():
    probability[i]=ranges[opt][i]/n
  test = [random.choice(list(probability.keys())) for i in range(10)]
  test2 = dict()
  for i in test:
    if i not in test2.keys():
      test2[i]=1
    else:
      test2[i]+=1
  n=len(test2)
  for i in test2.keys():
    test2[i]=(test2[i]/n)*(probability[i])
  maxi=max(test2.values())
  key=""
  for i in test2.keys():
    if(test2[i]==maxi):
      key=i
      break
  return "~random "+opt+key

def initcommands():
  # commands : response dictionary
  commands = {
  "$help"       : "Return description of all commands available",
  "$quote"      : "Return a quote with Author Name",
  "$start quotes": "Start to send quotes on general channel with an interval of 24 hour",
  "$start competitive": "Start to send competitive coding questions on channel competitive with an interval of 1 hour",
  "$members"    : "Return the number of members on server"
  }
  if(db['commands']!=commands):
    db["commands"]=commands


# start a discord client
initcommands()

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

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
    if msg != "":
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
    elif(msg.startswith("$start")):
      msg=msg.split()
      if(len(msg) == 2):
        if("quotes" in msg):
          await send_quotes.start()
        if("competitive" in msg):
          await send_competitive.start()
        else:
          await message.channel.send("Invalid Command!")
          return 
        await message.channel.send("started")
    elif(msg.startswith("$members")):
      await message.channel.send(f"Number of members: {server_id.member_count}")
    elif( msg.startswith("$competitive")):
      await message.channel.send(f"{get_comp()}")
      
@tasks.loop(minutes = 1440.0)
async def send_quotes():
  channel = client.get_channel(836125215393316887)
  quote=get_quote()
  await channel.send(quote)

@tasks.loop(minutes = 60.0)
async def send_competitive():
  channel = client.get_channel(836130690860711957)
  command=get_comp()
  # send command for random question
  await channel.send(command)


# when new user joins the server
@client.event
async def on_member_join(member):
  server = "Programming and Gaming"
  channel = client.get_channel(836125215393316887)
  message = f"Hello {member.mention}, Welcome to {server}"
  await channel.send(message)


# run bot
keep_alive() # keep bot up
client.run(os.getenv("TOKEN"))