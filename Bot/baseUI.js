// 필요한 클래스 임포트
const { 
    EmbedBuilder, 
    ActionRowBuilder, 
    ButtonBuilder, 
    ButtonStyle 
  } = require('discord.js');
  
  // 임베드 생성 예시
  const waitEmbed = new EmbedBuilder()
    .setColor(0x2F3136)  // 디스코드 Embed 느낌의 진한 회색
    .setTitle("알로항 - 음악채널")
    .setDescription(
      "99.99%의 업타임 보장\n" +
      "봇 재시작 사이에 음악이 끊기지 않으며, 음질과 접적력을 위해 " +
      "매번 많은 시간을 투자해 유지보수합니다.\n\n" +
      "최적의 사용자 편의를 제공하는\n" +
      "유저가 직접 개발한 커스텀의 동작으로 기능을 사용함을\n" +
      "우선으로 집중했습니다.\n\n" +
      "커스텀봇을 사용으로 고품질 서비스를 유지합니다!\n" +
      "커스텀봇만의 뛰어난 명령어와 디테일링 기능을 누릴 수 있습니다.\n\n" +
      "단 돈 3,990원으로 커스봇을 만나보세요!"
    );
  
  // 버튼들(명령어 예시)
  const row = new ActionRowBuilder()
    .addComponents(
      new ButtonBuilder()
        .setCustomId('play')
        .setLabel('재생')
        .setStyle(ButtonStyle.Primary),
      new ButtonBuilder()
        .setCustomId('stop')
        .setLabel('정지')
        .setStyle(ButtonStyle.Danger),
      new ButtonBuilder()
        .setCustomId('skip')
        .setLabel('다음 노래')
        .setStyle(ButtonStyle.Secondary),
      new ButtonBuilder()
        .setCustomId('lyrics')
        .setLabel('가사보기')
        .setStyle(ButtonStyle.Secondary),
      new ButtonBuilder()
        .setCustomId('queue')
        .setLabel('재생목록')
        .setStyle(ButtonStyle.Secondary)
    );
  
  // 메시지 전송 (예: 명령어 처리 시)
  module.exports = {waitEmbed, row};