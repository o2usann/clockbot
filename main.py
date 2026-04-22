import discord
from discord.ext import tasks
import datetime
import pytz
import os

TOKEN = os.environ["TOKEN"]

intents = discord.Intents.default()
client = discord.Client(intents=intents)

CHANNEL_ID = 1496308886435532945

@tasks.loop(minutes=1)
async def update_channel_name():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    now_jp = datetime.datetime.now(pytz.timezone("Asia/Tokyo"))
    now_mm = datetime.datetime.now(pytz.timezone("Asia/Yangon"))

    # 5分刻みに丸める
    jp_min = (now_jp.minute // 5) * 5
    mm_min = (now_mm.minute // 5) * 5

    new_name = f"🕒jp{now.strftime('%H:%M')}｜mm{now.strftime('%M:%S')}"

    if channel.name != new_name:
        await channel.edit(name=new_name)

@client.event
async def on_ready():
    print("Bot起動！")
    update_channel_name.start()

client.run(TOKEN)
