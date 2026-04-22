import discord
from discord.ext import tasks
import datetime
import pytz
import os
import threading
from flask import Flask

# --- Render用 ---
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive"

def run_web():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_web, daemon=True).start()

# --- Discord設定 ---
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1373853116268548150

intents = discord.Intents.default()
client = discord.Client(intents=intents)

# --- 10分刻みに丸める関数 ---
def floor_to_10(dt):
    minute = (dt.minute // 10) * 10
    return dt.replace(minute=minute, second=0, microsecond=0)

# --- 時間更新（10分ごと） ---
@tasks.loop(minutes=10)
async def update_channel_name():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    if channel is None:
        print("❌ チャンネル取得失敗")
        return

    # 時間取得 → 10分刻みに丸め
    now_jp = floor_to_10(datetime.datetime.now(pytz.timezone("Asia/Tokyo")))
    now_mm = floor_to_10(datetime.datetime.now(pytz.timezone("Asia/Yangon")))

    # 表示フォーマット
    new_name = f"🕒jp{now_jp.strftime('%H：%M')}｜mm{now_mm.strftime('%H：%M')}"
    print(f"更新候補: {new_name}")

    # 同じならスキップ（超重要）
    if channel.name == new_name:
        print("ℹ️ 同じなのでスキップ")
        return

    try:
        await channel.edit(name=new_name)
        print("✅ チャンネル名更新成功")
    except Exception as e:
        print(f"❌ 更新失敗: {e}")

# --- 起動時 ---
@update_channel_name.before_loop
async def before_update():
    await client.wait_until_ready()

@client.event
async def on_ready():
    print(f"Bot起動: {client.user}")
    update_channel_name.start()

client.run(TOKEN)
