import os
import discord
from discord import option
from discord.ext.pages import Paginator, Page, PaginatorButton
from discord.ext import commands
import time as t
import random
from flask import Flask, jsonify
from threading import Thread
import logging
import aiohttp
import json
import inflect
import urllib.parse

p = inflect.engine()

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask('')


@app.route('/')
def main():
  return jsonify({"status": "up"})


def run():
  app.run(host="0.0.0.0", port=8000, threaded=True)


server = Thread(target=run)
server.start()
'''
Bot Code
'''


async def fixPrompt(text: str):
  return urllib.parse.quote_plus(text)


def find_command(command: str) -> bool:
  command = command.lower()
  with open('commands.txt', 'r') as file:
    content = file.readlines()
    for index, line in enumerate(content):
      cline = line.split('cmd: ')
      if cline[0] == '':
        if cline[1].strip() == command:
          desc = content[index+1].replace('- ', '', 1)
          return {"found": True, "desc": desc}
    return {"found": False, "desc": None}


bot = discord.Bot(activity=discord.Game(name="/help"))

user = bot.create_group("user", "User API of Servers")
cats = bot.create_group("cat", "Cat API of Servers")
scratch = bot.create_group("scratch", "Scratch things")

def count_truth():
  with open('truths.txt', 'r') as f:
    return int(f.read())


def count_dare():
  with open('dares.txt', 'r') as f:
    return int(f.read())


async def update_truth():
  with open('truths.txt', 'r') as f:
    cCount = int(f.read())
  with open('truths.txt', 'w') as f:
    f.write(f"{cCount + 1}")


async def update_dare():
  with open('dares.txt', 'r') as f:
    cCount = int(f.read())
  with open('dares.txt', 'w') as f:
    f.write(f"{cCount + 1}")

class Messenger(discord.ui.Modal):

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    self.add_item(
      discord.ui.InputText(label="Insert better placeholder lol",
                           style=discord.InputTextStyle.long))

  async def callback(self, interaction: discord.Interaction):
    embed = discord.Embed(title="Private Message:",
                          description="Provided by Spongebot",
                          color=discord.Color.random())
    embed.add_field(name="Message:", value=self.children[0].value)
    await interaction.response.send_message(embeds=[embed])


class BardButton(discord.ui.View):

  def __init__(self):
    super().__init__()
    button = discord.ui.Button(
      label='See our API!',
      style=discord.ButtonStyle.url,
      url='https://text-generator-api.knightbot63.repl.co/')
    self.add_item(button)

  async def on_timeout(self):
    pass


choices = ["Rock", "Paper", "Scissors"]


class game(discord.ui.View):

  @discord.ui.select(
    placeholder="Choose an action!",
    min_values=1,
    max_values=1,
    options=[
      discord.SelectOption(label="🪨 Rock",
                           description="Choose if you want rock"),
      discord.SelectOption(label="🧻 Paper",
                           description="Choose if you want to use paper"),
      discord.SelectOption(label="✂ Scissors",
                           description="Choose if you want Scissors")
    ])
  async def select_callback(self, select, interaction):
    user_choice = select.values[0]
    answer = random.choice(choices)
    if user_choice == "🪨 Rock":  # 1
      if answer == "Rock":
        await interaction.response.send_message(
          f"# You tied to {answer}!\n\n ### Ready to challenge again? Do /play again."
        )
      elif answer == "Scissors":
        await interaction.response.send_message(
          f"# You lost to {answer}!\n\n ### Ready to challenge again? Do /play again."
        )
      elif answer == "Paper":
        await interaction.response.send_message(
          f"# You won to {answer}!\n\n ### Ready to challenge again? Do /play again."
        )

    elif user_choice == "🧻 Paper":  # 2
      if answer == "Rock":
        await interaction.response.send_message(
          f"# You Won to {answer}!\n\n ### Ready to challenge again? Do /play again."
        )
      elif answer == "Scissors":
        await interaction.response.send_message(
          f"# You lost to {answer}!\n\n ### Ready to challenge again? Do /play again."
        )
      elif answer == "Paper":
        await interaction.response.send_message(
          f"# You tied to {answer}!\n\n ### Ready to challenge again? Do /play again."
        )

    elif user_choice == "✂ Scissors":  # 3
      if answer == "Rock":
        await interaction.response.send_message(
          f"# You lost to {answer}!\n\n ### Ready to challenge again? Do /play again."
        )
      elif answer == "Scissors":
        await interaction.response.send_message(
          f"# You tied to {answer}!\n\n ### Ready to challenge again? Do /play again."
        )
      elif answer == "Paper":
        await interaction.response.send_message(
          f"# You won to {answer}!\n\n ### Ready to challenge again? Do /play again."
        )


