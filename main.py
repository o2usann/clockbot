import discord
from discord.ext import tasks
import datetime
import pytz
import os

# --- Render用 ---
import threading
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive"

def run_web():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_web).start()

# --- Discord設定 ---
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

CHANNEL_ID = 1496330709541978112

# --- 時間更新 ---
@tasks.loop(minutes=1)
async def update_channel_name():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    if channel is None:
        print("❌ チャンネル取得できてない")
        return

    now_jp = datetime.datetime.now(pytz.timezone("Asia/Tokyo"))
    now_mm = datetime.datetime.now(pytz.timezone("Asia/Yangon"))

    # 半角コロンに修正
    new_name = f"🕒jp{now_jp.strftime('%H:%M')}｜mm{now_mm.strftime('%M:%S')}"

    print(f"✅ 更新候補: {new_name}")

    if channel.name != new_name:
        await channel.edit(name=new_name)
        print("🎉 チャンネル名更新！")

@client.event
async def on_ready():
    print("Bot起動！")
    update_channel_name.start()

client.run(TOKEN)
