# THIS MAY BE OUTDATED. IF SO, PLEASE CONTACT @KNIGHTBOT63 ON SCRATCH
from flask import Flask
from threading import Thread
import os
import discord
from discord import option
import requests
import time as t
import random

app = Flask('')

print("Running")

@app.route('/')
def main():
  return "Your Bot Is Ready"

def run():
  app.run(host="0.0.0.0", port=8000)

server = Thread(target=run)
server.start()

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
@bot.command(description="Sees if online")
async def ping(ctx):
  await ctx.respond(f"Pong! Latency is {bot.latency}")
@bot.command(description="Does addition.")
@option(
    "first",
    str,
    description="Enter a number"
)
@option(
    "second",
    str,
    description="Enter a number"
)
async def add(ctx, first: discord.Option(int), second: discord.Option(int)):
  sum = first + second
  await ctx.respond(f"The sum of {first} and {second} is {sum}.")
#Pages for Leaderboard
  
@bot.command(description="Repeats after you")
async def messenger(ctx, message: discord.Option(str), private: discord.Option(str)):
  print(ctx.author, f"Message: {message} Private: {private}")
  if private == "no":
    author = str(ctx.author)
  else:
    author = "Anonymous User 👻"
  print(author)
  embed = discord.Embed(
        title="Message Provider:",
        description="Provided from your convienience.",
        color=discord.Color.random(),
    )
  discord.Embed.set_author(embed, name=f"Written by: @{author}")
  discord.Embed.add_field(embed, name="Message Content:", value=f"{message}")
  embed.set_footer(text="---------\nThis is bad? Contact @k3\n\nProvided by Pycord")
  await ctx.send(embed=embed)

@bot.command(description="Get Help via Direct Messages (Filling out the help box can be anything)")
async def help(ctx, member: discord.Member):
  print(member)
  member = ctx.author
  await ctx.respond("Sent a Direct Message to you, check your inbox for help!", ephemeral=True)
  embed = discord.Embed(
        title="Commands",
        description="Here are the list of commands, most of these are updated to the current version.",
        color=discord.Colour.blurple())
  embed.add_field(name="/help", value="Get's you here", inline=False)
  embed.add_field(name="/ping", value="Check if bot is online", inline=False)
  embed.add_field(name="/messenger", value="Sends secret messages if selected 'no'", inline=False)
  embed.set_author(name="Creator of Bot: k3")
  embed.set_footer(text="Update version: v2.0.2")
  await member.send(embed=embed)

@bot.command(description="Checks if ScratchDB is Up or Not.")
async def check_scratchdb(ctx):
  await ctx.respond("Request sent!", ephemeral=True)
  data = requests.get("https://scratchdb-checker.knightbot63.repl.co").json()['Status']
  await ctx.respond(data)
@bot.command(description="Fun game to check if you are human")
async def vibe_check(ctx):
  await ctx.respond("**Loading your content!**", ephemeral=True)
  msg = await ctx.send("Checking your vibe...")
  t.sleep(random.randint(2,5))
  if random.randint(1,2) == 1:
    await msg.edit(content="*You're good.*")
  else:
    await msg.edit(content="You're not good. You are a **demon**.")
bot.run(os.environ['token'])
