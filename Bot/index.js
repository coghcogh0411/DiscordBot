//주요 클래스 가져오기
const { Client, Events, GatewayIntentBits } = require("discord.js");
const { DisTube } = require("distube");
const { YouTubePlugin } = require("@distube/youtube");
const ytSearch = require("yt-search");
const { token, channel_id } = require("./config.json");
const { waitEmbed, row } = require("./index2");

//클라이언트 객체 생성 (Guilds관련, 메시지관련 인텐트 추가)
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
    GatewayIntentBits.GuildVoiceStates,
  ],
});

const distube = new DisTube(client, {
  plugins: [new YouTubePlugin()],
});

//봇이 준비됐을때 한번만(once) 표시할 메시지
client.once(Events.ClientReady, async (readyClient) => {
  console.log(`Ready! Logged in as ${readyClient.user.tag}`);
  const channel = client.channels.cache.get(channel_id);
  if (!channel) {
    console.log("해당 채널을 찾을 수 없습니다.");
    return;
  }

  // 2) 채널에 메시지 전송하기
  const baseMessage = await channel.send({
    embeds: [waitEmbed],
    components: [row],
  });
});

distube.on("finishSong", (queue) => {
  baseMessage.edit({
    embeds: [waitEmbed],
    components: [row],
  });
});

// 메시지가 생성되면
client.on("messageCreate", async (msg) => {
  //노래채널에 입력했을때
  if (msg.channel.id == channel_id) {
    msg.delete();
    if (!msg.member.voice.channel) {
      return msg.reply("먼저 음성 채널에 접속해주세요!");
    }

    //메시지 보낸사람이 음성채널에 들어와있는지 확인
    if (msg.member.voice.channel) {
      //메시지 youtube에 검색해서 url,제목 가져옴
      Song = await ytSearch(msg.content);
      var mainSong = {
        title: Song.all[0].title,
        url: Song.all[0].url,
        thumbnail: Song.all[0].thumbnail,
      };

      //이상한거 있을수 있으니 여러개 더 가져와서 고를수있게
      var previewSongs = [];
      for (let i = 1; i < 6; i++) {
        previewSongs.push({
          title: Song.all[i].title,
          url: Song.all[0].url,
          thumbnail: Song.all[i].thumbnail,
        });
      }

      distube.play(msg.member.voice.channel, mainSong.url, {
        textChannel: msg.channel,
        member: msg.member,
      });

      console.log(mainSong);
      console.log(previewSongs);
    }
  }
});

// 5. 시크릿키(토큰)을 통해 봇 로그인 실행
client.login(token);
