import aiohttp
import requests

async def fetch_darkjoke():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://peter-api.up.railway.app/api/darkjoke") as response:
            result = await response.json()
            return result

async def fetch_joke():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://peter-api.up.railway.app/api/joke") as response:
            result = await response.json()
            return result

async def fetch_question():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://peter-api.up.railway.app/api/question") as response:
            result = await response.json()
            return result

async def fetch_fact():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://peter-api.up.railway.app/api/fact") as response:
            result = await response.json()
            return result

async def fetch_quote():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://peter-api.up.railway.app/api/quote") as response:
            result = await response.json()
            return result

async def fetch_roast(user):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://peter-api.up.railway.app/api/roast/{user}") as response:
            result = await response.json()
            return result

def fetch_song():
    response = requests.get("https://peter-api.up.railway.app/api/recommendation")
    result = response.json()
    return result


async def fetch_version():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://peter-api.up.railway.app/api/version") as response:
            result = await response.json()
            return result