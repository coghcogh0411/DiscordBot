//주요 클래스 가져오기
const { Client, Events, GatewayIntentBits } = require("discord.js");
const { DisTube, Queue } = require("distube");
const { YouTubePlugin } = require("@distube/youtube");
const ytSearch = require("yt-search");
const { token, channel_id } = require("./config.json");
const { waitEmbed, row } = require("./baseUI");
const { createMusicEmbed, buttons } = require("./reservationUI");

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

const requesterMap = new Map();
var baseMessage = null;

//봇이 준비됐을때 한번만(once) 표시할 메시지
client.once(Events.ClientReady, async (readyClient) => {
  console.log(`Ready! Logged in as ${readyClient.user.tag}`);
  const channel = client.channels.cache.get(channel_id);
  if (!channel) {
    console.log("해당 채널을 찾을 수 없습니다.");
    return;
  }

  // 2) 채널에 메시지 전송하기
  baseMessage = await channel.send({
    embeds: [waitEmbed],
    components: [row],
  });
});

// 메시지가 생성되면
client.on("messageCreate", async (msg) => {
  //노래채널에 입력했을때
  if (msg.channel.id == channel_id && !msg.author.bot) {
    if (!msg.member.voice.channel) {
      return msg.reply("먼저 음성 채널에 접속해주세요!");
    }
    msg.delete();

    //메시지 보낸사람이 음성채널에 들어와있는지 확인
    if (msg.member.voice.channel) {
      //메시지 youtube에 검색해서 url,제목 가져옴
      // Song = await ytSearch(msg.content);
      // var mainSong = {
      //   title: Song.all[0].title,
      //   url: Song.all[0].url,
      //   thumbnail: Song.all[0].thumbnail,
      //   requester: msg.member,
      // };

      // //이상한거 있을수 있으니 여러개 더 가져와서 고를수있게
      // var previewSongs = [];
      // for (let i = 1; i < 6; i++) {
      //   previewSongs.push({
      //     title: Song.all[i].title,
      //     url: Song.all[0].url,
      //     thumbnail: Song.all[i].thumbnail,
      //   });
      // }

      await distube.play(msg.member.voice.channel, msg.content, {
        member: msg.member,
        textChannel: msg.channel,
      });

      const queue = distube.getQueue(msg);
      //autoplay되는거같긴한데 지금 정보가 제대로 안 넘어오는 듯 제목까지는 가져옴 101줄부터 문제
      queue.toggleAutoplay();
      const guildId = msg.guild.id;
      if (!requesterMap.has(guildId)) {
        requesterMap.set(guildId, new Map());
      }
      const guildMap = requesterMap.get(guildId);
      const addedSong = queue.songs[queue.songs.length - 1];
      guildMap.set(addedSong.id, msg.member);
      console.log(guildMap);
    } 
  }
});

//노래 재생 될 때
distube.on("playSong", (queue, song) => {
  setTimeout(() => {
    const songTitle = song.name;
    const albumImage = song.thumbnail;
    // 현재 서버의 guild id를 구합니다.
    const guildId = queue.textChannel.guild.id;
    console.log(`guildID:${guildId}`);
    //여기부터 제대로된 정보가 안들어옴
    const guildMap = requesterMap.get(guildId);
    console.log(`guildMap:`);
    console.log(guildMap);
    const requester = guildMap.get(song.id);

    console.log(`Now playing: ${songTitle}`);
    //   console.log(requester.globalName);
    //   console.log(requester.avartarURL);
    console.log(requester);
    if (requester) {
      // baseMessage에 재생중인 노래 정보를 담은 embed 업데이트
      baseMessage.edit({
        embeds: [createMusicEmbed(songTitle, requester, albumImage)],
        components: [buttons],
      });
      guildMap.delete(song.id);
    } else {
      console.log("Requester 정보가 없습니다.");
      const requester = client;
      console.log(requester);
      baseMessage.edit({
        embeds: [
          createMusicEmbed(
            songTitle,
            requester,
            albumImage
          ),
        ],
        components: [buttons],
      });
    }
  }, 1000);
});

//버튼 클릭하면 버튼기능 실행
client.on("interactionCreate", async (interaction) =>{
  //버튼을 누른게아니면 동작안함
  if(!interaction.isButton()){
    return;
  }
  switch(interaction.customId){
    case "play":
      await distube.resume(interaction.guildId);
      break;
    case "stop":
      await distube.stop(interaction.guildId);
      baseMessage.edit({
        embeds: [waitEmbed],
        components: [row],
      });
      break;
    case "skip":
      await distube.skip(interaction.guildId);
      break;
    case "pause":
      await distube.pause(interaction.guildId);
      break;
    default:
      await distube.stop(interaction.guildId);
      baseMessage.edit({
        embeds: [waitEmbed],
        components: [row],
      });
      break;
  } 
  //interaction에는 channelID(버튼누른 채널 id), guildID(버튼누른 서버 ID), user객체, member객체가 있음
  // 가져와야 할 것
  // 1. guildID 어느서버의 봇을 컨트롤 할 지 정해야하므로 필요함
  // channelID, user객체, member객체는 필요한가?
  // 예를 들면 멈춤버튼을 누르면 guildID가져와서 그서버에 gupa봇 distube.stop하면 되는거아닌가?
  // interaction에 너무 많은 정보가 담겨있는데 사용자가 많아지면 부담이 커지지않나?
  // guildID만 가져오는 식으로하면 부담이 줄어드나? 
  // ex)interaction.guildID
  // 근데 이렇게하면 보여주는건 guildID만 보여주긴 하겠지만 결국 interaction전부 가져오는건 똑같지 않나?


})

//노래가끝나면 다시 기본메시지로
distube.on("finish", (queue) => {
  console.log(queue);
});

distube.on("disconnect", (queue) => {
  baseMessage.edit({
    embeds: [waitEmbed],
    components: [row],
  });
});
// 5. 시크릿키(토큰)을 통해 봇 로그인 실행
client.login(token);
