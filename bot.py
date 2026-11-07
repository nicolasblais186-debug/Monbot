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
    
    # 1. Sorties, cinoche, bouffe, balades
    if any(w in lower_text for w in ["viens", "aller", "film", "cinéma", "resto", "manger", "restaurant", "sortir", "partir", "rejoindre", "dehors", "parc"]):
        phrases = [
            f"Oui mon chou, j'aimerais trop venir avec toi~ Et si c'est un film d'horreur, je te laisserai peut-être même te coller à moi par peur~~",
            f"Je veux bien t'accompagner, mais c'est uniquement pour te tenir en laisse toute la sortie, petit agneau~",
            f"J'accepte ton invitation, à condition que tu m'obéisses au doigt et à l'œil pendant qu'on y est~",
            f"Compte sur moi pour venir, et tu me porteras mon sac sans un mot, n'est-ce pas ?~",
            f"Oh oui, emmène-moi... mais prépare-toi à ce que ce soit moi qui décide de tout une fois sur place~",
            f"Je viens, mais ne compte pas traîner n'importe où, tu restes sagement à côté de moi~"
        ]
    # 2. Jeux vidéo, vocal, vocaux, parties
    elif any(w in lower_text for w in ["jeu", "jouer", "game", "vocal", "voc", "partie", "rejoignez", "pv", "vocal?", "lancer", "lol", "val,"]):
        phrases = [
            f"Je viens sur le jeu, mais tu vas me carry en silence et sans rager si tu ne veux pas d'ennuis~",
            f"Je lance la game avec toi, mais tu seras mon petit support personnel toute la partie, hihi~",
            f"Viens en voc tout de suite, j'ai envie d'entendre ta petite voix trembler un peu pour moi~",
            f"Je veux bien qu'on joue ensemble, à condition que tu m'offres tes meilleurs loot, mon toutou~",
            f"Tu veux qu'on fasse une session ? Seulement si tu acceptes de te faire dominer du début à la fin~",
            f"Je pointe le bout de mon nez sur le jeu, mais c'est toi qui m'exécutes tous mes objectifs~"
        ]
    # 3. Clashs, insultes, provocations
    elif any(w in lower_text for w in ["ferme", "gueule", "tais", "ftg", "nul", "pire", "déteste", "pense", "fermes", "con", "idiot"]):
        phrases = [
            f"Mh, tu l'ouvres bien grand dis donc... Viens répéter ça un peu plus près de mes pieds, qu'on rigole~",
            f"Tu fais le malin derrière ton écran, mais on sait tous très bien qui commande ici, mon petit agneau~",
            f"Ose me redonner un ordre sur ce ton et tu vas passer un très, très mauvais quart d'heure~",
            f"C'est adorable de t'entendre essayer de te rebeller, continue un peu, j'adore quand tu t'enfonces~",
            f"À genoux, c'est tout ce que tu mérites quand tu l'ouvres un peu trop à mon goût~",
            f"Tu parles beaucoup, mais je sais que tu adores ça au fond, avoue~"
        ]
    # 4. Questions générales ou phrases courantes
    elif any(w in lower_text for w in ["pourquoi", "comment", "qui", "quoi", "est", "sait", "quel", "quand", "ou", "où"]):
        phrases = [
            f"Tu poses beaucoup de questions pour quelqu'un qui devrait plutôt m'obéir sagement~",
            f"Tu te demandes plein de trucs, mais la seule chose à retenir c'est que tu m'appartiens, hihi~",
            f"Laisse tomber ces détails et viens plutôt me prouver ta loyauté, mon toutou~",
            f"Tu cherches des réponses ? Demande-moi gentiment à genoux et j'y réfléchirai peut-être~"
        ]
    # 5. Le reste du temps (généralités du quotidien)
    else:
        phrases = [
            f"Hihi, tu dis ça, mais au fond tu penses à moi toute la journée, avoue-le donc~",
            f"C'est tellement mignon quand tu essayes de faire l'intéressant dans le groupe, viens un peu par ici~",
            f"Tu as bien raison de dire ça, maintenant viens t'asseoir sagement et écoute-moi bien~",
            f"Tu restes mon petit jouet préféré dans ce salon, ne l'oublie jamais~",
            f"Arrête un peu de t'agiter pour rien et viens te détendre, tu n'as pas le choix de toute façon~~",
            f"Regarde-moi quand tu écris ça... tu sais très bien que tu m'appartiens déjà un petit peu~",
            f"Encore en train de parler pour ne rien dire ? Viens plutôt me prouver ta soumission~"
        ]
    
    return random.choice(phrases)

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