class tord(discord.ui.View):

  @discord.ui.button(label="Truth", style=discord.ButtonStyle.green)
  async def first_button_callback(self, button, interaction):
    async with aiohttp.ClientSession() as session:
      async with session.get(
          "https://api.truthordarebot.xyz/v1/truth") as request:
        data = await request.json()
        print(interaction.user)
        embed = discord.Embed(
          title=f"{data['question']}",
          description=f"Rating: {data['rating']}\nType: {data['type']}",
          color=discord.Colour.random())
        embed.set_author(name=f"Sent by: {interaction.user}",
                         icon_url=interaction.user.avatar.url)
        await update_truth()
        await interaction.response.send_message(embed=embed, view=tord())

  @discord.ui.button(label="Dare", style=discord.ButtonStyle.red)
  async def second_button_callback(self, button, interaction):
    async with aiohttp.ClientSession() as session:
      async with session.get(
          "https://api.truthordarebot.xyz/v1/dare") as request:
        data = await request.json()
        embed = discord.Embed(
          title=f"{data['question']}",
          description=f"Rating: {data['rating']}\nType: {data['type']}",
          color=discord.Colour.random())
        embed.set_author(name=f"Sent by: {interaction.user}",
                         icon_url=interaction.user.avatar.url)
        await update_dare()
        await interaction.response.send_message(embed=embed, view=tord())


@bot.command(description="Checks if the bot is online")
async def ping(ctx):
  await ctx.respond("🏓Pong!")


@bot.command(description="Repeats after you")
async def messenger(ctx: discord.ApplicationContext):
  modal = Messenger(title="Please enter text.")
  await ctx.send_modal(modal)


@bot.command(description="Get Help via the tables.")
async def help(ctx):
  await ctx.defer()
  my_pages = [
    Page(embeds=[
      discord.Embed(
        title="Basic Commands:",
        description=
        "/find - help for certain commands and bigger descriptions in 5.1.2+.\n/help - help - You are here.\n/messenger - Sends a private message in the area.\n/ping - Checks if the bot is alive\n/game - Plays rock paper scissors.\n/prompt - Gets responses from Google Bard, An AI\n/weather - Displays the weather for any city\n/dice - Rolls the dice\n/vote - Creates a vote.\n/fact - Gets a fact in 5.0.0+\n/flip - Flips a coin\n/ban - Bans a user (do not play with this feature) in 5.2.0+\n/kick - Kicks a user (do NOT play around with this feature) in 5.2.0+"
      ),
    ], ),
    Page(embeds=[
      discord.Embed(
        title="Advanced Commands:",
        description=
        "/vibe_check - Sees your vibe.\n/serverstats - Gets serverstats based on members and channels!\n/user avatar - Gets the avatar of a user in the server\n/user message - Direct Messages the user who does the command the text reverse!\n/truth - Does a Truth in 5.0.0+\n/dare - Does a Dare in 5.0.0+\n/tordstats - Gets all of the Truth or Dare stats in 5.0.0+\n/scratch user_avatar - Gets the Scratch Avatar in 5.0.0+\n/scratch rank - Gets the Scratch Rank of a user based on their country."
      )
    ], ),
    Page(embeds=[
      discord.Embed(
        title="Questions? Feedback?",
        description=
        "Direct Message @k3!\n\n**Patch notes:**\n```5.2.0:\nReadded kick and ban commands, If it does not work, it may mean that you do not have the roles to do so.```"
      )
    ], ),
  ]
  buttons = [
    PaginatorButton("first", label="<<", style=discord.ButtonStyle.blurple),
    PaginatorButton("prev", label="<", style=discord.ButtonStyle.blurple),
    PaginatorButton("page_indicator",
                    style=discord.ButtonStyle.gray,
                    disabled=True),
    PaginatorButton("next", label=">", style=discord.ButtonStyle.blurple),
    PaginatorButton("last", label=">>", style=discord.ButtonStyle.blurple),
  ]
  paginator = Paginator(
    pages=my_pages,
    show_indicator=True,
    use_default_buttons=False,
    custom_buttons=buttons,
  )
  await paginator.respond(ctx.interaction)


