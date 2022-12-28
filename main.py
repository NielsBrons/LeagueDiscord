import os
import discord
import urllib.request, json 
from urllib.error import URLError, HTTPError

from dotenv import load_dotenv
from discord.ext import commands

if __name__ == '__main__':
    load_dotenv()
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    RIOT_TOKEN = os.getenv('RIOT_TOKEN')

    intents=discord.Intents.default()
    intents.message_content = True

    client=commands.Bot(intents=intents, command_prefix="!")

    async def do_request(do_url, ctx):
        do_url = do_url.replace(" ", "%20")
        try:
            result = urllib.request.urlopen(do_url)                
        except HTTPError as e:
            await ctx.send(f'DEBUG: {e}')
        except URLError as e:
            await ctx.send(f'DEBUG: {e}')
        
        return result

    @client.command()
    async def lol(ctx, *, arg):
        
        request_url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{arg}?api_key={RIOT_TOKEN}"

        result = await do_request(request_url, ctx)

        if result.status == 200:
            data = json.load(result)
        else:
            await ctx.send(f'DEBUG: {result.status}')
            return
        
        id = data['id']

        request_url = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{id}?api_key={RIOT_TOKEN}"
        result = await do_request(request_url,ctx)

        if result.status == 200:
            data = json.load(result)
        else:
            await ctx.send(f'DEBUG: {result.status}')
            return

        for x in data:
            if x['queueType'] == "RANKED_SOLO_5x5":

                await ctx.send(f"{arg}: {x['tier']} {x['rank']}. Wins: {x['wins']} Losses: {x['losses']}. Win rate: {int(x['wins'] / (x['wins'] + x['losses']) * 100 )}%")

    @client.event
    async def on_message(message):
            await client.process_commands(message)

    client.run(DISCORD_TOKEN)