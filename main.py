from riotwatcher import LolWatcher
import json
import discord


with open('champion.json', encoding="utf8") as file:
    data = json.load(file)

api_key = 'api_key'
watcher = LolWatcher(api_key)
region = 'na1'
all_champion_data = data['data']
token = 'token'
client = discord.Client()


def get_account_information(summoner_name: str) -> dict:
    return watcher.summoner.by_name(region, summoner_name)


def get_summoner_level(summoner_name: str) -> int:
    return get_account_information(summoner_name)['summonerLevel']


def get_encrypted_id(summoner_name: str) -> str:
    return get_account_information(summoner_name)['id']


def get_account_id(summoner_name: str) -> str:
    return get_account_information(summoner_name)['accountId']


def get_champion_mastery_information(summoner_name: str, champion: str):
    champ_data = all_champion_data[champion]
    champ_id = int(champ_data['key'])
    encrypted_id = get_encrypted_id(summoner_name)

    return watcher.champion_mastery.by_summoner_by_champion(
        region, encrypted_id, champ_id)


def get_champion_mastery_level(summoner_name: str, champion: str):
    champ_mastery_info = get_champion_mastery_information(
        summoner_name, champion)
    return champ_mastery_info['championLevel']


def get_champion_mastery_points(summoner_name: str, champion: str):
    champ_mastery_info = get_champion_mastery_information(
        summoner_name, champion)
    return champ_mastery_info['championPoints']


def get_champ_level_points(summoner_name: str, champion: str):
    return 'Mastery ' + str(get_champion_mastery_level(summoner_name, champion)) + ' with ' + \
           str(get_champion_mastery_points(summoner_name, champion)) + ' points'


def chest_received(summoner_name: str, champion: str):
    info = get_champion_mastery_information(summoner_name, champion)

    return info['chestGranted']


def all_masteries_info(summoner_name: str):
    return watcher.champion_mastery.by_summoner(
        region, get_encrypted_id(summoner_name))


def total_mastery_score(summoner_name: str):
    return watcher.champion_mastery.scores_by_summoner(
        region, get_encrypted_id(summoner_name))


def rank_info(summoner_name: str):
    return watcher.league.by_summoner(region, get_encrypted_id(summoner_name))


def rank_display_solo(summoner_name: str):
    rank_list = rank_info(summoner_name)

    for ranking in rank_list:
        if ranking['queueType'] == 'RANKED_SOLO_5x5':
            return ranking['tier'] + ' ' + ranking['rank'] + ' ' + str(
                ranking['leaguePoints']) + ' LP'

    return 'N/A'


def rank_solo_winrate(summoner_name: str):
    rank_list = rank_info(summoner_name)

    for ranking in rank_list:
        if ranking['queueType'] == 'RANKED_SOLO_5x5':
            return '{0:.2f}'.format(
                (ranking['wins'] /
                 (ranking['wins'] + ranking['losses'])) * 100) + '%'
    return 'N/A'


def rank_icons(rank: str):
    if 'IRON' in rank:
        return 'https://static.wikia.nocookie.net/leagueoflegends/images/f/fe/Season_2022_-_' \
               'Iron.png/revision/latest/scale-to-width-down/130?cb=20220105213520'
    elif 'BRONZE' in rank:
        return 'https://static.wikia.nocookie.net/leagueoflegends/images/e/e9/Season_2022_-_' \
               'Bronze.png/revision/latest/scale-to-width-down/130?cb=20220105214224'
    elif 'SILVER' in rank:
        return 'https://static.wikia.nocookie.net/leagueoflegends/images/4/44/Season_2022_-_' \
               'Silver.png/revision/latest/scale-to-width-down/130?cb=20220105214225'
    elif 'GOLD' in rank:
        return 'https://static.wikia.nocookie.net/leagueoflegends/images/8/8d/Season_2022_-_' \
               'Gold.png/revision/latest/scale-to-width-down/130?cb=20220105214225'
    elif 'PLATINUM' in rank:
        return 'https://static.wikia.nocookie.net/leagueoflegends/images/3/3b/Season_2022_-_' \
               'Platinum.png/revision/latest/scale-to-width-down/130?cb=20220105214225'
    elif 'DIAMOND' in rank:
        return 'https://static.wikia.nocookie.net/leagueoflegends/images/e/ee/Season_2022_-_' \
               'Diamond.png/revision/latest/scale-to-width-down/130?cb=20220105214226'
    elif 'GRANDMASTER' in rank:
        return 'https://static.wikia.nocookie.net/leagueoflegends/images/f/fc/Season_2022_-_' \
            'Grandmaster.png/revision/latest/scale-to-width-down/130?cb=20220105214312'
    elif 'MASTER' in rank:
        return 'https://static.wikia.nocookie.net/leagueoflegends/images/e/eb/Season_2022_-_' \
               'Master.png/revision/latest/scale-to-width-down/130?cb=20220105214311'
    elif 'CHALLENGER' in rank:
        return 'https://static.wikia.nocookie.net/leagueoflegends/images/0/02/Season_2022_-_' \
               'Challenger.png/revision/latest/scale-to-width-down/130?cb=20220105214312'
    else:
        return 'https://www.unrankedsmurfs.com/storage/blogposts/lol-ranks-explained/unranked.png'


