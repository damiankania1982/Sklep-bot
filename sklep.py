import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Przykładowy sklep
shop_items = {
    "apteczka": 50,
    "maczeta": 100,
    "jedzenie": 30
}

user_balance = {}  # Sztuczna ekonomia do testów

@bot.event
async def on_ready():
    print(f'Zalogowano jako {bot.user}!')
    try:
        synced = await bot.tree.sync()
        print(f"Zsynchronizowano {len(synced)} komend slash.")
    except Exception as e:
        print(e)

@bot.tree.command(name="sklep", description="Zobacz dostępne przedmioty w sklepie")
async def sklep(interaction: discord.Interaction):
    message = "**Dostępne przedmioty w sklepie:**\n"
    for item, price in shop_items.items():
        message += f"- {item.title()}: {price} $Z\n"
    await interaction.response.send_message(message)

@bot.tree.command(name="kup", description="Kup przedmiot ze sklepu")
@app_commands.describe(item="Nazwa przedmiotu do kupienia")
async def kup(interaction: discord.Interaction, item: str):
    user_id = str(interaction.user.id)
    item = item.lower()

    if item not in shop_items:
        await interaction.response.send_message("Taki przedmiot nie istnieje!", ephemeral=True)
        return

    price = shop_items[item]
    balance = user_balance.get(user_id, 100)  # domyślnie 100$

    if balance >= price:
        user_balance[user_id] = balance - price
        await interaction.response.send_message(f"Kupiłeś **{item}** za {price} $Z. Pozostało: {user_balance[user_id]} $Z")
    else:
        await interaction.response.send_message(f"Masz za mało kasy! Masz tylko {balance} $Z.", ephemeral=True)
