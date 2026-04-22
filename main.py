import discord
from discord.ext import tasks
import datetime
import pytz
import os
import threading
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive"

def run_web():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_web, daemon=True).start()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

CHANNEL_ID = 1373853116268548150

@tasks.loop(minutes=1)
async def update_channel_name():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    if channel is None:
        print("❌ チャンネル取得できてない")
        return

    now_jp = datetime.datetime.now(pytz.timezone("Asia/Tokyo"))
    now_mm = datetime.datetime.now(pytz.timezone("Asia/Yangon"))

    new_name = f"🕒jp{now_jp.strftime('%H:%M')}｜mm{now_mm.strftime('%H:%M')}"
    print(f"更新候補: {new_name}")

    try:
        if channel.name != new_name:
            await channel.edit(name=new_name)
            print("🎉 チャンネル名更新")
    except Exception as e:
        print(f"❌ 更新失敗: {e}")

@client.event
async def on_ready():
    print(f"Bot起動: {client.user}")
    update_channel_name.start()

client.run(TOKEN)
