import os
import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Suivi de l'état et des cibles par serveur
active_servers = set()
target_users = {}

def mommy_transform(text):
    prefixes = [
        "Tu l'ouvres encore, petit... ",
        "Oh, tu oses l'ouvrir ? ",
        "Tu penses pouvoir commander, doux agneau ? ",
        "Regarde-moi bien dans les yeux et écoute : ",
        "Tu fais moins le malin tout d'un coup... "
    ]
    
    suffixes = [
        f" ...et tu vas obéir au doigt et à l'œil, pas vrai ?~",
        f" ...tu ne me décevras pas, n'est-ce pas ?~",
        f" ...à genoux, c'est tout ce que tu mérites~",
        f" ...maintenant, cours exécuter mes ordres~",
        f" ...hihi, tu n'as pas vraiment le choix de toute façon~"
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
        await ctx.send("Mode Mommy désactivé. Dommage pour eux... 💅")
    else:
        active_servers.add(ctx.guild.id)
        await ctx.send("Mode Mommy activé. Préparez-vous à vous faire dominer. ✨")

@bot.command(name="mommy-target")
@commands.has_permissions(administrator=True)
async def set_target(ctx, member: discord.Member):
    target_users[ctx.guild.id] = member.id
    await ctx.send(f"Cible verrouillée : {member.mention} va devoir filer droit. 👑")

@bot.event
async def on_message(message):
    if message.author.bot or not message.guild:
        return

    guild_id = message.guild.id

    if guild_id in active_servers and guild_id in target_users:
        if message.author.id == target_users[guild_id]:
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

    await bot.process_commands(message)

token = os.getenv("DISCORD_TOKEN")
bot.run(token)
