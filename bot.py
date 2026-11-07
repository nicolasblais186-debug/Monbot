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
    # Un dictionnaire de tournures bien plus poussées, dominantes et sensuelles
    prefixes = [
        f"Oh, {text} ? Regarde-moi bien dans les yeux quand tu parles, petit chien... ",
        f"Tu l'ouvres encore avec cette petite voix tremblante ? Tu dis : *\"{text}\"* ? ",
        f"Mh... Tu oses l'ouvrir devant moi en disant *\"{text}\"* ? Quel toupet adoré... ",
        f"Tu penses pouvoir commander ou proposer des trucs comme *\"{text}\"*, doux agneau ? ",
        f"Regarde ta propre phrase *\"{text}\"*... Tu fais tellement moins le malin tout d'un coup... ",
        f"Tu rampes déjà en disant *\"{text}\"* ? C'est pathétique, j'adore... "
    ]
    
    suffixes = [
        f" ...et tu vas obéir au doigt et à l'œil pour m'accompagner, pas vrai ?~",
        f" ...tu ne me décevras pas sur ce coup-là, n'est-ce pas mon toutou ?~",
        f" ...à genoux, c'est exactement ta place quand tu l'ouvres~",
        f" ...maintenant, viens lécher mes bottes et cours exécuter mes ordres~",
        f" ...hihi, tu n'as pas le moindre choix de toute façon, alors obéis~",
        f" ...viens donc te faire promener en theière, sale petit soumis~"
    ]
    
    prefix = random.choice(prefixes)
    suffix = random.choice(suffixes)
    
    # On intègre le message original en l'enrobant de manière bien trash/dominante
    return f"{prefix}*{text}*{suffix}"

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")

@bot.command(name="mommy")
@commands.has_permissions(administrator=True)
async def toggle_mommy(ctx):
    if ctx.guild.id in active_servers:
        active_servers.remove(ctx.guild.id)
        await ctx.send("Mode Mommy désactivé. Dommage pour leur liberté... 💅")
    else:
        active_servers.add(ctx.guild.id)
        await ctx.send("Mode Mommy activé sur ce salon. Préparez-vous à tous devenir mes toutous. ✨")

@bot.event
async def on_message(message):
    # Le bot ne réagit pas à ses propres messages ni aux autres bots, et doit être activé sur le serveur
    if message.author.bot or not message.guild:
        return

    guild_id = message.guild.id

    # Si le mode mommy est activé, le bot attrape TOUT le monde (sauf les admins si tu veux, ou tout le monde pour le troll)
    if guild_id in active_servers:
        # On évite de s'auto-trigger ou de modifier les commandes du bot
        if message.content.startswith("!"):
            await bot.process_commands(message)
            return

        if message.channel.permissions_for(message.guild.me).manage_webhooks:
            webhooks = await message.channel.webhooks()
            webhook = discord.utils.get(webhooks, name="MommyLock")
            if not webhook:
                webhook = await message.channel.create_webhook(name="MommyLock")

            # On transforme le message avec le nouveau vocabulaire poussé
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
