import os
import discord
from discord.ext import commands
import random
from flask import Flask
from threading import Thread

# Serveur web factice pour maintenir le bot éveillé sur Render (Port 8080)
app = Flask('')

@app.route('/')
def home():
    return "Bot MommyLock (Ultimate Edition) en ligne 24h/24 !"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Configuration du bot Discord
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Suivi par serveur : états, cibles et modes de personnalité (False = Teasing, True = Vraie Mommy Dominante)
active_servers = set()
target_users = {}
mommy_mode_heavy = {}  # True si le mode dominant extrême est activé

def mommy_transform(text, is_heavy_mode):
    clean_text = text.strip()
    lower_text = text.lower()
    
    # ----------------------------------------------------
    # MODE 1 : VRAIE MOMMY DOMINANTE (Plus cash, autoritaire et possessive)
    # ----------------------------------------------------
    if is_heavy_mode:
        if any(w in lower_text for w in ["yo", "salut", "hey", "bonjour", "cc", "coucou", "slt"]):
            flavor = [f"Tu arrives en lâchant '{clean_text}'..."]
            action = ["à genoux tout de suite, tu n'as pas le droit de parler sans permission~", "viens te faire pardonner ton insolence immédiatement, mon agneau~"]
        elif any(w in lower_text for w in ["jeu", "jouer", "game", "vocal", "voc", "partie", "lancer"]):
            flavor = [f"Tu veux faire ça ('{clean_text}')..."]
            action = ["tu vas m'obéir au doigt et à l'œil et me carry en silence sans broncher~", "tu vas te faire dominer du début à la fin, c'est moi qui donne les ordres ici~"]
        elif any(w in lower_text for w in ["viens", "aller", "film", "cinéma", "resto", "manger", "sortir"]):
            flavor = [f"Tu oses planifier '{clean_text}'..."]
            action = ["tu marcheras sagement en laisse derrière moi sans un mot~", "tu me porteras mon sac et tu te tairas tout le long~"]
        else:
            flavor = [
                f"À force de l'ouvrir avec '{clean_text}'...", 
                f"Te voir écrire '{clean_text}'..."
            ]
            action = [
                "tu me dois le respect, maintenant baise les yeux et obéis~", 
                "tu m'appartiens corps et âme, arrête de faire l'enfant roi~",
                "à genoux, c'est ta seule place quand tu t'adresses à moi~"
            ]
            
    # ----------------------------------------------------
    # MODE 2 : MODE TEASING / TAQUIN (Plus subtil, complice et vicieux)
    # ----------------------------------------------------
    else:
        if any(w in lower_text for w in ["yo", "salut", "hey", "bonjour", "cc", "coucou", "slt"]):
            flavor = [f"Oh, tu pointes le bout de ton nez avec un petit '{clean_text}'..."]
            action = ["viens vite me faire un câlin pour te faire pardonner~", "tu tombes bien, j'avais justement besoin d'un petit toutou à taquiner~"]
        elif any(w in lower_text for w in ["jeu", "jouer", "game", "vocal", "voc", "partie", "lancer", "lol", "val"]):
            flavor = [f"Tu proposes de '{clean_text}'..."]
            action = ["je veux bien, mais tu seras mon petit support personnel toute la game, hihi~", "tu vas devoir me carry si tu veux espérer gagner un peu d'attention~"]
        elif any(w in lower_text for w in ["viens", "aller", "film", "cinéma", "resto", "manger", "sortir"]):
            flavor = [f"Tu as des envies de bouger avec '{clean_text}'..."]
            action = ["je veux bien t'accompagner, mais c'est moi qui choisis tout sur place~", "compte sur moi, à condition que tu restes sagement collé à moi~"]
        else:
            flavor = [
                f"À force de répéter '{clean_text}'...", 
                f"C'est mignon d'écrire '{clean_text}'..."
            ]
            action = [
                "tu prouves juste que tu penses à moi toute la journée, avoue~", 
                "viens t'asseoir sagement à mes pieds au lieu de raconter ça~",
                "tu n'as pas le choix, tu vas te faire taquiner quand même~"
            ]
            
    return f"{random.choice(flavor)} {random.choice(action)}"

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")

@bot.command(name="mommy")
@commands.has_permissions(administrator=True)
async def toggle_mommy(ctx):
    guild_id = ctx.guild.id
    if guild_id in active_servers:
        active_servers.remove(guild_id)
        if guild_id in target_users:
            del target_users[guild_id]
        if guild_id in mommy_mode_heavy:
            del mommy_mode_heavy[guild_id]
        await ctx.send("Mode Mommy désactivé. La récré est finie pour tout le monde... 💅")
    else:
        active_servers.add(guild_id)
        mommy_mode_heavy[guild_id] = False  # Par défaut en mode teasing
        await ctx.send("Mode Mommy activé (Mode Teasing). Préparez-vous à devenir mes agneaux. ✨")

@bot.command(name="mommy-target")
@commands.has_permissions(administrator=True)
async def set_target(ctx, member: discord.Member):
    guild_id = ctx.guild.id
    target_users[guild_id] = member.id
    active_servers.add(guild_id)
    if guild_id not in mommy_mode_heavy:
        mommy_mode_heavy[guild_id] = False
    await ctx.send(f"Cible verrouillée : {member.mention} va désormais se faire piéger à chacun de ses messages. 👑")

@bot.command(name="mommy-mode")
@commands.has_permissions(administrator=True)
async def toggle_heavy_mode(ctx):
    guild_id = ctx.guild.id
    if guild_id not in active_servers:
        await ctx.send("Le mode Mommy n'est même pas activé sur ce serveur ! Tape `!mommy` d'abord.")
        return
    
    # Inverser le mode (Teasing <-> Vraie Mommy)
    current_state = mommy_mode_heavy.get(guild_id, False)
    mommy_mode_heavy[guild_id] = not current_state
    
    if mommy_mode_heavy[guild_id]:
        await ctx.send("⚠️ **VRAI MODE MOMMY ACTIVÉ** : Le ton devient intransigeant et purement dominant. Fini de rire. 👑")
    else:
        await ctx.send("✨ Retour au **Mode Teasing** : Un poil plus taquin et joueur. 💅")

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

                # Récupérer l'état du mode (False par défaut)
                is_heavy = mommy_mode_heavy.get(guild_id, False)

                new_content = mommy_transform(message.content, is_heavy)
                await message.delete()

                avatar = message.author.display_avatar.url if message.author.display_avatar else message.author.default_avatar.url
                await webhook.send(
                    content=new_content,
                    username=message.author.display_name,
                    avatar_url=avatar
                )
                return

    await bot.process_commands(message)

if __name__ == "__main__":
    keep_alive()
    token = os.getenv("DISCORD_TOKEN")
    bot.run(token)
