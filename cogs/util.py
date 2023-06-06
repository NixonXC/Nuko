import discord
import pymongo
import asyncio
import json
import random
from datetime import datetime
from discord.ext import commands

with open('config.json') as f:
    data = json.load(f)

client = pymongo.MongoClient(data["mongodb"])
db = client.test

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Do a coinflip!")
    async def coinflip(self, ctx):
        em = discord.Embed(title="Coinflip", description="Flipping the coin...", color=discord.Colour.nitro_pink())
        em.set_thumbnail(url="https://i.pinimg.com/originals/d7/49/06/d74906d39a1964e7d07555e7601b06ad.gif")
        msg = await ctx.respond(embed = em)
        await asyncio.sleep(1.2)
        choices = ["Heads!", "Tails!", "Both???"]
        em.description = random.choice(choices)
        await msg.edit_original_response(embed = em)

    @discord.slash_command(description="Get the avatar/profile picture of a user.")
    async def avatar(self, ctx, user: discord.User):
        if user == None:
            user = ctx.author
        em = discord.Embed(title=user, color=discord.Colour.blurple())
        em.set_image(url=user.avatar)
        await ctx.respond(embed=em)


    @discord.slash_command(description="Get information about a specific user.")
    async def userinfo(self, ctx, user: discord.Member):
        em = discord.Embed(title=user, color=discord.Colour.blurple())
        em.add_field(name="Display Name:", value=user.display_name, inline=False)
        em.add_field(name="Name and Discriminator:", value=f"{user.name}#{user.discriminator}", inline=False)
        em.add_field(name="User ID:", value=f"{user.id}", inline=False)
    
        if user.status == discord.Status.online:
            status_text = "Online  <:online:1114841377541455953>"
        elif user.status == discord.Status.offline:
            status_text = "Offline  <:offline:1114843428086362173>"
        elif user.status == discord.Status.idle:
            status_text = "Idle  <:idle:1114841396898189375>"
        elif user.status == discord.Status.dnd:
            status_text = "Do Not Disturb  <:dnd:1114841420205936740>"
        else:
            status_text = "Unknown"
    
        em.add_field(name="Current Status:", value=status_text, inline=False)
        joined_date = user.joined_at.strftime("%Y-%m-%d %H:%M:%S")
        em.add_field(name="Joined Date:", value=joined_date, inline=False)
    
        # Formatting Account Creation Date
        creation_date = datetime.utcfromtimestamp(user.created_at.timestamp()).strftime("%Y-%m-%d %H:%M:%S")
        em.add_field(name="Account Creation Date:", value=creation_date, inline=False)

        em.set_thumbnail(url=user.avatar)
        await ctx.respond(embed=em)

def setup(bot):
    bot.add_cog(Util(bot))