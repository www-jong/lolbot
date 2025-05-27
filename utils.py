import discord
import requests

async def get_account_info(game_name, tag, headers):
    account_url = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag}"
    account_response = requests.get(account_url, headers=headers)
    if account_response.status_code != 200:
        raise Exception("플레이어를 찾을 수 없습니다.")
    return account_response.json()

async def get_summoner_info(puuid, headers):
    summoner_url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    summoner_response = requests.get(summoner_url, headers=headers)
    if summoner_response.status_code != 200:
        raise Exception("소환사 정보를 찾을 수 없습니다.")
    return summoner_response.json()

async def get_rank_info(summoner_id, headers):
    rank_url = f"https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
    rank_response = requests.get(rank_url, headers=headers)
    if rank_response.status_code != 200:
        raise Exception("랭크 정보를 가져오는데 실패했습니다.")
    return rank_response.json()

def get_tier_score(tier, rank, lp):
    tier_mapping = {
        'IRON': 0, 'BRONZE': 1, 'SILVER': 2, 'GOLD': 3,
        'PLATINUM': 4, 'EMERALD': 5, 'DIAMOND': 6,
        'MASTER': 7, 'GRANDMASTER': 8, 'CHALLENGER': 9
    }
    rank_mapping = {'IV': 0, 'III': 1, 'II': 2, 'I': 3}
    return (tier_mapping[tier] * 400 + rank_mapping[rank] * 100 + lp)

async def get_tft_summoner_info(puuid, headers):
    tft_summoner_url = f"https://kr.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/{puuid}"
    tft_summoner_response = requests.get(tft_summoner_url, headers=headers)
    if tft_summoner_response.status_code != 200:
        raise Exception("TFT 소환사 정보를 가져오는데 실패했습니다.")
    return tft_summoner_response.json()


async def get_tft_rank_info(summoner_id, headers):
    tft_rank_url = f"https://kr.api.riotgames.com/tft/league/v1/entries/by-summoner/{summoner_id}"
    tft_rank_response = requests.get(tft_rank_url, headers=headers)
    if tft_rank_response.status_code != 200:
        raise Exception("TFT 랭크 정보를 가져오는데 실패했습니다.")
    return tft_rank_response.json()


def get_profile_icon_url(profile_icon_id):
    return f"http://ddragon.leagueoflegends.com/cdn/13.24.1/img/profileicon/{profile_icon_id}.png"

def create_rank_embed(title, color=0x00ff00):
    return discord.Embed(title=title, color=color)
