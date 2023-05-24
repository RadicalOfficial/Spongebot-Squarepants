import os
import discord
from discord import option
from discord.ext.pages import Paginator, Page, PaginatorButton
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure
import requests
import time as t
import random
from flask import Flask, jsonify
from threading import Thread
import logging
import aiohttp
import json
import datetime
import inflect

p = inflect.engine()

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask('')


@app.route('/')
def main():
  return jsonify({"status": "up"})

@app.route('/lottery/reset')
def rng():
  return jsonify({"Hourly time until reset:": datetime.datetime.now().hour})

def run():
  app.run(host="0.0.0.0", port=8000, threaded=True)


server = Thread(target=run)
server.start()

def checkIfMidnight():
    return datetime.time(hour=0, minute=0, second=0, microsecond=0) == 0

def change_lottery_numbers():
  f = open('lottery.json')
  data = json.load(f)["rng"]

  findString = str(data)
  rpl = random.randint(0,99), random.randint(0,99), random.randint(0,99), random.randint(0,99)
  res = str(rpl)[1:-1]
  print(res)
  with open('lottery.json', 'r') as f:
    data = f.read()
    data = data.replace(findString, res)
  
  with open('lottery.json', 'w') as f:
    f.write(data)
  f.close()
  print("JSON Data replaced")
def like_the_bot():
  if random.randint(1,10) == 4:
    print("☕Like the bot?")
midnight = checkIfMidnight()
print(midnight)

'''
Bot Code
'''
activity = discord.Game(name="/help")
bot = discord.Bot(activity=activity, status=discord.Status.online)


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


class BardButton(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)

    supportServerButton = discord.ui.Button(label='Support Server', style=discord.ButtonStyle.gray, url='https://discord.com')
    self.add_item(supportServerButton)

  
  @discord.ui.button(label="See the API", style=discord.ButtonStyle.url)
  async def button_callback(self, button, interaction):
    await interaction.response.send_message("You clicked the button!")

choices = ["Rock", "Paper", "Scissors"]

class game(discord.ui.View):
    @discord.ui.select(placeholder = "Choose an action!", min_values = 1, max_values = 1, options = [
            discord.SelectOption(
                label="🪨 Rock",
                description="Choose if you want rock"
            ),
            discord.SelectOption(
                label="🧻 Paper",
                description="Choose if you want to use paper"
            ),
            discord.SelectOption(
                label="✂ Scissors",
                description="Choose if you want Scissors"
            )
        ]
    )
    async def select_callback(self, select, interaction):
      user_choice = select.values[0]
      answer = random.choice(choices)
      if user_choice == "🪨 Rock": # 1
        if answer == "Rock":
          await interaction.response.send_message(f"# You tied to {answer}!\n\n ### Ready to challenge again? Do /play again.")
        elif answer == "Scissors":
          await interaction.response.send_message(f"# You lost to {answer}!\n\n ### Ready to challenge again? Do /play again.")
        elif answer == "Paper":
          await interaction.response.send_message(f"# You won to {answer}!\n\n ### Ready to challenge again? Do /play again.")
      
      
      elif user_choice == "🧻 Paper": # 2
        if answer == "Rock":
          await interaction.response.send_message(f"# You Won to {answer}!\n\n ### Ready to challenge again? Do /play again.")
        elif answer == "Scissors":
          await interaction.response.send_message(f"# You lost to {answer}!\n\n ### Ready to challenge again? Do /play again.")
        elif answer == "Paper":
          await interaction.response.send_message(f"# You tied to {answer}!\n\n ### Ready to challenge again? Do /play again.")
      
      
      elif user_choice == "✂ Scissors": # 3
        if answer == "Rock":
          await interaction.response.send_message(f"# You lost to {answer}!\n\n ### Ready to challenge again? Do /play again.")
        elif answer == "Scissors":
          await interaction.response.send_message(f"# You tied to {answer}!\n\n ### Ready to challenge again? Do /play again.")
        elif answer == "Paper":
          await interaction.response.send_message(f"# You won to {answer}!\n\n ### Ready to challenge again? Do /play again.")
      

@bot.command(description="Checks if the bot is online")
async def ping(ctx):
  await ctx.respond("🏓Pong!")


@bot.command(description="Repeats after you")
async def messenger(ctx: discord.ApplicationContext):
  like_the_bot()
  modal = Messenger(title="Please enter text.")
  await ctx.send_modal(modal)
  await ctx.respond(
    "✅Success! The message you have sent is now available to the public!",
    ephemeral=True)


