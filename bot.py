import configparser
import discord
import asyncio
from discord.ext import commands

config = configparser.ConfigParser()
config.read("config.ini", encoding='utf-8')

bot = commands.Bot(command_prefix=config["Config"]["prefix"], intents=discord.Intents.all())
bot.remove_command('help')

@bot.event
async def on_member_update(before, after):
    if after.top_role.position >= after.guild.me.top_role.position or after == after.guild.owner:
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
        if member.top_role.position >=  ctx.guild.me.top_role.position or member == member.guild.owner:
            print(f'{member.display_name} я не могу его изменить.')
        else:
            name_raw = member.display_name  
            name_raw = name_raw.replace(char, "")
            await member.edit(nick=name_raw, reason=f'Убран спецсимвол "{char}"')
        await asyncio.sleep(1)

@bot.event
async def on_command_error(ctx, exception):
    embed=discord.Embed(title=":x: Ошибка!", description=f'{exception}', color=0xff0000)
    embed.set_footer(text="Copyright © 2019–2020 Shandy developer agency All Rights Reserved. © 2020")
    try:
        await ctx.channel.send(embed = embed, delete_after=60)
    except:
        print('Не могу отправить сообщение об ошибке на сервере', ctx.guild.name)
    print(exception)

@bot.event
async def on_guild_join(guild):
    await guild.owner.send('Привет! :partying_face:')
    embed=discord.Embed(title="Инструкция", url="https://github.com/Shandeika/special-character-remover#как-же-его-применять", description="Можешь нажать ссылку выше и ты попадешь на репозиторий github с инструкцией", color=0x000000)
    embed.set_author(name="Shandy", url="https://vk.com/shandeika", icon_url="http://v70551da.beget.tech/uploads/shandy.png")
    embed.add_field(name="Что он делает", value="1. Удаляет запрещенные символы из ника\n2. Удаляет символ, который вы хотите удалить", inline=False)
    embed.add_field(name="Если вы готовы, то для начала процесса необходимо ввести", value="`.remove`", inline=True)
    embed.add_field(name="Для удаления конкретного символа нужно ввести", value="`.remove H`", inline=True)
    embed.add_field(name="ОЧЕНЬ ВАЖНО!\nРазмести роль бота выше всех!", value="Иначе он не сможет изменять ники", inline=True)
    embed.set_footer(text="Copyright © 2019–2020 Shandy developer agency All Rights Reserved. © 2020")
    await guild.owner.send(embed=embed)

@bot.event
async def on_ready():
    print("Запустился под", bot.user)

@bot.command(aliaces=['помощь'])
async def help(ctx):
    try:
        await ctx.message.delete()
    except:
        print('Не получилось удалить сообщение')
    embed=discord.Embed(title="special-character-remover", url="https://github.com/Shandeika/special-character-remover", description="Уберет спецсимволы из ников пользователей, что бы они не светились в топе из за одного символа.")
    embed.set_author(name="Shandy", url="https://vk.com/shandeika", icon_url="http://v70551da.beget.tech/uploads/shandy.png")
    embed.set_image(url='http://v70551da.beget.tech/uploads/special-character-remover.png')
    embed.set_footer(text="Copyright © 2019–2020 Shandy developer agency All Rights Reserved. © 2020")
    await ctx.channel.send(embed=embed)

@bot.command(aliaces=['убрать'])
async def remove(ctx, char:str=None):
    await ctx.message.delete()
    if char == None:
        for member in ctx.guild.members:
            if member.top_role.position >=  ctx.guild.me.top_role.position or member == member.guild.owner:
                print(f'{member.display_name} я не могу его изменить.')
            else:
                nick = await remove_chars(member)
                await member.edit(nick=nick, reason='Убраны спецсимволы')
    else:
        await rm_custom_char(ctx, char)

bot.run(config["Config"]["token"])