def mastery_image(level: int):
    if level == 1:
        return 'https://static.wikia.nocookie.net/leagueoflegends/images/d/d8/Champion_Mastery_Level_1_Flair.png' \
               '/revision/latest/scale-to-width-down/120?cb=20150312005229 '
    elif level == 2:
        return 'https://static.wikia.nocookie.net/leagueoflegends/images/4/4d/Champion_Mastery_Level_2_Flair.png' \
               '/revision/latest/scale-to-width-down/120?cb=20150312005244 '
    elif level == 3:
        return 'https://static.wikia.nocookie.net/leagueoflegends/images/e/e5/Champion_Mastery_Level_3_Flair.png' \
               '/revision/latest/scale-to-width-down/120?cb=20150312005319 '
    elif level == 4:
        return 'https://static.wikia.nocookie.net/leagueoflegends/images/b/b6/Champion_Mastery_Level_4_Flair.png' \
               '/revision/latest/scale-to-width-down/120?cb=20200113041829 '
    elif level == 5:
        return 'https://static.wikia.nocookie.net/leagueoflegends/images/9/96/Champion_Mastery_Level_5_Flair.png' \
               '/revision/latest/scale-to-width-down/120?cb=20200113041512 '
    elif level == 6:
        return 'https://static.wikia.nocookie.net/leagueoflegends/images/b/be/Champion_Mastery_Level_6_Flair.png' \
               '/revision/latest/scale-to-width-down/120?cb=20200113041636 '
    elif level == 7:
        return 'https://static.wikia.nocookie.net/leagueoflegends/images/7/7a/Champion_Mastery_Level_7_Flair.png' \
               '/revision/latest/scale-to-width-down/120?cb=20200113041615 '


