import discord
import aiohttp
import asyncio

# 글로벌 세션 (재사용을 위해)
_session = None

async def get_session():
    """공유 세션을 반환합니다."""
    global _session
    if _session is None or _session.closed:
        _session = aiohttp.ClientSession()
    return _session

async def close_session():
    """세션을 닫습니다."""
    global _session
    if _session and not _session.closed:
        await _session.close()

async def get_account_info(game_name, tag, headers):
    account_url = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag}"
    session = await get_session()
    async with session.get(account_url, headers=headers) as response:
        if response.status != 200:
            error_text = await response.text()
            print(f"Account API Error: {response.status} - {error_text}")
            raise Exception(f"플레이어를 찾을 수 없습니다. (Status: {response.status})")
        return await response.json()

async def get_summoner_info(puuid, headers):
    summoner_url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    session = await get_session()
    async with session.get(summoner_url, headers=headers) as response:
        if response.status != 200:
            error_text = await response.text()
            print(f"Summoner API Error: {response.status} - {error_text}")
            raise Exception(f"소환사 정보를 찾을 수 없습니다. (Status: {response.status})")
        return await response.json()

async def get_rank_info(puuid, headers):
    rank_url = f"https://kr.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}"
    session = await get_session()
    async with session.get(rank_url, headers=headers) as response:
        if response.status != 200:
            error_text = await response.text()
            print(f"Rank API Error: {response.status} - {error_text}")
            raise Exception(f"랭크 정보를 가져오는데 실패했습니다. (Status: {response.status})")
        return await response.json()

async def get_tft_summoner_info(puuid, headers):
    tft_summoner_url = f"https://kr.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/{puuid}"
    session = await get_session()
    async with session.get(tft_summoner_url, headers=headers) as response:
        if response.status != 200:
            error_text = await response.text()
            print(f"TFT Summoner API Error: {response.status} - {error_text}")
            raise Exception(f"TFT 소환사 정보를 가져오는데 실패했습니다. (Status: {response.status})")
        return await response.json()

async def get_tft_rank_info(puuid, headers):
    tft_rank_url = f"https://kr.api.riotgames.com/tft/league/v1/by-puuid/{puuid}"
    session = await get_session()
    async with session.get(tft_rank_url, headers=headers) as response:
        if response.status != 200:
            error_text = await response.text()
            print(f"TFT Rank API Error: {response.status} - {error_text}")
            raise Exception(f"TFT 랭크 정보를 가져오는데 실패했습니다. (Status: {response.status})")
        return await response.json()

async def get_player_lol_info_only(game_name, tag, lol_headers):
    """LOL 정보만 가져옵니다. (TFT API 문제 시 대안)"""
    try:
        account_data = await get_account_info(game_name, tag, lol_headers)
        
        tasks = [
            get_summoner_info(account_data['puuid'], lol_headers),
            get_rank_info(account_data['puuid'], lol_headers)
        ]
        
        summoner_data, rank_data = await asyncio.gather(*tasks)
        
        return {
            'account': account_data,
            'summoner': summoner_data,
            'rank': rank_data,
            'puuid': account_data['puuid']
        }
    except Exception as e:
        print(f"Error getting LOL info for {game_name}#{tag}: {e}")
        raise e

async def get_player_all_info_safe(game_name, tag, lol_headers, tft_headers):
    """TFT API 오류를 안전하게 처리하는 버전"""
    try:
        # LOL 정보는 항상 가져오기
        lol_info = await get_player_lol_info_only(game_name, tag, lol_headers)
        
        # TFT 정보는 오류 시 빈 데이터로 처리
        try:
            tft_account_data = await get_account_info(game_name, tag, tft_headers)
            tft_summoner_data = await get_tft_summoner_info(tft_account_data['puuid'], tft_headers)
            tft_rank_data = await get_tft_rank_info(tft_account_data['puuid'], tft_headers)
            
            return {
                **lol_info,
                'tft_account': tft_account_data,
                'tft_summoner': tft_summoner_data,
                'tft_rank': tft_rank_data,
                'tft_puuid': tft_account_data['puuid']
            }
        except Exception as tft_error:
            print(f"TFT API Error for {game_name}#{tag}: {tft_error}")
            # TFT 정보 없이 LOL 정보만 반환
            return {
                **lol_info,
                'tft_account': None,
                'tft_summoner': None,
                'tft_rank': [],
                'tft_puuid': None
            }
            
    except Exception as e:
        print(f"Error getting info for {game_name}#{tag}: {e}")
        raise e

def get_tier_score(tier, rank, lp):
    tier_mapping = {
        'IRON': 0, 'BRONZE': 1, 'SILVER': 2, 'GOLD': 3,
        'PLATINUM': 4, 'EMERALD': 5, 'DIAMOND': 6,
        'MASTER': 7, 'GRANDMASTER': 8, 'CHALLENGER': 9
    }
    rank_mapping = {'IV': 0, 'III': 1, 'II': 2, 'I': 3}
    return (tier_mapping[tier] * 400 + rank_mapping[rank] * 100 + lp)

def get_profile_icon_url(profile_icon_id):
    return f"http://ddragon.leagueoflegends.com/cdn/13.24.1/img/profileicon/{profile_icon_id}.png"

def create_rank_embed(title, color=0x00ff00):
    return discord.Embed(title=title, color=color)