@bot.command(description="Get Help via the tables.")
async def help(ctx):
  like_the_bot()
  my_pages = [
    Page(embeds=[
      discord.Embed(
        title="Basic Commands:",
        description=
        "/help - Direct Messages for help\n/messenger - Sends a private message in the area.\n/ping - Checks if the bot is alive\n/game - Plays rock paper scissors."
      ),
    ], ),
    Page(embeds=[
      discord.Embed(
        title="Advanced Commands:",
        description=
        "/vibe_check - Sees your vibe.\n/write - Gets responses from Google Bard, An AI\n/weather - Displays the weather for any city\n/dice - Rolls the dice\n/vote - Creates a vote."
      )
    ], ),
    Page(embeds=[
      discord.Embed(
        title="Questions? Feedback?",
        description=
        "Direct Message @k3!\n\n**Other:**\nCurernt Version: ```3.1.0```\n*Credits:*\nPyCord for code\nEverything else by @k3 (creator of this bot)\nGitHub: https://github.com/speedwaysingapore/Spongebot-Squarepants\nReplit: https://replit.com/@Knightbot63/Spongebot\nLine Count (python code): 300+"
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


# @bot.command(description="Checks if ScratchDB is Up or Not.")
async def check_scratchdb(ctx):
  like_the_bot()
  async with aiohttp.ClientSession() as session:
    async with session.get("https://scratchdb.lefty.one") as r:
      status = await r.status_code
      print(status)
      if status == 200:
        data = "Online"
      else:
        data = "Offline"
      await ctx.respond("ScratchDB is Currently: " + data, ephemeral=True)


@bot.command(description="Fun game to check if you are human")
async def vibe_check(ctx):
  like_the_bot()
  await ctx.respond("**Loading your content!**", ephemeral=True)
  msg = await ctx.send("Checking your vibe...")
  t.sleep(random.randint(2, 5))
  if random.randint(1, 2) == 1:
    await msg.edit(content="*You're good.*")
  else:
    await msg.edit(content="You're not good.")


'''
@bot.command(description="Bot Updates or other announcements")
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
    await ctx.respond("What do you think you are doing?", ephemeral=True)
'''


@bot.command(description="Gets weather via https://weatherapi.com")
@option("city", str, description="Enter a city. Please use valid ones")
async def weather(ctx, city: discord.Option(str)):
  like_the_bot()
  url = "http://api.weatherapi.com/v1/current.json"
  params = {"key": os.environ["Weather ID"], "q": city}
  async with aiohttp.ClientSession() as session:
    async with session.get(url, params=params) as res:
      data = await res.json()
      #print('\n\n', data, "\n\n")
      if 'error' in data:
        await ctx.respond(
          f"Error: `{data['error']['message']}` | Error code: `{data['error']['code']}`"
        )
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


@bot.command(description="Uses Google Bard to fetch responses")
@option("request", str, description="Enter text that Bard will generate")
@option("member", str, description="This is optional, you don't have to enter anything.")
@commands.cooldown(1,5)
async def prompt(ctx, request: discord.Option(str), member: discord.Member=None):
  like_the_bot()
  member = ctx.author
  await ctx.respond("*Spongebot Squarepants is thinking...*", ephemeral=True)
  async with aiohttp.ClientSession() as session:
    async with session.get("https://text-generator-api.knightbot63.repl.co/api/" + request) as r:
      data = await r.json()
      response = data['content']
      request = data['request']
      send = f"**{request}**\n\n```{response}```"
  try:
    await member.respond(send)
  except Exception:
    raise f"The bot can't send the request because {Exception}"
    
@bot.command(description='Get a random cat image')
@commands.cooldown(1,300)
async def cat_image(ctx):
  like_the_bot()
  async with aiohttp.ClientSession() as session:
    async with session.get('https://cataas.com/cat?html=false&json=true') as r:
      data = r.json()["url"]
      await ctx.send("https://cataas.com" + data)
      await ctx.respond("Success!", ephemeral=True)


@bot.command(description='Range of Random Numbers')
@commands.cooldown(1,10)
@option("first", int, description="Your first number")
@option("second", int, description="Your second number")
async def dice(ctx, first: discord.Option(int), second: discord.Option(int)):
  like_the_bot()
  print("Ranging")
  print("Yes")
  rang = random.randint(first, second)
  await ctx.respond("Successfully sent the prompt!", ephemeral=True)
  await ctx.respond(f"{ctx.author.mention}\nFirst: {first}\nSecond: {second}\n Result: {rang}")

@bot.command(description="Fetches latest comment")
@option("channel", str, description="Enter the channel ID for the server the bot is in to get the latest comment.")
async def fetch_latest(ctx, channel: discord.Option(str)):
  like_the_bot()
  try:
    channel = bot.get_channel(int(channel))
    message = await channel.fetch_message(
    channel.last_message_id)
    await ctx.respond(f'Latest message in: #{channel.name} has been sent by @{message.author.name}\n**Message:**\n' + message.content)
  except:
    await ctx.respond("Failed to fetch.", ephemeral=True)


@bot.command(description="Makes a voting system")
@option("desc", str, description="Enter a description for your vote!")
async def create_vote(ctx, desc: discord.Option(str)):
  like_the_bot()
  try:
    embed = discord.Embed(
        title="Vote:",
        description=desc
    )
    embed.set_footer(text="Upvote and Downvote about your expressions!")
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
    msg = await ctx.respond(embed=embed)
    message = await msg.original_response()
    await message.add_reaction("👍")
    await message.add_reaction("👎")
  except Exception as e:
    await ctx.respond("Some errors had occurred. Do not worry, this is in an alpha state.", ephemeral=True)


@bot.command(description="Plays a basic game of rick, paper, scissors")
async def play(ctx):
  like_the_bot()
  await ctx.respond(f"Challenge accepted {ctx.author.mention}!", ephemeral=True)
  await ctx.send("Up to a battle of rock paper scissors from the bot?", view=game())


'''
@tasks.loop(time=midnight)
async def send():
  channel = bot.get_channel(os.environ['CHANNEL'])
  change_lottery_numbers()
  await channel.send('Rerolling the Loterry for today!')
'''

@bot.event
async def on_application_command_error(ctx, error):  
  if isinstance(error, commands.CommandOnCooldown):
      await ctx.send('Sorry, you must wait %.2fs until you can do this command.' % error.retry_after)

@bot.event
async def on_ready():
  # send.start()
  print(f"{bot.user} is ready and online!")


bot.run(os.environ['token'])
