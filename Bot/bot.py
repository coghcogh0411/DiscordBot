import discord
from discord.ext import commands
import yt_dlp as youtube_dl
from discord.ui import Button, View
import asyncio
import sys
import signal

f = open("token.txt", "r")
token = f.readline().strip()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# 서버별 재생 대기열을 저장할 딕셔너리
song_queue = {}

# 전역 변수로 현재 재생 중인 노래 정보 저장
current_song = {}

ydl_opts = {"format": "bestaudio/best", "quiet": True}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}

# 전역 변수로 봇의 상태 메시지를 저장
bot_message = None


async def update_bot_message(channel, content, view=None):
    global bot_message
    try:
        if bot_message:
            await bot_message.edit(content=content, view=view)
        else:
            bot_message = await channel.send(content, view=view)
    except:
        bot_message = await channel.send(content, view=view)


class MusicControlView(discord.ui.View):
    def __init__(self, bot, guild):
        super().__init__(timeout=None)
        self.bot = bot
        self.guild = guild

    @discord.ui.button(label="⏭️ 스킵", style=discord.ButtonStyle.primary)
    async def skip_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        voice_client = self.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await interaction.response.send_message("⏭️ 다음 곡으로 넘어갑니다!")
        else:
            await interaction.response.send_message(
                "❌  현재 재생 중인 곡이 없습니다!", ephemeral=True
            )

    @discord.ui.button(label="⏹️ 정지", style=discord.ButtonStyle.danger)
    async def stop_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        voice_client = self.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            song_queue[self.guild.id].clear()
            await interaction.response.send_message(
                "⏹️ 재생을 멈추고 대기열을 비웠습니다!"
            )
        else:
            await interaction.response.send_message(
                "❌  현재 생 중인 곡이 없습니다!", ephemeral=True
            )


async def play_next(guild, channel):
    if len(song_queue[guild.id]) > 0:
        next_source = song_queue[guild.id].pop(0)
        current_song[guild.id] = next_source["title"]
        guild.voice_client.play(
            next_source["audio"],
            after=lambda e: bot.loop.create_task(play_next(guild, channel)),
        )
        view = MusicControlView(bot, guild)
        content = f"🎵  현재 재생 중인 노래\n{next_source['title']}"
        await update_bot_message(channel, content, view)
    else:
        current_song[guild.id] = None
        content = "재생 목록이 비었습니다."
        await update_bot_message(channel, content)


async def update_bot_message(channel, content, view=None):
    global bot_message
    try:
        if bot_message:
            await bot_message.edit(content=content, view=view)
        else:
            bot_message = await channel.send(content, view=view)
    except:
        bot_message = await channel.send(content, view=view)


class MusicControlView(discord.ui.View):
    def __init__(self, bot, guild):
        super().__init__(timeout=None)
        self.bot = bot
        self.guild = guild

    @discord.ui.button(label="⏭️ 스킵", style=discord.ButtonStyle.primary)
    async def skip_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        voice_client = self.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await interaction.response.send_message("⏭️ 다음 곡으로 넘어갑니다!")
        else:
            await interaction.response.send_message(
                "❌  현재 재생 중인 곡이 없습니다!", ephemeral=True
            )

    @discord.ui.button(label="⏹️ 정지", style=discord.ButtonStyle.danger)
    async def stop_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        voice_client = self.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            song_queue[self.guild.id].clear()
            await interaction.response.send_message(
                "⏹️ 재생을 멈추고 대기열을 비웠습니다!"
            )
        else:
            await interaction.response.send_message(
                "❌  현재 생 중인 곡이 없습니다!", ephemeral=True
            )


async def play_next(guild, channel):
    if len(song_queue[guild.id]) > 0:
        next_source = song_queue[guild.id].pop(0)
        current_song[guild.id] = next_source["title"]
        guild.voice_client.play(
            next_source["audio"],
            after=lambda e: bot.loop.create_task(play_next(guild, channel)),
        )
        view = MusicControlView(bot, guild)
        content = f"🎵  현재 재생 중인 노래\n{next_source['title']}"
        await update_bot_message(channel, content, view)
    else:
        current_song[guild.id] = None
        content = "재생 목록이 비었습니다."
        await update_bot_message(channel, content)

# 서버별 재생 대기열을 저장할 딕셔너리
song_queue = {}

# 전역 변수로 현재 재생 중인 노래 정보 저장
current_song = {}

ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

# 전역 변수로 봇의 상태 메시지를 저장
bot_message = None
async def update_bot_message(channel, content, view=None):
    global bot_message
    try:
        if bot_message:
            await bot_message.edit(content=content, view=view)
        else:
            bot_message = await channel.send(content, view=view)
    except:
        bot_message = await channel.send(content, view=view)
