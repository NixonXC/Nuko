import discord
import json
import pymongo
import aiohttp
import apicalls
from discord.ext import commands

with open('config.json') as f:
    data = json.load(f)

client = pymongo.MongoClient(data["mongodb"])
db = client.test

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def joke(self, ctx):
        result = await apicalls.fetch_joke()
        await ctx.respond(result["setup"] + "? " + result["punchline"])

    @discord.slash_command(description="Returns a random fun fact!")
    async def fact(self, ctx):
        result = await apicalls.fetch_fact()
        await ctx.respond(result["fact"])

    @discord.slash_command(description="Returns a Random Question.")
    async def question(self, ctx):
        result = await apicalls.fetch_question()
        await ctx.respond(result["question"])

    @discord.slash_command(description="Returns a darkjoke(NSFW)")
    async def darkjoke(self, ctx):
        if ctx.channel.is_nsfw():
            result = await apicalls.fetch_darkjoke()
            await ctx.respond(result["setup"] + "? " + result["punchline"])
        else:
            await ctx.respond("Sorry, this command is only for NSFW channels.")

    @discord.slash_command(description="Returns a Quote from Peter API")
    async def quote(self, ctx):
        result = await apicalls.fetch_quote()
        main_quote = result["quote"]
        author = result["author"]
        await ctx.respond(f'*" {main_quote} "*' + "\n\n          - " + f"**{author}**")

    @discord.slash_command(description="Returns a Roast from Peter API")
    async def roast(self, ctx, user : discord.User):
        result = await apicalls.fetch_roast(user)
        await ctx.respond(result["roast"])

    @discord.slash_command(decsription="Returns a random Meme.")
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://meme-api.com/gimme') as f:
                response = await f.json()
                em = discord.Embed(title=f"Meme By {response['author']}", description=f"[{response['title']}]({response['postLink']})", color=discord.Colour.blurple())
                em.set_image(url=response["url"])
                em.set_footer(text=f"{response['ups']} Upvotes      ●      r/{response['subreddit']}")
                await ctx.respond(embed=em)


def setup(bot):
    bot.add_cog(Fun(bot))