@bot.command(description="Fun game to check if you are human")
async def vibe_check(ctx):
  await ctx.respond("Support the bot!", ephemeral=True)
  msg = await ctx.send("Checking your vibe...")
  t.sleep(random.randint(2, 5))
  if random.randint(1, 2) == 1:
    await msg.edit(content="*You're good.*")
  else:
    await msg.edit(content="You're not good.")


@bot.command(description="Gets weather via https://weatherapi.com")
@option("city", str, description="Enter a city. Please use valid ones")
async def weather(ctx, city: discord.Option(str)):
  await ctx.defer()
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
@commands.cooldown(1, 5)
async def prompt(ctx, request: discord.Option(str)):
  await ctx.defer()
  async with aiohttp.ClientSession() as session:
    headers = {"Prompt": request, "Secure-1PSID": os.environ["bard"]}
    async with session.get(
        "https://text-generator-api.knightbot63.repl.co/ask",
        headers=headers) as r:
      data = await r.json()
      try:
        await ctx.respond(f"** > {request}**\n```{data['content']}```",
                          view=BardButton())
        await ctx.respond("✅Your content has been thru!", ephemeral=True)
      except Exception as e:
        await ctx.respond(f"The bot can't send the request because {e}")


@cats.command(description='Get a random cat image')
@commands.cooldown(1, 300)
async def image(ctx):
  await ctx.defer()
  async with aiohttp.ClientSession() as session:
    async with session.get('https://cataas.com/cat?html=false&json=true') as r:
      data = await r.json()
      await ctx.respond("https://cataas.com" + data['url'])


@bot.command(description='Range of Random Numbers')
@commands.cooldown(1, 10)
@option("first", int, description="Your first number")
@option("second", int, description="Your second number")
async def dice(ctx, first: discord.Option(int), second: discord.Option(int)):
  print("Ranging")
  print("Yes")
  rang = random.randint(first, second)
  await ctx.respond(
    f"{ctx.author.mention}\nFirst: {first}\nSecond: {second}\n Result: {rang}")

  await ctx.respond("Successfully sent!", ephemeral=True)


@bot.command(description="Fetches latest comment")
@option(
  "channel",
  str,
  description=
  "Enter the channel ID for the server the bot is in to get the latest comment."
)
async def fetch_latest(ctx, channel: discord.Option(str)):
  try:
    channel = bot.get_channel(int(channel))
    message = await channel.fetch_message(channel.last_message_id)
    await ctx.respond(
      f'Latest message in: #{channel.name} has been sent by @{message.author.name} at {message.created_at} \n**Message:**\n'
      + message.content)
  except:
    await ctx.respond("Failed to fetch.", ephemeral=True)


@bot.command(description="Makes a voting system")
@option("desc", str, description="Enter a description for your vote!")
async def create_vote(ctx, desc: discord.Option(str)):
  try:
    embed = discord.Embed(title="Vote:", description=desc)
    embed.set_footer(text="Upvote and Downvote about your expressions!")
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
    msg = await ctx.respond(embed=embed)
    message = await msg.original_response()
    await message.add_reaction("👍")
    await message.add_reaction("👎")
    await ctx.respond("Created the vote!", ephemeral=True)
  except Exception as e:
    await ctx.respond(
      "Some errors had occurred. Do not worry, this is in an alpha state.",
      ephemeral=True)


@bot.command(description="Plays a basic game of rick, paper, scissors")
async def play(ctx):
  await ctx.respond(f"Challenge accepted {ctx.author.mention}!")
  await ctx.send("Up to a battle of rock paper scissors from the bot?",
                 view=game())


@bot.command(description="Gets serverstats of the server.")
async def serverstats(ctx):
  await ctx.defer()
  embed = discord.Embed(title=f"Stats for {ctx.guild.name}")
  embed.add_field(name="Users:", value=ctx.guild.member_count, inline=False)
  embed.add_field(name="Channels:",
                  value=len(ctx.guild.channels),
                  inline=False)
  await ctx.respond(embed=embed)


