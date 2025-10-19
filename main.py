import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =================== CONFIG ===================
SOURCE_CHANNEL_ID = 1425133174702211104
TARGET_CHANNEL_ID = 1407438967481172058
# ==============================================

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
            files = [await a.to_file() for a in message.attachments]
            try:
                await target_channel.send(content=message.content or "", files=files if files else None)
                print(f"Message forwarded successfully")
            except Exception as e:
                print(f"Failed to forward message: {e}")

# Run the bot
token = os.getenv("TOKEN")
if not token:
    raise ValueError("Discord token not found! Please set TOKEN in your .env file.")
bot.run(token)
