// reservationUI.js
const {
  EmbedBuilder,
  ActionRowBuilder,
  ButtonBuilder,
  ButtonStyle,
} = require("discord.js");

function createMusicEmbed(
  songTitle,
  requester,
  albumImage
) {
  return new EmbedBuilder()
    .setColor(0x2f3136)
    .setTitle("음악 재생 중")
    .setDescription(
      `**${songTitle}**\n\n`
    )
    .setThumbnail(requester.user.displayAvatarURL())
    .setImage(albumImage)
    .setFooter({
      text: `신청자: ${requester.user.globalName}`,
      iconURL: requester.user.displayAvatarURL(),
    })
    .setTimestamp();
}

const buttons = new ActionRowBuilder().addComponents(
  new ButtonBuilder()
    .setCustomId("stop")
    .setLabel("정지")
    .setStyle(ButtonStyle.Danger),
  new ButtonBuilder()
    .setCustomId("skip")
    .setLabel("스킵")
    .setStyle(ButtonStyle.Primary),
  new ButtonBuilder()
    .setCustomId("pause")
    .setLabel("일시정지")
    .setStyle(ButtonStyle.Secondary),
  new ButtonBuilder()
    .setCustomId("queue")
    .setLabel("대기열")
    .setStyle(ButtonStyle.Primary)
);

module.exports = { createMusicEmbed, buttons };
