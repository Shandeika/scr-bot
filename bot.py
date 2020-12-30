import configparser
import discord
import asyncio
from discord.ext import commands

config = configparser.ConfigParser()
config.read("config.ini", encoding='utf-8')

bot = commands.Bot(command_prefix=config["Config"]["prefix"], intents=discord.Intents.all())
#удаление стандартной команды help 
bot.remove_command('help')

chars = {}

@bot.event
async def on_member_update(before, after):
    if after.top_role.position >= after.guild.me.top_role.position:
        return
    if before.display_name == after.display_name:
        return
    name_raw = after.display_name
    for char in config["Config"]["chars"]:
        name_raw = name_raw.replace(char, "")
    await before.edit(nick=name_raw, reason='Автоматически: Спецсимволы в нике')

async def remove_chars(member):
    name_raw = member.display_name
    for char in config["Config"]["chars"]:  
        name_raw = name_raw.replace(char, "")
    return name_raw

async def rm_custom_char(ctx, char):
    for member in ctx.guild.members:
        if member.top_role.position >=  ctx.guild.me.top_role.position:
            print(f'{member.display_name} я не могу его изменить.')
        else:
            name_raw = member.display_name  
            name_raw = name_raw.replace(char, "")
            await member.edit(nick=name_raw, reason=f'Убран спецсимвол "{char}"')

#@bot.event
async def on_command_error(ctx, exception): # для команд
    embed=discord.Embed(title=":x: Ошибка!", description=f'{exception}', color=0xff0000)
    embed.set_footer(text="Copyright © 2019–2020 Shandy developer agency All Rights Reserved. © 2020")
    await ctx.channel.send(embed = embed, delete_after=60)
    print(exception)

@bot.event
async def on_ready():
    print("Запустился под", bot.user)

@bot.command()
async def test(ctx):
    await ctx.channel.send('test')

@bot.command(aliaces=['убрать'])
async def remove(ctx, char:str=None):
    if char == None:
        for member in ctx.guild.members:
            if member.top_role.position >=  ctx.guild.me.top_role.position:
                print(f'{member.display_name} я не могу его изменить.')
            else:
                nick = await remove_chars(member)
                await member.edit(nick=nick, reason='Убраны спецсимволы')
    else:
        await rm_custom_char(ctx, char)

bot.run(config["Config"]["token"])