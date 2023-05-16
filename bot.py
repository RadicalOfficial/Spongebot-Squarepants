import os
import discord
from discord import option
import requests
import time as t
import random
from flask import Flask
from threading import Thread
import logging
from discord.ext.pages import Paginator, Page, PaginatorButton
from discord.ext import commands

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask('')

@app.route('/')
def main():
  return "Your Bot Is Ready"

def run():
  app.run(host="0.0.0.0", port=8000)

server = Thread(target=run)
server.start()

print("Loading... ")

bot = discord.Bot()

class Messenger(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(discord.ui.InputText(label="Long Input", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Private Message:", description="Provided by Pycord Bot", color=discord.Color.random())
        embed.add_field(name="Message:", value=self.children[0].value)
        await interaction.response.send_message(embeds=[embed])

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
@bot.command(description="Sees if online")
async def ping(ctx):
  await ctx.respond(f"Pong! Latency is {bot.latency}", ephemeral=True)
  
@bot.command(description="Repeats after you")
async def messenger(ctx: discord.ApplicationContext):
  modal = Messenger(title="this is a title")
  await ctx.send_modal(modal)
  await ctx.respond("Success! The message you have sent is now available to the public!", ephemeral=True)

@bot.command(description="Get Help via the tables.")
async def help(ctx):
  my_pages = [
    Page(
        embeds=[
            discord.Embed(title="Basic Commands:", description="/help - Direct Messages for help\n/messenger - Sends a private message in the area.\n/ping - Checks if the bot is alive\n"),
        ],
    ),
    Page(embeds=[
            discord.Embed(title="Advanced Commands:", description="/check_scratchdb - Checks if ScratchDB is up or not\n")],),
    Page(embeds=[
            discord.Embed(title="Questions? Feedback?", description="Direct Message @k3!\n\n**Other:**\nCurernt Version: ```2.0.3```\n*Credits:*\nPyCord for code\nEverything else by @k3 (creator of this bot)")],),]
  buttons = [
            PaginatorButton("first", label="⏮", style=discord.ButtonStyle.blurple),
            PaginatorButton("prev", label="⏪", style=discord.ButtonStyle.blurple),
            PaginatorButton("page_indicator", style=discord.ButtonStyle.gray, disabled=True),
            PaginatorButton("next", label="⏩", style=discord.ButtonStyle.blurple),
            PaginatorButton("last", label="⏭", style=discord.ButtonStyle.blurple),
        ]
  paginator = Paginator(
            pages=my_pages,
            show_indicator=True,
            use_default_buttons=False,
            custom_buttons=buttons,
        )
  await paginator.respond(ctx.interaction)
@bot.command(description="Checks if ScratchDB is Up or Not.")
async def check_scratchdb(ctx):
  data = requests.get("https://scratchdb-checker.knightbot63.repl.co").json()['Status']
  await ctx.respond("ScratchDB is Currently: " + data, ephemeral=True)
@bot.command(description="Fun game to check if you are human")
async def vibe_check(ctx):
  await ctx.respond("**Loading your content!**", ephemeral=True)
  msg = await ctx.send("Checking your vibe...")
  t.sleep(random.randint(2,5))
  if random.randint(1,2) == 1:
    await msg.edit(content="*You're good.*")
  else:
    await msg.edit(content="You're not good.")
@bot.command(description="Bot Updates or other announcements")
async def announcement(ctx, title: discord.Option(str), message: discord.Option(str), announcement: discord.Option(str), ping_everyone: discord.Option(str)):
  if str(ctx.author) == "k3#8331":
    embed = discord.Embed(title=title, description=message)
    embed.add_field(name="", value=announcement, inline=True)
    embed.set_author(name="Pycord Bot Team", icon_url="https://cdn.discordapp.com/avatars/1095344733104128173/8267b033dec75ddc733b35debc4cc4ad.webp?size=80")
    await ctx.respond(embed=embed)
  else:
    await ctx.respond("What do you think you are doing?", ephemeral=True)
@bot.command(description="Meme Generator")
async def meme_generator(ctx):
  pass
bot.run(os.environ['token'])
