import discord
import pymongo
import json
from discord.ext import commands

with open('config.json') as f:
    data = json.load(f)

client = pymongo.MongoClient(data["mongodb"])
db = client.test

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    @commands.has_permissions(manage_channels=True)
    async def setleavechannel(self, ctx, channel: discord.TextChannel):
        """Set the Leave/Goodbye Channel."""
        db = client["nuko"]
        collection = db["leavechannel"]

        try:
            query = collection.find_one({'guild_id': ctx.guild.id})

            if not query:
                post = {
                    'guild_id': ctx.guild.id,
                    'channel_id': channel.id
                }
                collection.insert_one(post)
                return await ctx.respond(f"Successfully set Leave/Goodbye channel to {channel.mention}")
            else:
                collection.update_one(
                {'guild_id': ctx.guild.id},
                {'$set': {'channel_id': channel.id}}
            )
            return await ctx.respond(f"Successfully edited Leave/Goodbye channel to {channel.mention}")

        except Exception as e:
            await ctx.respond(f"An error occurred while setting the Leave/Goodbye channel: {str(e)}")

    @discord.slash_command()
    @commands.has_permissions(manage_channels=True)
    async def delleavechannel(self, ctx):
        """Delete the Leave/Goodbye Channel."""
        db = client['nuko']
        collection = db['leavechannel']
        query = collection.find_one({'guild_id': ctx.guild.id})
        if query:
            collection.delete_one({'guild_id': ctx.guild.id})
            return await ctx.respond("Successfully deleted Leave/Goodbye channel.")
        else:
            return await ctx.respond("No Leave/Goodbye channel has been set yet.")
    
    @discord.slash_command()
    @commands.has_permissions(manage_channels=True)
    async def setleavemessage(self, ctx, image_title: str, message: str, image_url:str, mention_user : discord.Option(str, choices=["true" , "false"])):
        """Set the Welcome Channel."""
        db = client["nuko"]
        collection = db["leaves"]
        query = collection.find_one({f'guild_id': ctx.guild.id})
        if not query:
            post = {
                'guild_id' : ctx.guild.id,
                'image_title' : image_title,
                'message' : message,
                'image_url' : image_url,
                'mention_user' : mention_user
            }
            collection.insert_one(post)
            return await ctx.respond(f"Successfully set Leave System To: \n**Image Title:** `{image_title}`\n**Image Message:** `{message}`\n**Image(URL):** `{image_url}`\n**Mention Member:** `{mention_user}`")
        else:
            collection.update_many(
                {'guild_id': ctx.guild.id},
                {'$set': {'image_title': image_title,
                'message' : message,
                'image_url' : image_url,
                'mention_user' : mention_user
                }},
                upsert=True
            )
            return await ctx.respond(f"Successfully edited Leave System To: \n**Image Title:** `{image_title}`\n**Image Message:** `{message}`\n**Image(URL):** `{image_url}`\n**Mention Member:** `{mention_user}`")
        
    @discord.slash_command()
    @commands.has_permissions(manage_channels=True)
    async def delleavemessage(self, ctx):
        """Delete the Welcome Channel."""
        db = client['nuko']
        collection = db['leaves']
        query = collection.find_one({'guild_id': ctx.guild.id})
        if query:
            collection.delete_one({'guild_id': ctx.guild.id})
            return await ctx.respond("Successfully deleted Leave Message.")
        else:
            return await ctx.respond("No Leave Message has been set yet.")
        
    @discord.slash_command()
    @commands.has_permissions(manage_channels=True)
    async def setwelcomechannel(self, ctx, channel: discord.TextChannel):
        """Set the Welcome Channel."""
        db = client["nuko"]
        collection = db["channels"]
        query = collection.find_one({f'guild_id': ctx.guild.id})
        if not query:
            post = {
                'guild_id' : ctx.guild.id,
                'channel_id' : channel.id
            }
            collection.insert_one(post)
            return await ctx.respond(f"Successfully set Welcome channel to {channel.mention}")
        else:
            collection.update_one(
                {'guild_id': ctx.guild.id},
                {'$set': {'channel_id': channel.id}}
            )
            return await ctx.respond(f"Successfully edited Welcome channel to {channel.mention}")
        
    @discord.slash_command()
    @commands.has_permissions(manage_channels=True)
    async def delwelcomechannel(self, ctx):
        """Delete the Welcome Channel."""
        db = client['nuko']
        collection = db['channels']
        query = collection.find_one({'guild_id': ctx.guild.id})
        if query:
            collection.delete_one({'guild_id': ctx.guild.id})
            return await ctx.respond("Successfully deleted Welcome channel.")
        else:
            return await ctx.respond("No Welcome channel has been set yet.")

    @discord.slash_command()
    @commands.has_permissions(manage_channels=True)
    async def setwelcomemessage(self, ctx, image_title: str, message: str, image_url:str, mention_user : discord.Option(str, choices=["true" , "false"])):
        """Set the Welcome Channel."""
        db = client["nuko"]
        collection = db["messages"]
        query = collection.find_one({f'guild_id': ctx.guild.id})
        if not query:
            post = {
                'guild_id' : ctx.guild.id,
                'image_title' : image_title,
                'message' : message,
                'image_url' : image_url,
                'mention_user' : mention_user
    
            }
            collection.insert_one(post)
            return await ctx.respond(f"Successfully set Welcome System To: \n**Image Title:** `{image_title}`\n**Image Message:** `{message}`\n**Image(URL):** `{image_url}`\n**Mention New Member:** `{mention_user}`")
        else:
            collection.update_many(
                {'guild_id': ctx.guild.id},
                {'$set': {'image_title' : image_title,
                'message' : message,
                'image_url' : image_url,
                'mention_user' : mention_user
                }},
                upsert=True
            )
            return await ctx.respond(f"Successfully Edited Welcome System To: \n**Image Title:** `{image_title}`\n**Image Message:** `{message}`\n**Image(URL):** `{image_url}`\n**Mention New Member:** `{mention_user}`")
        
    @discord.slash_command()
    @commands.has_permissions(manage_channels=True)
    async def delwelcomemessage(self, ctx):
        """Delete the Welcome Channel."""
        db = client['nuko']
        collection = db['messages']
        query = collection.find_one({'guild_id': ctx.guild.id})
        if query:
            collection.delete_one({'guild_id': ctx.guild.id})
            return await ctx.respond("Successfully deleted Welcome Message.")
        else:
            return await ctx.respond("No Welcome Message has been set yet.")
        
def setup(bot):
    bot.add_cog(Welcome(bot))