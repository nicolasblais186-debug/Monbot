import os
import discord
from discord.ext import commands
import random
from flask import Flask
from threading import Thread

# Serveur web factice pour maintenir le bot éveillé sur Render
app = Flask('')

@app.route('/')
def home():
    return "Bot MommyLock en ligne 24h/24 !"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Configuration du bot Discord
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

active_servers = set()
target_users = {}

def mommy_transform(text):
    lower_text = text.lower()
    
    # 1. Salutations et messages d'accueil
    if any(w in lower_text for w in ["yo", "salut", "hey", "bonjour", "cc", "coucou", "slt"]):
        responses = [
            f"Yo mon cœur, tu tombes bien viens me faire un câlin tout de suite~",
            f"Salut mon petit agneau, viens par ici te faire pardonner ton retard~",
            f"Oh, tu dis yo ? Viens le répéter en t'agenouillant devant moi, que j'écoute mieux~",
            f"Hey ! C'est bien de te pointer, tu vas pouvoir me tenir compagnie sagement~",
            f"Regardez qui pointe le bout de son nez... Viens là que je m'occupe de toi~"
        ]
    # 2. Sorties, cinéma, bouffe, déplacements
    elif any(w in lower_text for w in ["viens", "aller", "film", "cinéma", "resto", "manger", "restaurant", "sortir", "partir", "rejoindre", "parc", "bouffer"]):
        responses = [
            f"Oui mon chou, j'aimerais trop venir avec toi~ Et si on y va, c'est moi qui décide de tout~~",
            f"Je veux bien t'accompagner, mais c'est uniquement pour te tenir en laisse toute la sortie, mon toutou~",
            f"J'accepte ton invitation, à condition que tu m'obéisses au doigt et à l'œil pendant qu'on y est~",
            f"Compte sur moi pour venir, et tu me porteras mon sac sans un mot, n'est-ce pas ?~",
            f"Oh oui, emmène-moi... mais prépare-toi à ce que ce soit moi qui commande sur place~"
        ]
    # 3. Jeux vidéo, vocaux, parties
    elif any(w in lower_text for w in ["jeu", "jouer", "game", "vocal", "voc", "partie", "rejoignez", "pv", "lancer", "vocal?"]):
        responses = [
            f"Je viens sur le jeu, mais tu vas me carry en silence et sans rager si tu ne veux pas d'ennuis~",
            f"Viens en voc tout de suite, j'ai envie d'entendre ta petite voix trembler un peu pour moi~",
            f"Je lance avec toi, mais tu seras mon petit support personnel toute la partie, hihi~",
            f"Tu veux qu'on fasse une session ? Seulement si tu acceptes de te faire dominer du début à la fin~",
            f"Je pointe le bout de mon nez sur le jeu, mais c'est toi qui m'exécutes tous mes objectifs~"
        ]
    # 4. Clashs, insultes, provocations
    elif any(w in lower_text for w in ["ferme", "gueule", "tais", "ftg", "nul", "pire", "déteste", "pense", "fermes", "con", "idiot", "nul"]):
        responses = [
            f"Mh, tu l'ouvres bien grand dis donc... Viens répéter ça un peu plus près de mes pieds, qu'on rigole~",
            f"Tu fais le malin derrière ton écran, mais on sait tous très bien qui commande ici, mon petit agneau~",
            f"Ose me redonner un ordre sur ce ton et tu vas passer un très, très mauvais quart d'heure~",
            f"C'est adorable de t'entendre essayer de te rebeller, continue un peu, j'adore quand tu t'enfonces~",
            f"À genoux, c'est tout ce que tu mérites quand tu l'ouvres un peu trop à mon goût~"
        ]
    # 5. Questions ou tournures interrogatives
    elif any(w in lower_text for w in ["pourquoi", "comment", "qui", "quoi", "est", "sait", "quel", "quand", "où", "?"]):
        responses = [
            f"Tu poses beaucoup de questions pour quelqu'un qui devrait plutôt m'obéir sagement~",
            f"Tu te demandes plein de trucs, mais la seule chose à retenir c'est que tu m'appartiens, hihi~",
            f"Laisse tomber ces détails et viens plutôt me prouver ta loyauté, mon toutou~",
            f"Tu cherches des réponses ? Demande-moi gentiment à genoux et j'y réfléchirai peut-être~"
        ]
    # 6. Cas général : le bot s'approprie subtilement le message de la cible
    else:
        responses = [
            f"Tu dis *\"{text}\"*, mais au fond tu penses à moi toute la journée, avoue-le donc~",
            f"C'est mignon de dire *\"{text}\"*, mais viens t'asseoir sagement à mes pieds maintenant~",
            f"À force de dire *\"{text}\"*, tu prouves juste que tu m'appartiens déjà un peu trop, hihi~",
            f"Tu racontes *\"{text}\"*, mais tu n'as pas le choix, tu vas m'obéir quand même~",
            f"Regarde-moi bien quand tu écris *\"{text}\"*... tu sais très bien que tu es à moi~"
        ]
    
    return random.choice(responses)

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

if __name__ == "__main__":
    keep_ai = keep_alive()
    token = os.getenv("DISCORD_TOKEN")
    bot.run(token)
