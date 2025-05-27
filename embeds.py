import discord
from utils import get_tier_score, get_profile_icon_url

def create_player_list_embed(players):
    if not players:
        return discord.Embed(title="등록된 플레이어가 없습니다.", color=0xff0000)
        
    embed = discord.Embed(title="등록된 플레이어 목록", color=0x00ff00)
    for i, player in enumerate(players, 1):
        embed.add_field(
            name=f"{i}번", 
            value=f"{player['game_name']}#{player['tag_line']}", 
            inline=False
        )
    return embed

def create_rank_embed(game_name, tag_line, summoner_data, solo_rank, tft_rank, ctx):
    embed = discord.Embed(
        title=f"{game_name}#{tag_line}의 랭크 정보",
        color=0x00ff00,
        timestamp=ctx.message.created_at
    )
    
    # 프로필 아이콘 설정
    profile_icon_url = get_profile_icon_url(summoner_data['profileIconId'])
    embed.set_thumbnail(url=profile_icon_url)
    
    # LOL 랭크 정보
    if solo_rank:
        tier = solo_rank['tier']
        rank = solo_rank['rank']
        lp = solo_rank['leaguePoints']
        wins = solo_rank['wins']
        losses = solo_rank['losses']
        win_rate = round((wins / (wins + losses)) * 100, 1)
        
        # 티어 아이콘 URL
        tier_icon_url = f"https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-shared-components/global/default/{tier.lower()}.png"
        embed.set_author(name="League of Legends", icon_url=tier_icon_url)
        
        embed.add_field(
            name="솔로랭크",
            value=f"**{tier} {rank}**\n{lp} LP",
            inline=True
        )
        embed.add_field(
            name="전적",
            value=f"**{wins}승 {losses}패**\n승률 {win_rate}%",
            inline=True
        )
    else:
        embed.add_field(name="League of Legends", value="**UNRANKED**", inline=False)
    
    # 구분선
    embed.add_field(name="\u200b", value="─" * 30, inline=False)
    
    # TFT 랭크 정보
    if tft_rank:
        tier = tft_rank['tier']
        rank = tft_rank['rank']
        lp = tft_rank['leaguePoints']
        
        embed.add_field(
            name="TeamFight Tactics",
            value=f"**{tier} {rank}**\n{lp} LP",
            inline=True
        )
    else:
        embed.add_field(name="TeamFight Tactics", value="**UNRANKED**", inline=True)
    
    # 푸터 추가
    embed.set_footer(text="Updated", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
    
    return embed

def get_str_width(s):
    """문자열의 실제 표시 폭을 계산 (한글=2, 영문/숫자=1)"""
    width = 0
    for c in s:
        if ord(c) > 127:  # 한글, 한자 등 (유니코드 128 이상)
            width += 2
        else:  # 영문, 숫자, 특수문자
            width += 1
    return width

def pad_string(s, target_width):
    """문자열을 목표 폭에 맞춰 오른쪽에 공백 추가"""
    current_width = get_str_width(s)
    padding = target_width - current_width
    return s + ' ' * max(0, padding)

def create_rank_table_embed(title, players, is_lol=True):
    embed = discord.Embed(title=title, color=0x00ff00)
    
    # 각 컬럼의 데이터를 준비
    rank_list = []
    name_list = []
    tier_list = []
    
    for i, player in enumerate(players, 1):
        name = player['name'][:24]  # 닉네임#태그 고려하여 24글자로 여유있게
        
        # 티어 정보 포맷팅
        if player['tier'] not in ['UNRANKED', 'ERROR']:
            # LOL과 TFT 졸업 기준이 다름
            if is_lol:
                # LOL: DIAMOND 이상에 (졸업생) 표시
                if player['tier'] in ['DIAMOND', 'MASTER', 'GRANDMASTER', 'CHALLENGER']:
                    tier_info = f"{player['tier']} {player['rank']} {player['lp']}LP (졸업생)"
                else:
                    tier_info = f"{player['tier']} {player['rank']} {player['lp']}LP"
            else:
                # TFT: GRANDMASTER 이상에 (졸업생) 표시
                if player['tier'] in ['GRANDMASTER', 'CHALLENGER']:
                    tier_info = f"{player['tier']} {player['rank']} {player['lp']}LP (졸업생)"
                else:
                    tier_info = f"{player['tier']} {player['rank']} {player['lp']}LP"
        else:
            tier_info = player['tier']
        
        # 각 리스트에 데이터 추가
        rank_list.append(f"**{i}위**")
        name_list.append(f"**{name}**")
        tier_list.append(tier_info)
    
    # 3개의 필드로 가로 배치
    embed.add_field(
        name="순위",
        value="\n".join(rank_list),
        inline=True
    )
    embed.add_field(
        name="닉네임", 
        value="\n".join(name_list),
        inline=True
    )
    embed.add_field(
        name="티어",
        value="\n".join(tier_list),
        inline=True
    )
    
    return embed