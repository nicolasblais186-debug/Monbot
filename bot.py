import os
import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Suivi de l'état (actif ou non par serveur)
active_servers = set()

def mommy_transform(text):
    prefixes = [
        f"Oh, tu dis *\"{text}\"* ? C'est mignon de t'entendre essayer de commander... ",
        f"Mh, vraiment ? *\"{text}\"*, c'est tout ce que tu trouves à dire ? ",
        f"Tu l'ouvres avec *\"{text}\"* ? Voyons voir si tu assumes jusqu'au bout, petit... ",
        f"Tu penses m'impressionner en disant *\"{text}\"* ? Continue, j'écoute... ",
        f"Regarde un peu ce que tu écris : *\"{text}\"*. Tu fais moins le malin, non ? "
    ]
    
    suffixes = [
        f" ...mais tu finiras par obéir quand même, pas vrai ?~",
        f" ...tu ne me décevras pas sur ce coup-là, si ?~",
        f" ...viens donc faire un petit effort pour moi~",
        f" ...hihi, tu n'as pas vraiment le choix de toute façon~",
        f" ...reste sagement à ta place, mon petit agneau~"
    ]
    
    prefix = random.choice(prefixes)
    suffix = random.choice(suffixes)
    
    return f"{prefix}*{text}*{suffix}"

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")

@bot.command(name="mommy")
@commands.has_permissions(administrator=True)
async def toggle_mommy(ctx):
    if ctx.guild.id in active_servers:
        active_servers.remove(ctx.guild.id)
        await ctx.send("Mode Mommy désactivé. Dommage, la récré est finie... 💅")
    else:
        active_servers.add(ctx.guild.id)
        await ctx.send("Mode Mommy activé sur ce salon. Préparez-vous à devenir mes agneaux. ✨")

@bot.event
async def on_message(message):
    if message.author.bot or not message.guild:
        return

    guild_id = message.guild.id

    if guild_id in active_servers:
        if message.content.startswith("!"):
            await bot.process_commands(message)
            return

        if message.channel.permissions_for(message.guild.me).manage_webhooks:
            webhooks = await message.channel.webhooks()
            webhook = discord.utils.get(webhooks, name="MommyLock")
            if not webhook:
                webhook = await message.channel.create_webhook(name="MommyLock")

            new_content = mommy_transform(message.content)
            await message.delete()

            avatar = message.author.display_avatar.url if message.author.display_avatar else message.author.default_avatar.url
            await webhook.send(
                content=new_content,
                username=message.author.display_name,
                avatar_url=avatar
            )
            return

    await bot.process_commands(message)

token = os.getenv("DISCORD_TOKEN")
bot.run(token)