def level_image(level: int):
    if level < 40:
        return 'https://sticker-collection.com/stickers/plain/League3motes/512/feeb151a-83e8-4c9b-a065' \
               '-cae7d2a43adefile_350323.webp '
    elif 40 <= level < 50:
        return 'https://vignette.wikia.nocookie.net/leagueoflegends/images/e/ec/Level_40_Prestige_Emote.png/revision' \
               '/latest?cb=20171121000702 '
    elif 50 <= level < 75:
        return 'https://vignette.wikia.nocookie.net/leagueoflegends/images/a/a4/Level_50_Prestige_Emote.png/revision' \
               '/latest?cb=20171121000027 '
    elif 75 <= level < 100:
        return 'https://vignette.wikia.nocookie.net/leagueoflegends/images/2/2f/Level_75_Prestige_Emote.png/revision' \
               '/latest?cb=20171121000405 '
    elif 100 <= level < 125:
        return 'https://vignette.wikia.nocookie.net/leagueoflegends/images/2/2a/Level_100_Prestige_Emote.png/revision' \
               '/latest?cb=20171120235253 '
    elif 125 <= level < 150:
        return 'https://vignette.wikia.nocookie.net/leagueoflegends/images/d/d4/Level_125_Prestige_Emote.png/revision' \
               '/latest?cb=20171120234718 '
    elif 150 <= level < 175:
        return 'https://vignette.wikia.nocookie.net/leagueoflegends/images/f/f3/Level_150_Prestige_Emote.png/revision' \
               '/latest?cb=20171120235812 '
    elif 175 <= level < 200:
        return 'https://vignette.wikia.nocookie.net/leagueoflegends/images/a/ab/Level_175_Prestige_Emote.png/revision' \
               '/latest?cb=20171120234752 '
    elif 200 <= level < 225:
        return 'https://vignette.wikia.nocookie.net/leagueoflegends/images/a/a2/Level_200_Prestige_Emote.png/revision' \
               '/latest?cb=20180224184205 '
    elif 225 <= level < 250:
        return 'https://vignette.wikia.nocookie.net/leagueoflegends/images/4/4c/Level_225_Prestige_Emote.png/revision' \
               '/latest?cb=20180224183824 '
    elif 250 <= level < 275:
        return 'https://vignette.wikia.nocookie.net/leagueoflegends/images/3/3f/Level_250_Prestige_Emote.png/revision' \
               '/latest?cb=20180224191059 '
    elif 275 <= level < 300:
        return 'https://vignette.wikia.nocookie.net/leagueoflegends/images/f/fc/Level_275_Prestige_Emote.png/revision' \
               '/latest?cb=20180224190658 '
    elif 300 <= level < 325:
        return 'https://vignette.wikia.nocookie.net/leagueoflegends/images/9/9b/Level_300_Prestige_Emote.png/revision' \
               '/latest?cb=20180224192733 '
    elif 325 <= level < 350:
        return 'https://vignette.wikia.nocookie.net/leagueoflegends/images/8/82/Level_325_Prestige_Emote.png/revision' \
               '/latest?cb=20180224192829 '
    elif 350 <= level < 375:
        return 'https://vignette.wikia.nocookie.net/leagueoflegends/images/7/74/Level_350_Prestige_Emote.png/revision' \
               '/latest?cb=20180224192324 '
    elif 375 <= level < 400:
        return 'https://vignette.wikia.nocookie.net/leagueoflegends/images/1/1b/Level_375_Prestige_Emote.png/revision' \
               '/latest?cb=20180224192856 '
    elif 400 <= level < 425:
        return 'https://vignette.wikia.nocookie.net/leagueoflegends/images/0/05/Level_400_Prestige_Emote.png/revision' \
               '/latest?cb=20180509205006 '
    elif 425 <= level < 450:
        return 'https://vignette.wikia.nocookie.net/leagueoflegends/images/f/f0/Level_425_Prestige_Emote.png/revision' \
               '/latest?cb=20180509205155 '
    elif 450 <= level < 475:
        return 'https://vignette.wikia.nocookie.net/leagueoflegends/images/8/85/Level_450_Prestige_Emote.png/revision' \
               '/latest?cb=20180509205220 '
    elif 475 <= level < 500:
        return 'https://vignette.wikia.nocookie.net/leagueoflegends/images/a/a4/Level_475_Prestige_Emote.png/revision' \
               '/latest?cb=20180509205316 '
    else:
        return 'https://vignette.wikia.nocookie.net/leagueoflegends/images/b/b8/Level_500_Prestige_Emote.png/revision' \
               '/latest?cb=20180509205438 '


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    user_message = str(message.content)

    if message.author == client.user:
        return

    elif user_message.startswith('!help'):
        embed = discord.Embed(title= 'Summoner Bot Commands', description = '```!lvl``` This command returns the summoner level of the summoner.\n```!masterylvl``` This command returns the mastery level of the summoner and champion. The command should be used as !masterylvl Summoner Name - Champion.\n```!masterypts``` This command returns the amount of mastery points the summoner has on the champion. The command should be used as !masterypts Summoner Name - Champion.\n```!mastery``` This command returns the mastery of the summoner on the champion. The command should be used as !mastery Summoner Name - Champion.\n```!totalmpts``` This command returns the total amount of mastery points of the summoner.\n```!havechest``` returns whether the summoner has received a chest on the champion. The command should be used as !havechest Summoner Name - Champion.\n```!op.gg``` This command returns the summoner\'s op.gg webpage.\n```!rank``` This command returns the Solo/Duo Rank of the summoner.\n```!wr``` This command returns the summoner\'s solo/duo ranked winrate.')
        await message.channel.send(embed=embed)

    elif user_message.startswith('!lvl'):
        summoner_name = user_message.replace('!lvl ', '')
        level = get_summoner_level(summoner_name)
        embed = discord.Embed(title=summoner_name + '\'s Summoner Level',
                              description=summoner_name + ' is level ' +
                              str(level))
        embed.set_thumbnail(url=level_image(level))
        await message.channel.send(embed=embed)

    elif user_message.startswith('!masterylvl'):
        msg = user_message.replace('!masterylvl', '').split(' - ')
        summoner_name = msg[0]
        champion = msg[1]
        level = get_champion_mastery_level(summoner_name, champion)
        embed = discord.Embed(title=summoner_name + '\'s Mastery Level on ' +
                              champion,
                              description='Mastery ' + str(level))
        embed.set_thumbnail(url=mastery_image(level))
        await message.channel.send(embed=embed)

    elif user_message.startswith('!masterypts'):
        msg = user_message.replace('!masterypts', '').split(' - ')
        summoner_name = msg[0]
        champion = msg[1]
        level = get_champion_mastery_level(summoner_name, champion)
        pts = get_champion_mastery_points(summoner_name, champion)
        embed = discord.Embed(
            title=summoner_name + '\'s Mastery Points on ' + champion,
            description=summoner_name + ' has ' + pts + ' on ' + champion)
        embed.set_thumbnail(url=mastery_image(level))
        await message.channel.send(embed=embed)

    elif user_message.startswith('!mastery'):
        msg = user_message.replace('!mastery', '').split(' - ')
        summoner_name = msg[0]
        champion = msg[1]
        embed = discord.Embed(
            title=summoner_name + '\'s Mastery on ' + champion,
            description=summoner_name + ' has ' +
            get_champ_level_points(summoner_name, champion) + ' on ' +
            champion)
        embed.set_thumbnail(url=mastery_image(
            get_champion_mastery_level(summoner_name, champion)))
        await message.channel.send(embed=embed)

    elif user_message.startswith('!totalmpts'):
        summoner_name = user_message.replace('!totalmpts', '')
        score = total_mastery_score(summoner_name)
        embed = discord.Embed(title=summoner_name + '\'s Total Mastery Score',
                              description=summoner_name +
                              ' has a total mastery score of' + score)
        embed.set_thumbnail(
            url=
            'https://boostingmarket.com/images/app/packs/league-of-legends/champion_mastery_hover.png'
        )
        await message.channel.send(embed=embed)

    elif user_message.startswith('!havechest'):
        msg = user_message.replace('!havechest', '').split(' - ')
        summoner_name = msg[0]
        champion = msg[1]
        chest = chest_received(summoner_name, champion)
        if chest:
            statement = ' has received a chest on '
            thumbnail = 'https://static.wikia.nocookie.net/leagueoflegends/images/6/60/' \
                        'Hextech_Crafting_Chest.png/revision/latest/scale-to-width-down/250?cb=20191203123712'
        else:
            statement = ' has not received a chest on '
            thumbnail = 'https://i.imgur.com/Ouf7Ajd.png'

        embed = discord.Embed(title='Has a Chest been Received?',
                              description=summoner_name + statement + champion)
        embed.set_thumbnail(url=thumbnail)
        await message.channel.send(embed=embed)

    elif user_message.startswith('!op.gg'):
        msg0 = user_message.replace('!op.gg ', '')
        msg1 = msg0.replace(' ', '')
        embed = discord.Embed(title='op.gg',
                              url='https://na.op.gg/summoners/na/' + msg1,
                              description=msg0 + '\'s OP.GG')
        embed.set_thumbnail(
            url="https://s-lol-web.op.gg/images/reverse.rectangle.png")
        await message.channel.send(embed=embed)

    elif user_message.startswith('!rank'):
        summoner_name = user_message.replace('!rank', '')
        rank = rank_display_solo(summoner_name)
        embed = discord.Embed(title=summoner_name + '\'s Solo/Duo Rank',
                              description=rank)
        embed.set_thumbnail(url=rank_icons(rank))
        await message.channel.send(embed=embed)

    elif user_message.startswith('!wr'):
        summoner_name = user_message.replace('!wr', '')
        rank = rank_display_solo(summoner_name)
        embed = discord.Embed(title=summoner_name +
                              '\'s Solo/Duo Ranked Win Rate',
                              description=rank_solo_winrate(summoner_name))
        embed.set_thumbnail(url=rank_icons(rank))
        await message.channel.send(embed=embed)


client.run(token)


