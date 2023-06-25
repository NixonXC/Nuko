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
import requests
import psutil
import apicalls

from PIL import Image, ImageDraw, ImageOps, ImageFont
from io import BytesIO

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
    em.add_field(name="Welcome Commands", value="`setwelcomechannel` , `delwelcomechannel` , `setleavechannel` , `delleavechannel` , `setwelcomemessage` , `delwelcomemessage` , `setleavemessage` , `delleavemessage`")
    em.add_field(name="Fun Commands", value="`joke` , `darkjoke` , `fact` , `roast <user>` , `question` , `quote` , `meme`", inline=False)
    em.add_field(name="Util & Bot", value="`avatar` , `coinflip` , `userinfo` , `uptime` , `ping` , `stats` , `servers`")
    em.add_field(name="Owner", value="`subreddit`", inline=False)
    await ctx.respond(embed=em)

startup_time = datetime.now()

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
    
    if not query or not query2:
        return
    
    channel = bot.get_channel(query["channel_id"])
    url = query2["image_url"]
    background_response = requests.get(url)
    background_response.raise_for_status()
    background_data = BytesIO(background_response.content)
    img = Image.open(background_data)
    fontXL = ImageFont.truetype("fonts/robotom.ttf", 75)
    fontX = ImageFont.truetype("fonts/popregular.ttf", 37)
    fontXC = ImageFont.truetype("fonts/mid.ttf", 40)
    
    if img.size != (1500, 500):
        img = img.resize((1500, 500))
    
    uavatar = member.avatar
    data = BytesIO(await uavatar.read())
    pfp = Image.open(data).convert("RGBA")
    pfp = pfp.resize((367, 375))

    mask = Image.new("L", pfp.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, pfp.width, pfp.height), fill=255)

    rounded_pfp = ImageOps.fit(pfp, mask.size)
    rounded_pfp.putalpha(mask)

    bordered_pfp = ImageOps.expand(rounded_pfp)

    img.paste(bordered_pfp, (143, 60), mask=bordered_pfp)

    welcome = query2["image_title"]
    username = "@" + str(member)
    userid = "Creation Date: " + member.created_at.strftime("%d %B, %Y | %H:%M")
    message = query2["message"]
    message = message.replace("{user.name}", f"{member.name}")
    message = message.replace("{user}", f"{member}")
    message = message.replace("{user.mention}", f"{member.name}")
    print(message)

    if len(message) > 40:
        message_lines = [message[i:i + 40] for i in range(0, len(message), 40)]
        message = "\n".join(message_lines)

    draw = ImageDraw.Draw(img)
    draw.text((820, 55), f"{welcome}", (20, 17, 20), font=fontXL)
    draw.text((610, 170), username, (20, 17, 20), font=fontXC)
    draw.text((610, 235), userid, (20, 17, 20), font=fontX)
    draw.text((610, 290), message, (20, 17, 20), font=fontX)

    profile_path = "rounded_profile.png"
    img.save(profile_path)

    with open(profile_path, "rb") as f:
        profile_image = discord.File(f, filename=profile_path)
    
    if query2["mention_user"] == "true":
        await channel.send(f"{member.mention}", file=profile_image)
    else:
        await channel.send(file=profile_image)

@bot.event
async def on_member_remove(member):
    db = client['nuko']
    channels = db['leavechannel']
    messages = db["leaves"]
    query = channels.find_one({"guild_id": member.guild.id})
    query2 = messages.find_one({"guild_id": member.guild.id})
    
    if not query or not query2:
        return
    channel = bot.get_channel(query["channel_id"])
    url = query2["image_url"]
    background_response = requests.get(url)
    background_response.raise_for_status()
    background_data = BytesIO(background_response.content)
    img = Image.open(background_data)
    fontXL = ImageFont.truetype("fonts/robotom.ttf", 75)
    fontX = ImageFont.truetype("fonts/popregular.ttf", 37)
    fontXC = ImageFont.truetype("fonts/mid.ttf", 40)
    
    if img.size != (1500, 500):
        img = img.resize((1500, 500))
    
    uavatar = member.avatar
    data = BytesIO(await uavatar.read())
    pfp = Image.open(data).convert("RGBA")
    pfp = pfp.resize((367, 375))

    mask = Image.new("L", pfp.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, pfp.width, pfp.height), fill=255)

    rounded_pfp = ImageOps.fit(pfp, mask.size)
    rounded_pfp.putalpha(mask)

    bordered_pfp = ImageOps.expand(rounded_pfp)

    img.paste(bordered_pfp, (143, 60), mask=bordered_pfp)

    title = query2["image_title"]
    username = "@" + str(member)
    userid = "Creation Date: " + member.created_at.strftime("%d %B, %Y | %H:%M")
    message = query2["message"]
    message = message.replace("{user}", f"{member}")
    message = message.replace("{user.mention}", f"{member.name}")
    message = message.replace("{user.name}", f"{member.name}")
    print(message)

    if len(message) > 40:
        message_lines = [message[i:i + 40] for i in range(0, len(message), 40)]
        message = "\n".join(message_lines)

    draw = ImageDraw.Draw(img)
    draw.text((820, 55), f"{title}", (20, 17, 20), font=fontXL)
    draw.text((610, 170), username, (20, 17, 20), font=fontXC)
    draw.text((610, 235), userid, (20, 17, 20), font=fontX)
    draw.text((610, 290), message, (20, 17, 20), font=fontX)

    profile_path = "deltapath.png"
    img.save(profile_path)

    with open(profile_path, "rb") as f:
        profile_image = discord.File(f, filename=profile_path)
    
    if query2["mention_user"] == "true":
        await channel.send(f"{member.mention}", file=profile_image)
    else:
        await channel.send(file=profile_image)

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

async def update():
    inp = input("Do you want to announce any updates? Type 'Yes' to confirm:\n")
    if inp == "Yes":
        channel = input("Select Channel:\n1. [📢] announcement\n2. [🤖] bot-updates\n")
        if channel == "1":
            content = input("Write the Announcement Content:\n")
            channel = bot.get_channel(1109754654331519029)
            await channel.send(content)
        elif channel == "2":
            content = input("Write the Bot Update Content:\n")
            channel = bot.get_channel(1119700162013577294)
            await channel.send(content)
        else:
            print("Please select a valid channel")
    else:
        return
    
@bot.event
async def on_ready():
    await update()
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