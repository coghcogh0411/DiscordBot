import discord
from discord.ext import commands
import yt_dlp as youtube_dl

f = open('token.txt', 'r')
token = f.readline().strip()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# 서버별 재생 대기열을 저장할 딕셔너리
song_queue = {}

ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

async def play_next(guild, channel):
    if len(song_queue[guild.id]) > 0:
        next_source = song_queue[guild.id].pop(0)
        guild.voice_client.play(next_source['audio'], 
                              after=lambda e: bot.loop.create_task(play_next(guild, channel)))
        await channel.send(f"🎵 지금 재생 중: {next_source['title']}")

@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return
        
    target_channel_id = 1305621030072619068
    
    if msg.channel.id == target_channel_id:
        print(f"{msg.author}: {msg.content}")
        
        if msg.author.voice:
            if msg.guild.id not in song_queue:
                song_queue[msg.guild.id] = []
                
            voice_channel = msg.author.voice.channel
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(f"ytsearch:{msg.content}", download=False)['entries'][0]
                    url = info['url']
                    
                    # FFmpegPCMAudio 사용
                    audio = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
                    
                    if not msg.guild.voice_client:
                        voice_client = await voice_channel.connect()
                    else:
                        voice_client = msg.guild.voice_client
                    
                    if voice_client.is_playing():
                        # 노래가 재생 중이면 대기열에 추가
                        song_queue[msg.guild.id].append({
                            'audio': audio,
                            'title': info['title']
                        })
                        await msg.channel.send(f"🎵 재생목록에 추가됨: {info['title']}")
                    else:
                        # 재생 중이 아니면 바로 재생
                        voice_client.play(audio, after=lambda e: bot.loop.create_task(play_next(msg.guild, msg.channel)))
                        await msg.channel.send(f"🎵 지금 재생 중: {info['title']}")
                        
            except Exception as e:
                await msg.channel.send(f"오류가 발생했습니다: {str(e)}")
        else:
            await msg.channel.send("음성 채널에 먼저 입장해주세요!")
    
    await bot.process_commands(msg)

@bot.command()
async def showqueue(ctx):
    if ctx.guild.id not in song_queue or len(song_queue[ctx.guild.id]) == 0:
        await ctx.send("재생목록이 비어있습니다!")
        return
        
    queue_list = "🎵 재생목록:\n"
    for i, song in enumerate(song_queue[ctx.guild.id], 1):
        queue_list += f"{i}. {song['title']}\n"
    
    await ctx.send(queue_list)

bot.run(token)