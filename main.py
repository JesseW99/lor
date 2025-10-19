import discord
from discord.ext import commands
import os
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =================== CONFIG ===================
SOURCE_CHANNEL_ID = 1425133174702211104
TARGET_CHANNEL_ID = 1407438967481172058
BACKUP_FOLDER = "backup_files"
# ==============================================

os.makedirs(BACKUP_FOLDER, exist_ok=True)

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.channel.id == SOURCE_CHANNEL_ID:
        target_channel = bot.get_channel(TARGET_CHANNEL_ID)
        if target_channel:
            files = []
            for a in message.attachments:
                backup_path = os.path.join(BACKUP_FOLDER, f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{a.filename}")
                await a.save(backup_path)
                files.append(discord.File(backup_path))
            try:
                await target_channel.send(content=message.content or "", files=files if files else None)
                print(f"[{datetime.now()}] Message forwarded successfully")
            except Exception as e:
                print(f"[{datetime.now()}] Failed to forward message: {e}")

bot.run(os.getenv("TOKEN"))