@user.command(description="Sends the User in the Servers' avatar.")
@commands.cooldown(1, 30)
async def avatar(ctx, member: discord.Member = None):
  if member == None:
    member = ctx.author
  memberAvatar = member.avatar.url
  embed = discord.Embed(title=f"{member}'s Avatar:")
  embed.set_image(url=memberAvatar)
  embed.set_footer(text="To do this, do /user avatar and add a field")
  await ctx.respond(embed=embed)
  await ctx.respond("Sent!", ephemeral=True)


@cats.command(description="Get a nice little CAT fact")
async def fact(ctx):
  await ctx.defer()
  async with aiohttp.ClientSession() as session:
    async with session.get(
        "https://catfact.ninja/fact?max_length=9999") as request:
      data = await request.json()
      await ctx.respond(f"Fact: {data['fact']}")


@user.command(description="Reverses the text you said in a direct message")
@commands.cooldown(1, 60)
async def message(ctx, message: discord.Option(str)):
  await ctx.defer()
  await ctx.author.send(message[::-1])
  await ctx.respond(f"Please check your DM's {ctx.author.mention}!")


@bot.command(description="Gets a truth. Comes with 2 buttons.")
async def truth(ctx):
  async with aiohttp.ClientSession() as session:
    async with session.get(
        "https://api.truthordarebot.xyz/v1/truth") as request:
      data = await request.json()
      embed = discord.Embed(
        title=f"{data['question']}",
        description=f"Rating: {data['rating']}\nType: {data['type']}",
        color=discord.Colour.random())
      embed.set_author(name=f"Sent by: {ctx.author}",
                       icon_url=ctx.author.avatar.url)
      await update_truth()
      await ctx.respond(embed=embed, view=tord())


@bot.command(description="Gets a dare. Comes with 2 buttons.")
async def dare(ctx):
  async with aiohttp.ClientSession() as session:
    async with session.get(
        "https://api.truthordarebot.xyz/v1/dare") as request:
      data = await request.json()
      embed = discord.Embed(
        title=f"{data['question']}",
        description=f"Rating: {data['rating']}\nType: {data['type']}",
        color=discord.Colour.random())
      embed.set_author(name=f"Sent by: {ctx.author}",
                       icon_url=ctx.author.avatar.url)
      await update_dare()
      await ctx.respond(embed=embed, view=tord())


@bot.command(description="Truth or Dare stats Everywhere!")
async def tordstats(ctx):
  embed = discord.Embed(
    title="Truth or Dare Stats:",
    description=
    f"__Total Truths:__ {count_truth()}\n __Total Dares:__ {count_dare()}\n**Total in all:** {count_dare() + count_truth()}",
    color=discord.Colour.random())
  await ctx.respond(embed=embed)


@scratch.command(description="Random Scratch Project with Thumbnail and info")
@option("user", str, description="Enter a username")
async def user_avatar(ctx, user: discord.Option(str)):
  async with aiohttp.ClientSession() as session:
    async with session.get(
        f"https://apis.scratchconnect.eu.org/free-proxy/get?url=https://api.scratch.mit.edu/users/{user}"
    ) as request:
      try:
        await ctx.defer()
        data = await request.json()
        embed = discord.Embed(title=f"Request Name: {user}",
                              color=discord.Colour.random())
        embed.set_author(name=f"Sent by: {ctx.author}",
                         icon_url=ctx.author.avatar.url)
        embed.set_image(url=data['profile']['images']['90x90'])
        await ctx.respond(embed=embed)
        await ctx.respond("Sent!", ephemeral=True)
      except:
        try:
          await ctx.respond(
            f"Sorry, I can't get the user {user} because they don't exist on Scratch."
          )
        except:
          print("Failed to parse as ephemeral")


@scratch.command(
  description="Get a Scratch User's profile simulated in an embed!")
