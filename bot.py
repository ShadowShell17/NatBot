import random
import discord
from discord import app_commands
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from config import token


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
meme_list = ["with Jett", "with Harbor", "with Deadlock", "Valorant", "Starcraft II", "Stormgate", "League of Legends",
             "Sonic 06"]


def pull_card_text(text_interaction):
    html_page = "https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=1&sess=1&rp=10&mode=&sort=1&keyword="\
                + text_interaction
    html_page = html_page.replace(' ', '+')
    response = requests.get(html_page)
    soup = BeautifulSoup(response.text, 'html.parser')
    res = soup.find(id="card_list")
    card_name = res.find(class_='card_name')
    image_location = res.find('img')
    card_image = image_location.find('src')
    card_text = res.find(class_='box_card_text c_text flex_1')

    return card_name.text.strip(), card_text.text.strip(), card_image


def get_random_team(name_list):
    new_list = name_list.split(",")
    new_team = {}
    count = 0
    random.shuffle(new_list)
    for i in new_list:
        i.strip()
        if count % 2:
            new_team[i] = 1
        else:
            new_team[i] = 2
        count += 1
    return new_team


@bot.event
async def on_ready():
    print("Bot is up and ready!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(random.choice(meme_list)))
    except Exception as e:
        print(e)


@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}! This is a slash command!", ephemeral=True)


@bot.tree.command(name="say")
@app_commands.describe(thing_to_say="What should I say?")
async def say(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(f"{interaction.user.name} said: '{thing_to_say}'")


@bot.tree.command(name="coin_flip")
async def coin_flip(interaction: discord.Interaction):
    await interaction.response.send_message(f"You got: {random.choice(['heads', 'tails'])}. This was generated "
                                            f"using a deterministic random algorithm.")


@bot.tree.command(name="yugioh_card")
@app_commands.describe(looking_up="What am I looking up?")
async def yugioh_card(interaction: discord.Interaction, looking_up: str):
    await interaction.response.send_message(f"```{pull_card_text(looking_up)}```")


@bot.tree.command(name="random_team")
@app_commands.describe(team_input="give me a list seperated by comma's")
async def random_team(interaction: discord.Interaction, team_input: str):
    await interaction.response.send_message(f"```{get_random_team(team_input)}```")


bot.run(token)
