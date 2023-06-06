import discord
import pymongo
import aiohttp
import time
import json
from discord.ext import commands

with open('config.json') as f:
    data = json.load(f)

client = pymongo.MongoClient(data["mongodb"])
db = client.test

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Access any subreddit - Bot Owner Only")
    @commands.is_owner()
    async def subreddit(self, ctx, subreddit : str):
        if ctx.channel.is_nsfw():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f'https://meme-api.com/gimme/{subreddit}') as f:
                    response = await f.json()
                    em = discord.Embed(title=f"Meme By {response['author']}", description=f"[{response['title']}]({response['postLink']})", color=discord.Colour.blurple())
                    em.set_image(url=response["url"])
                    em.set_footer(text=f"{response['ups']} Upvotes      ●      r/{response['subreddit']}")
                    await ctx.respond(embed=em)
        else:
            await ctx.respond("Sorry, this command is only for NSFW channels.")

def setup(bot):
    bot.add_cog(Owner(bot))