@option("user", str, description="Enter a Scratch Username.")
async def profile(ctx, user: discord.Option(str)):
  async with aiohttp.ClientSession() as session:
    async with session.get(
        f"https://apis.scratchconnect.eu.org/free-proxy/get?url=https://api.scratch.mit.edu/users/{user}"
    ) as request:
      data = await request.json()
      await ctx.defer()
      name = data["username"]
      id = data["id"]
      scratchteam = data["scratchteam"]
      joined = data["history"]["joined"]
      profile_url = data["profile"]["images"]["90x90"]
      work = data["profile"]["status"]
      about = data["profile"]["bio"]
      country = data["profile"]["country"]
      if about == '':
        about = "Nothing written."
      try:
        embed = discord.Embed(
          title=f"@{name}",
          description=
          f"#{id} | Scratch Team: {scratchteam} | Join Date: {joined} | Country: {country}",
          color=discord.Colour.random())
        embed.add_field(name="About Me", value=about, inline=False)
        embed.add_field(name=chr(173), value=chr(173))
        embed.add_field(name="What I'm Working On", value=work, inline=False)
        embed.set_thumbnail(url=profile_url)
        embed.set_footer(
          text="Do /scratch profile to get the result of this command")
        await ctx.respond(embed=embed)
      except Exception as e:
        await ctx.respond(
          f"Sorry, I can't get the user @{user} because @{user} doesn't exist! If this is wrong, please contact @k3 for troubleshooting. Here is the error: {e}"
        )


@bot.command(description="Get a fact!")
async def fact(ctx):
  async with aiohttp.ClientSession() as session:
    async with session.get(
        'https://uselessfacts.jsph.pl/random.json?language=en') as response:
      result = await response.json()
      fact = result['text']
      response = f'Fun fact: {fact}'
      await ctx.respond(response)



@bot.command(description="Flip a coin")
async def flip(ctx):
  dice = random.choice(["heads", "tails"])
  await ctx.respond(f"The coin landed on {dice}!")


@bot.command(description="Get help on a certain command")
@option("command", str, description="Command you need help with. This is NOT case sensitive")
async def find(ctx, command: discord.Option(str)):
  resp = find_command(command.lower())
  if resp['found'] == True:
    embed = discord.Embed(title=f"Command:\n{command}", color=discord.Colour.green())
    embed.add_field(name='Description:', value=resp['desc'], inline=True)
    embed.set_footer(text="Brought by the /find command")
    await ctx.respond(embed=embed)
  else:
    embed = discord.Embed(title="Command not found", color=discord.Colour.red())
    embed.add_field(name="Error", value=f"Command {command} was not found.")
    await ctx.respond(embed=embed, ephemeral=True)

@bot.command(description="Bans a user")
@commands.has_permissions(ban_members=True)
@option("reason", str, description="Reason why you want the user to be banned")
async def ban(ctx, member: discord.Member, reason=None):
  if member == ctx.author:
    print("1")
    await ctx.respond("❌You can not ban yourself", ephemeral=True)
  elif ctx.guild.me == member:
    print(2)
    await ctx.respond("Think you can ban me by my own command????", ephemeral=True)
  elif member.guild_permissions.manage_messages:
    print(3)
    await ctx.respond("❌You can't ban a moderator/admin or bot!", ephemeral=True)
  elif member.bot:
    print(4)
    await ctx.send("❌You can't ban a bot!", ephemeral=True)
  else:
    if reason == None:
      reason = "No reason Provided."
    await member.send(f"Sorry, you have been banned from the server: {ctx.guild.name}. Reason: {reason}")
    await member.ban(reason=reason)
    await ctx.respond("Successfully banned the user!", ephemeral=True)


@bot.command(description="Kicks a user")
@option("reason", str, description="Reason why you want the user to be kicked")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, reason=None):
  if member == ctx.author:
    print("1")
    await ctx.respond("❌You can not ban yourself", ephemeral=True)
  elif ctx.guild.me == member:
    print(2)
    await ctx.respond("Think you can ban me by my own command????", ephemeral=True)
  elif member.guild_permissions.manage_messages:
    print(3)
    await ctx.respond("❌You can't ban a moderator/admin or bot!", ephemeral=True)
  elif member.bot:
    print(4)
    await ctx.send("❌You can't ban a bot!", ephemeral=True)
  else:
    await member.send(f'You have been kicked from {ctx.guild.name}. Reason: {reason}')
    await member.kick(reason=reason)
    await ctx.respond(f'Kicked {member.mention}. Reason: {reason}', ephemeral=True)

        
@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
    if message.author.bot:
      return

@bot.event
async def on_application_command_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    await ctx.respond(f"Sorry, please wait {error.retry_after:.2f}s before trying again.", ephemeral=True)

@bot.event
async def on_ready():
  print(f"{bot.user} is online")


bot.run(os.environ['token'])

#700+ lines o-o
# Woah
