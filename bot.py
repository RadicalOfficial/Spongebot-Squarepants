import os
import discord
from discord import option
from discord.ext.pages import Paginator, Page, PaginatorButton
from discord.ext import commands
import requests
import time as t
import random
from flask import Flask
from threading import Thread
import logging
import aiohttp

print("Pycord Version", discord.__version__)

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
    self.add_item(
      discord.ui.InputText(label="Long Input",
                           style=discord.InputTextStyle.long))

  async def callback(self, interaction: discord.Interaction):
    embed = discord.Embed(title="Private Message:",
                          description="Provided by Spongebot",
                          color=discord.Color.random())
    embed.add_field(name="Message:", value=self.children[0].value)
    await interaction.response.send_message(embeds=[embed])

class MyView(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(label="Click to request being admin.", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
      member = interaction.user
      content = f"Hello {member}!\nDo you want to be an admin of the Server of k3? You're in luck! Once your application gets accepted, you will be admin for 2 months.\nAfter that time goes, you can't re-apply again or else it'll be rejected by the owner and the other moderators.\nRemember, just because you have admin powers doesn't mean you can ban everyone, if we do see things that break the #rules of the server, you will be revoked from admin.\n\nPlease note, this will be implemented in `4.0.0` so stay tuned!\n\nSecret fun fact, you can direct message anyone on the server you like with the bot invited by doing /dm"
      await member.send(content)
      

@bot.event
async def on_ready():
  print(f"{bot.user} is ready and online!")


@bot.command(description="Checks if the bot is online")
async def ping(ctx):
  await ctx.respond("🏓Pong!")


@bot.command(description="Repeats after you")
async def messenger(ctx: discord.ApplicationContext):
  modal = Messenger(title="Please enter text.")
  await ctx.send_modal(modal)
  await ctx.respond(
    "✅Success! The message you have sent is now available to the public!",
    ephemeral=True)


@bot.command(description="Get Help via the tables.")
async def help(ctx):
  my_pages = [
    Page(embeds=[
      discord.Embed(
        title="Basic Commands:",
        description=
        "/help - Direct Messages for help\n/messenger - Sends a private message in the area.\n/ping - Checks if the bot is alive\n"
      ),
    ], ),
    Page(embeds=[
      discord.Embed(
        title="Advanced Commands:",
        description=
        "/check_scratchdb - Checks if ScratchDB is up or not\n/vibe_check - Sees your vibe.\n**(NEW)** /write - Gets responses from Google Bard, An AI\n**(NEW)** /weather - Displays the weather for any city"
      )
    ], ),
    Page(embeds=[
      discord.Embed(
        title="Questions? Feedback?",
        description=
        "Direct Message @k3!\n\n**Other:**\nCurernt Version: ```3.0.0```\n*Credits:*\nPyCord for code\nEverything else by @k3 (creator of this bot)\nGitHub: https://github.com/speedwaysingapore/Spongebot-Squarepants\nReplit: https://replit.com/@Knightbot63/Spongebot\nLine Count (python code): 152"
      )
    ], ),
  ]
  buttons = [
    PaginatorButton("first", label="⏮", style=discord.ButtonStyle.blurple),
    PaginatorButton("prev", label="⏪", style=discord.ButtonStyle.blurple),
    PaginatorButton("page_indicator",
                    style=discord.ButtonStyle.gray,
                    disabled=True),
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
  data = requests.get(
    "https://scratchdb-checker.knightbot63.repl.co").json()['Status']
  await ctx.respond("ScratchDB is Currently: " + data, ephemeral=True)


@bot.command(description="Fun game to check if you are human")
async def vibe_check(ctx):
  await ctx.respond("**Loading your content!**", ephemeral=True)
  msg = await ctx.send("Checking your vibe...")
  t.sleep(random.randint(2, 5))
  if random.randint(1, 2) == 1:
    await msg.edit(content="*You're good.*")
  else:
    await msg.edit(content="You're not good.")


'''@bot.command(description="Bot Updates or other announcements")
async def announcement(ctx, title: discord.Option(str),
                       message: discord.Option(str),
                       announcement: discord.Option(str),
                       ping_everyone: discord.Option(str)):
  if str(ctx.author) == "k3#8331":
    embed = discord.Embed(title=title, description=message)
    embed.add_field(name="", value=announcement, inline=True)
    embed.set_author(
      name="Pycord Bot Team",
      icon_url=
      "https://cdn.discordapp.com/avatars/1095344733104128173/8267b033dec75ddc733b35debc4cc4ad.webp?size=80"
    )
    await ctx.respond(embed=embed)
  else:
    await ctx.respond("What do you think you are doing?", ephemeral=True)'''


@bot.command(description="Gets weather via https://weatherapi.com")
@option("city", str, description="Enter a city. Please use valid ones")
async def weather(ctx, city: discord.Option(str)):
  url = "http://api.weatherapi.com/v1/current.json"
  params = {"key": os.environ["Weather ID"], "q": city}
  async with aiohttp.ClientSession() as session:
    async with session.get(url, params=params) as res:
      data = await res.json()
      print('\n\n', data, "\n\n")
      if 'error' in data:
        await ctx.respond(
          f"Error: `{data['error']['message']}` | Error code: `{data['error']['code']}`"
        )  #respond > send
      else:
        location = data["location"]["name"]
        temp_c = data["current"]["temp_c"]
        temp_f = data["current"]["temp_f"]
        humidity = data["current"]["humidity"]
        wind_kph = data["current"]["wind_kph"]
        wind_mph = data["current"]["wind_mph"]
        condition = data["current"]['condition']['text']
        image_url = "http:" + data["current"]['condition']['icon']

        embed = discord.Embed(title=f"The Weather for {location}",
                              description=f"Condition: `{condition}`")
        embed.add_field(name="Temperature", value=f"F: {temp_f} | C: {temp_c}")
        embed.add_field(name="Humidity", value=f"{humidity}")
        embed.add_field(name="Wind Speeds",
                        value=f"KPH: {wind_kph} | MPH: {wind_mph}")
        embed.set_thumbnail(url=image_url)
        await ctx.respond(embed=embed)


@bot.command(description="[BETA] Uses Google Bard")
@option("request", str, description="Enter text that Bard will generate")
async def prompt(ctx, request: discord.Option(str)):
  await ctx.respond("Thinking...", ephemeral=True)
  data = requests.get("https://text-generator-api.knightbot63.repl.co/api/" +
                      request).json()
  response = data['content']
  request = data['request']
  send = f"**{request}**\n\n`{response}`"
  await ctx.send(send)


@bot.command(description="Calling certain discord people certain things")
async def roles(ctx):
  if str(ctx.author) in ["k3#8331", "Wolfieboy09#4819"]: # why not. wanna see
    await ctx.send(
      "**List of Nitrox's Chat custom roles (by me):\n*Custom:*\nHoid - Gorilla\nHypnos - Demon, witch etc.\nEpic - Perverted\nNitrox - Ant\n*Dirty minded People:*\n List on the padlet.\n*Good People:*\nPooky - Why not?\nEileen - Lowest on the padlet dirty minded people.\n*What about k3?:*\nI don't really have a custom role, maybe nerd since I'm better at coding."
    )
  else:
    await ctx.respond("You can't do that command!", ephemeral=True)
'''
@bot.command(description='Request to be an admin of the server of k3')
@commands.cooldown(1, 120, commands.BucketType.user)
async def curate(ctx):
  await ctx.respond("Please click the button to get a direct message from the bot on what to do.", view=MyView())
'''
@bot.command(description='Get a random cat image')
async def cat(ctx):
  data = requests.get("https://cataas.com/cat?html=false&json=true").json()["url"]
  await ctx.send("https://cataas.com" + data)

@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      await ctx.send('This command is on a %.2fs cooldown' % error.retry_after)

@bot.command(description="Close the form")
async def close(ctx):
  await ctx.send("Command is being built.", ephemeral=True)


bot.run(os.environ['token'])
