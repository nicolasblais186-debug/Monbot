import os
import discord
from discord.ext import commands
import random
from flask import Flask
from threading import Thread

# Serveur web factice pour maintenir le bot éveillé sur Render (évite le timeout du port)
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
    clean_text = text.strip()
    
    # 1. SALUTATIONS : Conserve l'accueil mais le rend possessif
    if any(w in lower_text for w in ["yo", "salut", "hey", "bonjour", "cc", "coucou", "slt"]):
        responses = [
            f"Yo mon cœur, tu tombes bien viens me faire un câlin tout de suite~",
            f"Salut mon petit agneau, viens par ici te faire pardonner ton retard~",
            f"Oh, tu dis {clean_text} ? Viens le répéter en t'agenouillant devant moi, que j'écoute mieux~",
            f"Hey ! C'est bien de te pointer, tu vas pouvoir me tenir compagnie sagement~"
        ]
    
    # 2. SORTIES / BOUFFE / DÉPLACEMENTS : Garde l'idée de bouger mais impose les règles
    elif any(w in lower_text for w in ["viens", "aller", "film", "cinéma", "resto", "manger", "restaurant", "sortir", "partir", "rejoindre", "parc", "bouffer"]):
        responses = [
            f"Je veux bien qu'on aille {clean_text.replace('aller', '').replace('viens', '').strip()}, mais c'est moi qui décide de tout une fois sur place~~",
            f"Tu proposes de {clean_text} ? D'accord, mais uniquement si tu me tiens en laisse tout du long, mon toutou~",
            f"J'accepte ton plan pour {clean_text}, à condition que tu m'obéisses au doigt et à l'œil~",
            f"Compte sur moi, et tu porteras mon sac sans un mot pendant qu'on fait ça~"
        ]
        
    # 3. JEUX VIDÉO / VOCAL : Conserve l'envie de jouer mais le transforme en esclave de game
    elif any(w in lower_text for w in ["jeu", "jouer", "game", "vocal", "voc", "partie", "rejoignez", "pv", "lancer", "lol", "val"]):
        responses = [
            f"Tu veux {clean_text} ? Très bien, mais tu vas me carry en silence et sans rager si tu ne veux pas d'ennuis~",
            f"Tu veux lancer {clean_text} ? OK, mais tu seras mon petit support personnel toute la partie, hihi~",
            f"Viens {clean_text} tout de suite, j'ai envie d'entendre ta petite voix trembler un peu pour moi~",
            f"On peut {clean_text}, mais seulement si tu acceptes de te faire dominer du début à la fin~"
        ]
        
    # 4. PROVOCATIONS / CLASHS : Retourne l'attaque avec du mépris dominant
    elif any(w in lower_text for w in ["ferme", "gueule", "tais", "ftg", "nul", "pire", "déteste", "pense", "fermes", "con", "idiot"]):
        responses = [
            f"Mh, tu oses dire *\"{clean_text}\"*... Viens répéter ça un peu plus près de mes pieds, qu'on rigole~",
            f"Tu fais le malin en disant *\"{clean_text}\"*, mais on sait tous très bien qui commande ici, mon petit agneau~",
            f"Ose me redonner un ordre ou dire *\"{clean_text}\"* sur ce ton et tu vas passer un très mauvais quart d'heure~",
            f"C'est adorable d'essayer de dire *\"{clean_text}\"*, continue un peu, j'adore quand tu t'enfonces~"
        ]
        
    # 5. QUESTIONS : Garde le fond de la question mais recadre
    elif any(w in lower_text for w in ["pourquoi", "comment", "qui", "quoi", "est", "sait", "quel", "quand", "où", "?"]):
        responses = [
            f"Tu demandes *\"{clean_text}\"* ? Tu poses beaucoup trop de questions pour quelqu'un qui devrait m'obéir sagement~",
            f"Tu te demandes *\"{clean_text}\"*, mais la seule chose à retenir c'est que tu m'appartiens, hihi~",
            f"Tu cherches la réponse à *\"{clean_text}\"* ? Demande-moi gentiment à genoux et j'y réfléchirai~"
        ]
        
    # 6. CAS GÉNÉRAL (Le plus important) : Intégration directe et logique du message exact de la cible
    else:
        responses = [
            f"Tu dis *\"{clean_text}\"*, mais au fond tu penses à moi toute la journée, avoue-le donc~",
            f"C'est mignon de vouloir dire *\"{clean_text}\"*, mais viens t'asseoir sagement à mes pieds maintenant~",
            f"À force de dire *\"{clean_text}\"*, tu prouves juste que tu m'appartiens déjà un peu trop, hihi~",
            f"Tu racontes *\"{clean_text}\"*, mais tu n'as pas le choix, tu vas m'obéir quand même~",
            f"Regarde-moi bien quand tu écris *\"{clean_text}\"*... tu sais très bien que tu es à moi~"
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
    keep_alive()
    token = os.getenv("DISCORD_TOKEN")
    bot.run(token)
