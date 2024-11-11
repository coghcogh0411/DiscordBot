import discord
from discord.ext import commands
f = open('token.txt', 'r')

token = f.readline().strip()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_message(msg):
    target_channel_id = 1305496311184883813  # 예시 ID입니다. 실제 채널 ID로 변경하세요
    
    if msg.channel.id == target_channel_id:
        print(f"{msg.author}: {msg.content}")  # 메시지 내용 출력
    
    await bot.process_commands(msg)

bot.run(token)