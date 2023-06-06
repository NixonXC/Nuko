import discord
import pymongo
import random
import asyncio
import aiohttp
from discord.ui import Button, View
from discord import Activity, ActivityType
from discord.ext import commands
from datetime import datetime
import json
import time
import os
import psutil
import apicalls

with open('config.json') as f:
    data = json.load(f)

intents = discord.Intents.all()

client = pymongo.MongoClient(data["mongodb"])
db = client.test

bot = commands.Bot(command_prefix=data["prefix"], intents=intents)
@bot.remove_command("help")

@bot.slash_command()
async def help(ctx):
    em = discord.Embed(title="Help", description="All the available help commands.", color=discord.Colour.blurple())
    em.add_field(name="Welcome Commands", value="`setwelcomechannel` , `delwelcomechannel` , `setleavechannel` , `delleavechannel` , `setwelcomemessage` , `delwelcomemessage` , `setleavemessage` , `delleavemessage` , `testwelcome` , `testleave`")
    em.add_field(name="Fun Commands", value="`joke` , `darkjoke` , `fact` , `roast <user>` , `question` , `quote` , `meme`", inline=False)
    em.add_field(name="Util & Bot", value="`avatar` , `coinflip` , `userinfo` , `uptime` , `ping` , `stats` , `servers` , `tutorial`")
    em.add_field(name="Owner", value="`subreddit`", inline=False)
    await ctx.respond(embed=em)

startup_time = datetime.now()

@bot.slash_command()
async def tutorial(ctx):
    em = discord.Embed(title="How to setup Welcome/leave commands:", color=discord.Colour.nitro_pink())
    em.add_field(name="Step 1. Set the Welcome/Leave Channel", value="You can setup the welcome/leave logging system by using the commands: `/setwelcomechannel` or `/setleavechannel`, there is one required parameter in the command which is `channel`, you will have to select the channel where you want the Welcome and leave logs to be displayed.", inline=False)
    em.add_field(name="Step 2. Set the Welcome/Leave Message", value="You can setup the welcome/leave message by using the commands: `/setwelcomemessage` or `setleavemessage`, there are four required parameters in the commands which are `embed_title`, `message` , `embed_image` , `embed_color`, you will have to full out the parameters with your desired options, If you want the embed_image to be `none` or nothing you can insert any random URL that does not contain an image like `https://google.com/`, and if you want to access the user like mentioning them or getting their username and discriminator then you can use the `{user}` module which allows you to mention or get the name and discriminator of the new member like `{user.mention}` will mention the newly joined member.", inline=False)
    em.add_field(name="That's It!", value="And that's it, if you need any help regarding the welcome system or any other commands then you can join the support server for more information", inline=False)
    await ctx.respond(embed = em)

@bot.slash_command()
async def servers(ctx):
    em = discord.Embed(title="Servers", description=f"I'm in {len(bot.guilds)} servers", color=discord.Colour.blurple())
    await ctx.respond(embed=em)

@bot.slash_command()
async def stats(ctx):
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    ram_usage = memory.used / 1024 / 1024
    ram_total = memory.total / 1024 / 1024
    ram_percent = memory.percent
    disk_usage = psutil.disk_usage('/')
    total_space = disk_usage.total / (1024 ** 3)  # Convert bytes to gigabytes
    used_space = disk_usage.used / (1024 ** 3)
    percent_used = disk_usage.percent
    em = discord.Embed(title="Nuko Stats", description="Check my statistics like Ram, Storage, CPU, Ping", colour=discord.Colour.blurple())
    em.add_field(name="Latency", value=f"{bot.latency * 1000:.2f}ms", inline=False)
    em.add_field(name="CPU Usage", value=f"{cpu_percent}%", inline=False)
    em.add_field(name="RAM Usage", value=f"{ram_usage:.2f} MB / {ram_total:.2f} MB ({ram_percent}%)", inline=False)
    em.add_field(name="Storage", value=f"{used_space:.2f} GB / {total_space:.2f} GB ({percent_used}%)", inline=False)
    await ctx.respond(embed = em)

@bot.slash_command(description="Show how long the bot has been running since it was last started.")
async def uptime(ctx):
    current_time = datetime.now()
    uptime = current_time - startup_time

    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    uptime_str = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

    em = discord.Embed(title="Bot Uptime", description=uptime_str, color=discord.Colour.blurple())
    await ctx.respond(embed=em)

@bot.slash_command(description="Check the bot's ping latency.")
async def ping(ctx):
    start_time = time.time()
    message = await ctx.respond("Pinging...")
    latency = (time.time() - start_time) * 1000
    await message.edit_original_response(content=f"Pong! **Latency:** {latency:.2f}ms | **API Latency:** {bot.latency * 1000:.2f}ms")

@bot.event
async def on_member_join(member):
    db = client['nuko']
    channels = db['channels']
    messages = db["messages"]
    query = channels.find_one({"guild_id": member.guild.id})
    query2 = messages.find_one({"guild_id": member.guild.id})
    if not query and query2:
        return
    else:
        channel = bot.get_channel(query["channel_id"])
        toSend = query2["message"].replace("{user}", f"{member.name}#{member.discriminator}")
        toSend = toSend.replace("{user.mention}", member.mention)
        color = getattr(discord.Colour, query2["embed_color"])()
        em = discord.Embed(title=query2["embed_title"], description=toSend, color=color)
        em.set_image(url=query2["embed_image"])
        return await channel.send(embed=em)

@bot.event
async def on_member_remove(member):
    db = client['nuko']
    channels = db['leavechannel']
    messages = db["leaves"]
    query = channels.find_one({"guild_id": member.guild.id})
    query2 = messages.find_one({"guild_id": member.guild.id})
    if not query and query2:
        return
    else:
        channel = bot.get_channel(query["channel_id"])
        toSend = query2["message"].replace("{user}", f"{member.name}#{member.discriminator}")
        toSend = toSend.replace("{user.mention}", member.mention)
        color = getattr(discord.Colour, query2["embed_color"])()
        em = discord.Embed(title=query2["embed_title"], description=toSend, color=color)
        em.set_image(url=query2["embed_image"])
        return await channel.send(embed=em)

@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.respond(f"Error 213: Missing Permission | You do not have sufficient permession to use this command.", ephemeral=True)
    else:
        pass

def get_recomend():
    obj = apicalls.fetch_song()
    string = obj['song'] + " - " + obj['artist']
    return string

statuses = [
    discord.Game(name="Minecraft"),
    discord.Streaming(name="How to setup Nuko.", url="https://www.youtube.com/watch?v=_HAuSkW-1ek"),
    discord.Activity(type=discord.ActivityType.listening, name=get_recomend()),
    discord.Activity(type=discord.ActivityType.watching, name="Naruto | Season 283293 | Episode 3923829")
]

async def change_status():
    while True:
        for status in statuses:
            await bot.change_presence(activity=status)
            await asyncio.sleep(50)

@bot.event
async def on_ready():
    print("Hello World, Nuko is alive!")
    bot.loop.create_task(change_status())

for f in os.listdir("./cogs"):
    if f.endswith(".py"):
        cog_name = "cogs." + f[:-3]
        try:
            bot.load_extension(cog_name)
            print(f"Cog [{cog_name}] Loaded Successfully.")
        except Exception as e:
            print(f"An error occurred while loading [{cog_name}]: {str(e)}")

bot.run(data["token"])
