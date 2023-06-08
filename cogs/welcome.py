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
    async def testleave(self, ctx):
        db = client["nuko"]
        channels = db["leavechannel"]
        messages = db["leaves"]
        query = channels.find_one({"guild_id": ctx.guild.id})
        query2 = messages.find_one({"guild_id": ctx.guild.id})

        if query is None or query2 is None:
            return await ctx.respond("No Leave Message or Channel has been set yet! Please set them up.")

        channel = self.bot.get_channel(query["channel_id"])
        if channel is None:
            return await ctx.respond("The leave channel does not exist. Please set it up correctly.")

        toSend = query2["message"].replace("{user}", f"Nuko#1234")
        toSend = toSend.replace("{user.mention}", f"<@1084050050495287356>")
        color = getattr(discord.Colour, query2["embed_color"])()
        em = discord.Embed(title=query2["embed_title"], description=toSend + " TEST MESSAGE", color=color)
        em.set_image(url=query2["embed_image"])

        try:
            if query2["mention_newmember"] == "true":
                await channel.send("<@1084050050495287356>")
                await channel.send(embed=em)
                await ctx.respond(f"Sent Test Leave/Goodbye message in {channel}.")
            else:
                await channel.send(embed=em)
                await ctx.respond(f"Sent Test Leave/Goodbye message in {channel}.")
        except discord.Forbidden:
            await ctx.respond("I don't have permission to send messages in the leave channel.")
        except discord.HTTPException:
            await ctx.respond("An error occurred while sending the leave message. Please try again.")

    @discord.slash_command()
    @commands.has_permissions(manage_channels=True)
    async def testwelcome(self, ctx):
        db = client['nuko']
        channels = db['channels']
        messages = db["messages"]
        query = channels.find_one({"guild_id": ctx.guild.id})
        query2 = messages.find_one({"guild_id": ctx.guild.id})

        if query is None or query2 is None:
            return await ctx.respond("No Welcome Message or Channel has been set yet! Please set them up.")

        channel = self.bot.get_channel(query["channel_id"])
        if channel is None:
            return await ctx.respond("The welcome channel does not exist. Please set it up correctly.")

        toSend = query2["message"].replace("{user}", f"Nuko#1234")
        toSend = toSend.replace("{user.mention}", f"<@1084050050495287356>")
        color = getattr(discord.Colour, query2["embed_color"])()
        em = discord.Embed(title=query2["embed_title"], description=toSend + " TEST MESSAGE", color=color)
        em.set_image(url=query2["embed_image"])

        try:
            if query2["mention_newmember"] == "true":
                await channel.send("<@1084050050495287356>")
                await channel.send(embed=em)
                await ctx.respond(f"Sent Test Leave/Goodbye message in {channel}.")
            else:
                await channel.send(embed=em)
                await ctx.respond(f"Sent Test Leave/Goodbye message in {channel}.")
        except discord.Forbidden:
            await ctx.respond("I don't have permission to send messages in the welcome channel.")
        except discord.HTTPException:
            await ctx.respond("An error occurred while sending the welcome message. Please try again.")

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
    async def setleavemessage(self, ctx, embed_title: str, message: str, embed_image:str, embed_color: discord.Option(str, choices=['blue', 'blurple', 'red' , 'green' , 'yellow' , 'nitro_pink' , 'gold']), mention_newmember : discord.Option(str, choices=["true" , "false"])):
        """Set the Welcome Channel."""
        db = client["nuko"]
        collection = db["leaves"]
        query = collection.find_one({f'guild_id': ctx.guild.id})
        if not query:
            post = {
                'guild_id' : ctx.guild.id,
                'embed_title' : embed_title,
                'message' : message,
                'embed_image' : embed_image,
                'embed_color' : embed_color,
                'mention_newmember' : mention_newmember
            }
            collection.insert_one(post)
            return await ctx.respond(f"Successfully set Leave System To: \n**Embed Title:** `{embed_title}`\n**Embed Description/Message:** `{message}`\n**Embed Image(URL):** `{embed_image}`\n**Embed Color:** `{embed_color}`\n**Mention Member:** `{mention_newmember}`")
        else:
            collection.update_many(
                {'guild_id': ctx.guild.id},
                {'$set': {'embed_title': embed_title,
                'message': message,
                'embed_image': embed_image,
                'embed_color' : embed_color,
                'mention_newmember' : mention_newmember
                }},
                upsert=True
            )
            return await ctx.respond(f"Successfully Edited Leave System To: \n**Embed Title:** `{embed_title}`\n**Embed Description/Message:** `{message}`\n**Embed Image(URL):** `{embed_image}`\n**Embed Color:** `{embed_color}`\n**Mention Member:** `{mention_newmember}`")
        
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
    async def setwelcomemessage(self, ctx, embed_title: str, message: str, embed_image:str, embed_color: discord.Option(str, choices=['blue', 'blurple', 'red' , 'green' , 'yellow' , 'nitro_pink' , 'gold']), mention_newmember : discord.Option(str, choices=["true" , "false"])):
        """Set the Welcome Channel."""
        db = client["nuko"]
        collection = db["messages"]
        query = collection.find_one({f'guild_id': ctx.guild.id})
        if not query:
            post = {
                'guild_id' : ctx.guild.id,
                'embed_title' : embed_title,
                'message' : message,
                'embed_image' : embed_image,
                'embed_color' : embed_color,
                'mention_newmember' : mention_newmember
            }
            collection.insert_one(post)
            return await ctx.respond(f"Successfully set Welcome System To: \n**Embed Title:** `{embed_title}`\n**Embed Description/Message:** `{message}`\n**Embed Image(URL):** `{embed_image}`\n**Embed Color:** `{embed_color}`\n**Mention New Member:** `{mention_newmember}`")
        else:
            collection.update_many(
                {'guild_id': ctx.guild.id},
                {'$set': {'embed_title': embed_title,
                'message': message,
                'embed_image': embed_image,
                'embed_color' : embed_color,
                'mention_newmember' : mention_newmember
                }},
                upsert=True
            )
            return await ctx.respond(f"Successfully Edited Welcome System To: \n**Embed Title:** `{embed_title}`\n**Embed Description/Message:** `{message}`\n**Embed Image(URL):** `{embed_image}`\n**Embed Color:** `{embed_color}`\n**Mention New Member:** `{mention_newmember}`")
        
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