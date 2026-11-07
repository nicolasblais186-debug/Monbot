import os
import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Suivi de l'état (actif ou non par serveur) et des cibles
active_servers = set()
target_users = {}

def mommy_transform(text):
    lower_text = text.lower()
    
    # Correction de la syntaxe Python ici (in word)
    keywords = ["viens", "aller", "film", "cinéma", "manger", "restaurant", "sortir", "partir"]
    if any(word in lower_text for word in keywords):
        prefixes = [
            f"Mh, tu proposes *\"{text}\"* ? Oh, ",
            f"Tu dis *\"{text}\"* ? Disons plutôt que ",
            f"Tu as osé dire *\"{text}\"* ? Très bien, alors ",
            f"En disant *\"{text}\"*, tu t'imagines quoi ? "
        ]
        suffixes = [
            f"oui mon chou, j'aimerais bien venir avec toi~ Si c'est un film d'horreur, je te laisserais peut-être même te coller à moi~~",
            f"compte sur moi pour t'accompagner, et tu me porteras mon sac tout du long, pas vrai ?~",
            f"je viens, mais c'est uniquement pour te surveiller de très près, petit agneau~",
            f"j'accepte ton invitation, à condition que tu m'obéisses pour tout le reste de la soirée~"
        ]
    else:
        prefixes = [
            f"Tu l'ouvres en disant *\"{text}\"*... Mais en vrai, ",
            f"Tu penses m'impressionner avec *\"{text}\"* ? Laisse-moi reformuler : ",
            f"À force de dire *\"{text}\"*, ",
            f"Mh... *\"{text}\"*, c'est mignon, mais "
        ]
        suffixes = [
            f"tu penses surtout à moi toute la journée, avoue-le~",
            f"tu finiras par venir ramper à mes pieds de toute façon, mon petit agneau~",
            f"tu vas obéir sagement sans chercher à comprendre, hihi~",
            f"tu restes mon petit jouet préféré dans ce salon~"
        ]
    
    prefix = random.choice(prefixes)
    suffix = random.choice(suffixes)
    
    return f"{prefix}{suffix}"

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")

@bot.command(name="mommy")
@commands.has_permissions(administrator=True)
async def toggle_mommy(ctx):
    if ctx.guild.id in active_servers:
        active_servers.remove(ctx.guild.id)
        if ctx.guild.id in target_users:
            del target_users[ctx.guild.id]
        await ctx.send("Mode Mommy désactivé. La récré est finie pour tout le monde... 💅")
    else:
        active_servers.add(ctx.guild.id)
        await ctx.send("Mode Mommy activé sur ce salon. Préparez-vous à devenir mes agneaux. ✨")

@bot.command(name="mommy-target")
@commands.has_permissions(administrator=True)
async def set_target(ctx, member: discord.Member):
    target_users[ctx.guild.id] = member.id
    active_servers.add(ctx.guild.id)
    await ctx.send(f"Cible verrouillée : {member.mention} va désormais se faire piéger à chacun de ses messages. 👑")

@bot.event
async def on_message(message):
    if message.author.bot or not message.guild:
        return

    guild_id = message.guild.id

    if guild_id in active_servers:
        if message.content.startswith("!"):
            await bot.process_commands(message)
            return

        should_transform = False
        if guild_id in target_users:
            if message.author.id == target_users[guild_id]:
                should_transform = True
        else:
            should_transform = True

        if should_transform:
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
