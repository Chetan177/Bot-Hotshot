#---------------------------------------- Author------------------------------------#
#Chetan Pandey 
#12-09-2018
#Github   : https://github.com/Chetan177/
#chetanpandey177@gmail.com
#
#
#---------------------------------------- Author------------------------------------#

import discord
import youtube_dl
import json
import os
from discord.ext import commands
import urllib.request
import urllib.parse
import re
import praw
import random

TOKEN = 'NDc4ODEyNzIzOTE2ODMyNzY5.DlQQ4A.GGgNTgTDaAGvWP0WOlkA_IZn--Y'
# Reddit instance

reddit = praw.Reddit(client_id='Yp2kpHRzd7tyZg',
                     client_secret='1EULWEQCN11DLniv7EyAKRytkNs',
                     user_agent='ImageBot')

client = commands.Bot(command_prefix='.')
players = {}
queues = {}
os.chdir(r'D:\Internship\Discord Bot\Bot_HotShots')





#---------------------------------------- Music Player------------------------------------#
def check_queue(id):
    if queues[id] !=[]:
        player = queues[id].pop()
        players[id] = player
        player.start()

@client.event
async def on_ready():
    print("Bot Online")



@client.command(pass_context=True)
async def joinme(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)



@client.command(pass_context=True)
async def play (ctx,song,a,b=" "):
    server = ctx.message.server
    if len(players) != 0:
        players[server.id].stop()

    if (client.is_voice_connected(server)==False):
        channel = ctx.message.author.voice.voice_channel
        await client.join_voice_channel(channel)


    detail=song+" "+a+" "+b
    query_string = urllib.parse.urlencode({"search_query" : detail})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    url ="http://www.youtube.com/watch?v=" + search_results[0]

    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url,after= lambda: check_queue(server.id))
    players[server.id] = player
    player.start()
    current_status = "Playing Music"
    await client.change_presence(game=discord.Game(name=current_status))


@client.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()
    await client.change_presence(status = None )

@client.command(pass_context=True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()
    server=ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()
    await client.change_presence(status = None )

@client.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()
    current_status = "Playing Music"
    await client.change_presence(game=discord.Game(name=current_status))

@client.command(pass_context=True)
async def queue(ctx,song,a,b=""):
    detail=song+" "+a+" "+b
    query_string = urllib.parse.urlencode({"search_query" : detail })
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    url ="http://www.youtube.com/watch?v=" + search_results[0]
    server = ctx.message.server
    voice_client=client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    await client.say('Video queued   {}'.format(url))

@client.command(pass_context=True)
async def  nextsong(ctx):
    id = ctx.message.server.id
    players[id].stop()
    if queues[id] !=[]:
        player = queues[id].pop()
        players[id] = player
        player.start()

#---------------------------------------- Music Player------------------------------------#
#---------------------------------------- Fun commands------------------------------------#
# spam message
@client.command(pass_context=True)
async def spam(ctx,word,t):
    channel=ctx.message.channel
    for x in range(0,int(t)):
        await client.send_message(channel,word)
# text to speech
@client.command(pass_context=True)
async def sayloud(ctx,word,a="",b="",c="",d="",e="",f=""):
    channel=ctx.message.channel
    await client.send_message(channel,word+" "+a+" "+b+" "+c+" "+d+" "+e+" "+f,tts=True)

# search Meme
@client.command(pass_context=True)
async def meme(ctx):
    channel=ctx.message.channel

    image= imageurl()
    await client.send_message(channel,image)


# search Image
@client.command(pass_context=True)
async def imagesearch(ctx,i):
    channel=ctx.message.channel
    image=imageurl(i)
    await client.send_message(channel,image)

#---------------------------------------- Fun commands------------------------------------#

def imageurl(img='memes'):

    memes_submissions = reddit.subreddit(img).hot()
    post_to_pick = random.randint(1, 10)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)
    return submission.url

#---------------------------------------- Help Embed ------------------------------------#
@client.command(pass_context=True)
async def bothelp(ctx):
    channel=ctx.message.channel
    embed=discord.Embed(title="Help ", description="These are the commands (prefix = . dot)", colour=discord.Colour.blue())
    embed.set_author(name="@Bot")
    embed.add_field(name='Music Player commands', value=':-------------------------------:', inline=False)
    embed.add_field(name='.play', value='Play music' , inline=True)
    embed.add_field(name='.stop', value='Stop music', inline=True)
    embed.add_field(name='.queue', value='Queue a song' , inline=True)
    embed.add_field(name='.pause', value='Pause Song', inline=True)
    embed.add_field(name='.resume', value='Resume song', inline=True)
    embed.add_field(name='.nextsong', value='Next song', inline=True)
    embed.add_field(name='Fun commands', value=':-------------------------------:', inline=False)
    embed.add_field(name='.spam (message , times)', value='Spam a message multiple time' , inline=True)
    embed.add_field(name='.sayloud', value='Bot Says', inline=True)
    embed.add_field(name='.meme', value='To get some memes', inline=False)
    embed.add_field(name='.imagesearch', value='To get image', inline=False)
    await client.send_message(channel,embed=embed)

#---------------------------------------- Help Embed ------------------------------------#
#---------------------------------------- Event ------------------------------------#


@client.event
async def on_member_join(member):

    client.say('{}  hoped into the server'.format(member.mention))
    with open('userlvl.json','r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('userlvl.json','w') as f:
        json.dump(users, f)


@client.event
async def on_message(message):
    with open('userlvl.json','r') as f:
        users = json.load(f)

    await update_data(users, message.author)
    await add_experience(users , message.author,5)
    await level_up(users,message.author,message.channel)



    with open('userlvl.json','w') as f:
        json.dump(users, f)
    await client.process_commands(message)

#---------------------------------------- Event ------------------------------------#

#---------------------------------------- Level System functions ------------------------------------#

async def update_data(users ,user):
    if not user.id in users:
        users[user.id] ={}
        users[user.id]['experience']=0
        users[user.id]['level'] = 1


async def add_experience(users,user,exp):
    users[user.id]['experience']+= exp

async def level_up(users,user,channel):
    experience = users[user.id]['experience']
    lvl_start = users[user.id]['level']
    lvl_end = int(experience **(1/4))

    if lvl_start < lvl_end:
        await client.send_message(channel,'{} has leveled up to level {}'.format(user.mention,lvl_end))
        users[user.id]['level'] = lvl_end

#---------------------------------------- Level System functions ------------------------------------#

client.run(TOKEN)
