import discord
import asyncio
import random
from discord.ext import commands
import secrets
import requests
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
async def test(ctx, *args):
    respuesta = ' '.join(args)
    await ctx.send(respuesta)


@bot.command()
async def contador(ctx, arg):
    temp_cont = int(arg)
    for _ in range(temp_cont):
        await ctx.send(temp_cont)
        temp_cont -= 1
        await asyncio.sleep(1)
    await ctx.send(f"El contador de {arg} segundos ha finalizado")


    

# Peticion a API
@bot.command()
async def poke(ctx, arg):
    try:
        pokemon = arg.split(" ",1)[0]
        result = requests.get("https://pokeapi.co/api/v2/pokemon/"+pokemon)
        if result.text == "Not Found":
            await ctx.send("Hermano voy to ciego, no lo veo")
        else:
            image_url = result.json()['sprites']['front_default']
            print(image_url)
            await ctx.send(image_url)

    except Exception as e:
        print("Error: ", e)


# Peticion a API perks dbd
@bot.command()
async def perks(ctx):
    try:
        result = requests.get(f"https://dbd.tricky.lol/api/randomperks?role=survivor&pretty")
        

        if result.status_code == 200:
            random_perk_data = result.json() 
            await ctx.send(random_perk_data)
        else:
            await ctx.send("No se pudo obtener una perk aleatoria. Inténtalo de nuevo más tarde.")
        
    except Exception as e:
        print("Error: ", e)
        await ctx.send("Hubo un problema al intentar obtener una perk aleatoria.")

@perks.error
async def error_type(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("No lo he encontrado esas perks")

@bot.command()
async def saluda_a_javi(ctx):
    await ctx.send("https://tenor.com/view/smg4-mario-garrys-mod-infinite-gif-17807543")

@bot.event
async def on_ready():
    print(f"Estamos dentro! {bot.user}")


bot.run(secrets.TOKEN)



