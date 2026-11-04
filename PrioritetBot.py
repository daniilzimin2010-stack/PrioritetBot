import discord
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

CMD_CHANNEL_ID = 1561990542194122847    # Чат отправки
TARGET_CHANNEL_ID = 1561990542194122847 # Пользовательский чат
ROLE_ID = 1561990539874803777           # Роль пользователей
Open = False
TOKEN = os.environ["DISCORD_TOKEN"]

@bot.event
async def on_message(message):
    global Open
    if message.author.bot:
        return
    if message.channel.id == CMD_CHANNEL_ID:
        if not Open and not message.content.startswith("!sw"):
            try:
                await message.delete()
            except discord.Forbidden:
                print("Бот не может удалить это сообщение")
            return
    await bot.process_commands(message)


@bot.command()
@commands.has_permissions(manage_channels=True)
async def sw(ctx):
    global Open
    if ctx.channel.id != CMD_CHANNEL_ID:
        return

    target_channel = bot.get_channel(TARGET_CHANNEL_ID)
    role = ctx.guild.get_role(ROLE_ID)
    
    if not target_channel or not role:
        return await ctx.send("Канал или роль не найдены.")
    
    await target_channel.set_permissions(role, view_channel=True, send_messages=True)
    Open = True 


@bot.command()
@commands.has_permissions(manage_channels=True)
async def ms(ctx):
    global Open
    if ctx.channel.id != CMD_CHANNEL_ID:
        return

    target_channel = bot.get_channel(TARGET_CHANNEL_ID)
    role = ctx.guild.get_role(ROLE_ID)
    
    if not target_channel or not role:
        return await ctx.send("Канал или роль не найдены.")
    
    await target_channel.set_permissions(role, view_channel=False, send_messages=False)
    Open = False 
bot.run(TOKEN)