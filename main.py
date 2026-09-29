from datetime import timedelta
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("DISCORD_TOKEN")


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()

@bot.tree.command()
async def dalsisession(interaction: discord.Interaction):
    DnDRole = discord.utils.get(interaction.guild.roles, name="Dračáci")

    poll = discord.Poll(question="🐉Kdy máte čas na další session?🐉", duration=timedelta(hours=24), multiple=True)
    for day in ["Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek", "Sobota", "Neděle"]:
        poll.add_answer(text=day)

    await interaction.response.send_message(content= DnDRole.mention,poll=poll)

@bot.listen()
async def on_message(message: discord.Message):

    if message.type != discord.MessageType.poll_result or message.author.id != bot.user.id:
        return
    DnDRole = discord.utils.get(message.guild.roles, name="Dračáci")

    poll_message = await message.channel.fetch_message(message.reference.message_id)
    poll = poll_message.poll

    top = max(a.vote_count for a in poll.answers)
    vitezove = ", ".join(f"**{a.text}**" for a in poll.answers if a.vote_count == top)

    await poll_message.reply(f"{DnDRole.mention} Příští session budeme mít v {vitezove}")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)