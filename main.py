import os
import discord
import time
import ast
import requests
import random


from discord.ext import commands
from running import *

from discord.utils import get
from translate import Translator

runType = 2


debug_mode = "off"
client = commands.Bot(command_prefix="",intents=discord.Intents.all())
currencybot = commands.Bot(command_prefix="p:",intents=discord.Intents.all())


@client.event
async def on_ready():
  global availablewords
  global data_storage_msg
  global data
  global msg_count
  msg_count = 0
  words = str(requests.get('http://www.instructables.com/files/orig/FLU/YE8L/H82UHPR8/FLUYE8LH82UHPR8.txt').content)
  words = words.split('\\n')
  availablewords = []
  for i in range(len(words)):
    wordinstance = words[i]
    if len(wordinstance) >= 5:
      availablewords.append(wordinstance)

  data_storage_msg = await client.get_channel(1046118935453507655).fetch_message(1046147460386521088)
  data = ast.literal_eval(data_storage_msg.content)
  # await data_storage_msg.edit(content='''{"dailyWordleWord":"","infiniteWordleWord":{},"dailyWordleProgress": {},"infiniteWordleProgress":{}}''')

  
  await client.change_presence(activity=discord.Game('with my dad pumpkin'))

@client.event
async def on_message(message):
  global availablewords
  global data
  global data_storage_msg
  global msg_count




  
  
  if message.content == "!admin_clear":
    data = {'dailyWordleWord': '', 'infiniteWordleWord': {}, 'dailyWordleProgress': {}, 'infiniteWordleProgress': {}}
    await data_storage_msg.edit(content = str(data))
    await message.channel.send("Success!")
    
    
  elif message.author.bot == False:
    
    currentServer = message.guild.name
    try:
      iwWord = data['infiniteWordleWord'][currentServer]
    except:
      iwWord = availablewords[random.randint(0,len(availablewords)-1)]
      data['infiniteWordleWord'][currentServer] = iwWord
  
    print(iwWord)
  
    try:
      iwProgress = data['infiniteWordleProgress'][currentServer]
    except:
      data['infiniteWordleProgress'][currentServer] = {}
  
    
    
    
  
    message_content = message.content.lower()
    if message_content == "!wordlerules":
        await message.channel.send('There are 2 different types of wordle: the infinite wordle, and the daily wordle. continuous_wordle would generate a new word every time somebody gets it correct; while daily wordles would only re-generate each day.')


      
  
    if "infinite-wordle" in message.channel.name.lower():

      try:
        triesLeft = data['infiniteWordleProgress'][currentServer][message.author.name] > 0
      except:
        triesLeft = True
      restarted = False

      

      if message.content.lower() == "!restart":
        await message.channel.send("Meow: "+message.author.name+" restarted the wordle! The answer was: "+ data['infiniteWordleWord'][currentServer])
        nextIWWord = availablewords[random.randint(0,len(availablewords)-1)]
        print(nextIWWord)
        await message.channel.send('The next wordle has '+str(len(nextIWWord))+" letters. Everybody will get up to "+str(len(nextIWWord)+1)+" tries.")
      
        data['infiniteWordleWord'][currentServer] = nextIWWord
        data['infiniteWordleProgress'][currentServer] = {}
        restarted = True



      
      if len(message_content) >= 5 and not " " in message_content and not restarted:
        if message_content == data['infiniteWordleWord'][currentServer] and triesLeft:


          
          await message.add_reaction("\N{THUMBS UP SIGN}")
          await message.channel.send('Congradulations **'+message.author.name+"** for solving the wordle! Pumpkin Jr is very happy!")
          nextIWWord = availablewords[random.randint(0,len(availablewords)-1)]
          print(nextIWWord)
          await message.channel.send('The next wordle has '+str(len(nextIWWord))+" letters. Everybody will get up to "+str(len(nextIWWord)+1)+" tries.")
        
          data['infiniteWordleWord'][currentServer] = nextIWWord
          data['infiniteWordleProgress'][currentServer] = {}



          
        elif triesLeft:
          
          ansLetterList = list(data['infiniteWordleWord'][currentServer])
          print(ansLetterList)
          userLetterList = list(message.content.lower())
          print(userLetterList)
          validationsequence = []

          if len(ansLetterList) == len(userLetterList):
            for i in range(len(ansLetterList)):
              if ansLetterList[i] == userLetterList[i]:
                validationsequence.append(":white_check_mark:")
                ansLetterList[i] = "*"
              else:
                validationsequence.append("*")
            print(ansLetterList)

            for i in range(len(ansLetterList)):
              if ansLetterList[i] != "*":
                if userLetterList[i] in ansLetterList:
                  validationsequence[i] = ":yellow_square:"
                else:
                  validationsequence[i] = ":red_square:"
            validationsequence = "".join(validationsequence) 
            displayedAns = ""
            for i in range(len(userLetterList)):
              displayedAns += ":regional_indicator_"+userLetterList[i]+":"
            
            await message.add_reaction("\N{THUMBS DOWN SIGN}")
            await message.author.send("Meow! Pumpkin Jr is not pleased with your wordle answer. \n"+ displayedAns+"\n"+validationsequence)
            try:
              data['infiniteWordleProgress'][currentServer][message.author.name] -= 1
              if data['infiniteWordleProgress'][currentServer][message.author.name] == 0:
                await message.author.send("Meow.... you have ran out of guesses. The answer was: "+ data['infiniteWordleWord'][currentServer])
                await message.author.send("To restart, type !restart in the server channel.")
                
            except:
              data['infiniteWordleProgress'][currentServer][message.author.name] = len(data['infiniteWordleWord'][currentServer])


              
          else:
            await message.channel.send("Meow meow, your word should only be "+str(len(ansLetterList))+" letters long.")
          # await data_storage_msg.edit(content='{"currentword":{},"progress": {}}')

        else:
          await message.channel.send("You have ran out of guesses. Type !restart if you want to reset the wordle.")


    
    elif message.channel.name.lower() == "daily-wordle":
      print("hi")
  
    await data_storage_msg.edit(content=str(data))
  



running()



try:
  client.run(os.environ['token'])
except:
  requests.get('https://PingMachine.danielchen1464.repl.co/botIsDown?name=pumpkinJr')