class MusicControlView(discord.ui.View):
    def __init__(self, bot, guild):
        super().__init__(timeout=None)
        self.bot = bot
        self.guild = guild

    @discord.ui.button(label="⏭️ 스킵", style=discord.ButtonStyle.primary)
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        voice_client = self.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await interaction.response.send_message("⏭️ 다음 곡으로 넘어갑니다!")
        else:
            await interaction.response.send_message("❌  현재 재생 중인 곡이 없습니다!", ephemeral=True)

    @discord.ui.button(label="⏹️ 정지", style=discord.ButtonStyle.danger)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        voice_client = self.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            song_queue[self.guild.id].clear()
            await interaction.response.send_message("⏹️ 재생을 멈추고 대기열을 비웠습니다!")
        else:
            await interaction.response.send_message("❌  현재 생 중인 곡이 없습니다!", ephemeral=True)
async def play_next(guild, channel):
    if len(song_queue[guild.id]) > 0:
        next_source = song_queue[guild.id].pop(0)
        current_song[guild.id] = next_source['title']
        guild.voice_client.play(next_source['audio'],
                              after=lambda e: bot.loop.create_task(play_next(guild, channel)))
        view = MusicControlView(bot, guild)
        content = f"🎵  현재 재생 중인 노래\n{next_source['title']}"
        await update_bot_message(channel, content, view)
    else:
        current_song[guild.id] = None
        content = "재생 목록이 비었습니다."
        await update_bot_message(channel, content)
@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return

    target_channel_id = 1306289397041201183

    if msg.channel.id == target_channel_id and not msg.content.startswith("!"):
        print(f"{msg.author}: {msg.content}")

        if msg.author.voice:
            await msg.delete()

            if msg.guild.id not in song_queue:
                song_queue[msg.guild.id] = []
            if msg.guild.id not in current_song:
                current_song[msg.guild.id] = None

            voice_channel = msg.author.voice.channel
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(f"ytsearch:{msg.content}", download=False)[
                        "entries"
                    ][0]
                    url = info["url"]
                    title = info["title"]
                    audio = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)

                    if not msg.guild.voice_client:
                        voice_client = await voice_channel.connect()
                    else:
                        voice_client = msg.guild.voice_client

                    if voice_client.is_playing():
                        song_queue[msg.guild.id].append(
                            {"audio": audio, "title": title}
                        )
                        content = f"🎵  현재 재생 중인 노래\n{current_song[msg.guild.id]}\n\n📋  대기열에 추가됨\n{title}"
                        await update_bot_message(msg.channel, content)

                        await asyncio.sleep(3)
                        view = MusicControlView(bot, msg.guild)
                        content = (
                            f"🎵  현재 재생 중인 노래\n{current_song[msg.guild.id]}"
                        )
                        await update_bot_message(msg.channel, content, view)
                    else:
                        current_song[msg.guild.id] = title
                        voice_client.play(
                            audio,
                            after=lambda e: bot.loop.create_task(
                                play_next(msg.guild, msg.channel)
                            ),
                        )
                        view = MusicControlView(bot, msg.guild)
                        content = f"🎵  현재 재생 중인 노래\n{title}"
                        await update_bot_message(msg.channel, content, view)

            except Exception as e:
                await update_bot_message(
                    msg.channel, f"❌  오류가 발생했습니다: {str(e)}"
                )
        else:
            await msg.delete()
            await update_bot_message(msg.channel, "⚠️ 음성 채널에 먼저 입장해주세요!")

    await bot.process_commands(msg)


@bot.command()
async def showqueue(ctx):
    if ctx.guild.id not in song_queue or len(song_queue[ctx.guild.id]) == 0:
        queue_text = "재생목록이 비어있습니다!"
    else:
        queue_text = "📋  재생목록:\n" + "\n".join(
            [
                f"{i}. {song['title']}"
                for i, song in enumerate(song_queue[ctx.guild.id], 1)
            ]
        )

    if current_song[ctx.guild.id]:
        current_text = f"🎵  현재 재생 중인 노래\n{current_song[ctx.guild.id]}"
    else:
        current_text = "재생 중인 노래가 없습니다."

    await update_bot_message(ctx.channel, f"{current_text}\n\n{queue_text}")


@bot.event
async def on_ready():
    target_channel = bot.get_channel(1306289397041201183)
    if target_channel:
        async for message in target_channel.history(limit=None):
            await message.delete()
    print(f"{bot.user} 로 로그인했습니다!")


async def cleanup():
    print("채널 정리를 시작합니다...")
    target_channel = bot.get_channel(1306289397041201183)
    if target_channel:
        try:
            # 채널의 모든 메시지를 한 번에 삭제
            await target_channel.purge(limit=None)
        except Exception as e:
            print(f"채널 정리 중 오류 발생: {e}")
    print("채널 정리가 완료되었습니다.")

# 시그널 핸들러 추가
def signal_handler(sig, frame):
    print("종료 신호를 받았습니다...")
    asyncio.run(cleanup())
    sys.exit(0)

# 시그널 핸들러 등록
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

try:
    bot.run(token)
except KeyboardInterrupt:
    print("봇을 종료합니다...")
    asyncio.run(cleanup())
except Exception as e:
    print(f"오류 발생: {e}")
    asyncio.run(cleanup())
finally:
    sys.exit(0)
