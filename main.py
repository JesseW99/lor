import discord
from discord.ext import commands
import os

# =================== CONFIG ===================
SOURCE_CHANNEL_ID = 1425133174702211104
TARGET_CHANNEL_ID = 1407438967481172058
# ==============================================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

@bot.event
async def on_message(message):
    # Ignore messages from itself
    if message.author == bot.user:
        return

    # Forward messages only from the source channel
    if message.channel.id == SOURCE_CHANNEL_ID:
        target_channel = bot.get_channel(TARGET_CHANNEL_ID)
        if target_channel:
            files = [await attachment.to_file() for attachment in message.attachments]
            try:
                await target_channel.send(
                    content=message.content if message.content else "",
                    files=files if files else None
                )
                print("Message forwarded successfully")
            except Exception as e:
                print(f"Failed to forward message: {e}")

# Make sure you have your bot token in environment variable TOKEN
bot.run(os.getenv("TOKEN"))
