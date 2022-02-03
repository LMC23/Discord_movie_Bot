import discord
import os
import asyncio
import datetime 
from discord.ext import commands
import time
from keep_alive import keep_alive
import requests 

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))

#Check if tickets for a movie are available:

@bot.command()
async def checkmovie(ctx):
  url = 'https://www.cinemacity.ro/ro/data-api-service/v1/quickbook/10107/film-events/in-cinema/1807/at-date/2021-12-17?attr=&lang=ro_RO'
  no_of_calls = 0

  #always running
  while True: 

    response = requests.get(url)
  
    json_response = response.json()
    
    #getting the movies list of dictionaries from API response
    all_movies = json_response['body']['films']
    found = False
    linkul = None

    for movie in all_movies:
      name = movie['name'].lower()

      #checking if the movie name contains specific key words
      if 'spider' in name or 'omul' in name or 'niciun drum' in name:
        found = True
        linkul = movie['link']
        break
    
    #sending messages based on the boolean value
    if found == True:
      message = f'L-am gasit. Intra aici pentru bilete: {linkul}'
      await ctx.message.author.send(message)
      break
    else:
      message = f'Not found: {datetime.datetime.now()}'
      await ctx.message.author.send(message)

    #checking if the API has been interogated 6 times (initial value is 0) and send message
    if no_of_calls == 5:
      await ctx.message.author.send('Still checking...')
      no_of_calls = 0

    no_of_calls = no_of_calls + 1

    #reactivating loop every 1h
    await asyncio.sleep(3600)

keep_alive()
bot.run(os.environ['token'])


