import discord
from discord.ext import commands
import aiohttp
import os
import asyncio
from utils import get_account_info, get_summoner_info, get_rank_info, get_tft_summoner_info, get_tft_rank_info, get_tier_score, get_player_all_info_safe
from database import get_players_from_db, add_player, remove_player
from embeds import create_player_list_embed, create_rank_embed, create_rank_table_embed

class LolCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.riot_api_key = os.getenv('RIOT_API_KEY')
        self.riot_lolchess_api_key = os.getenv('RIOT_LOLCHESS_API_KEY')

    @commands.command(name='추가')
    async def add_player_command(self, ctx, *, arg):
        try:
            if '#' not in arg:
                await ctx.send('올바른 형식: !추가 게임닉네임#태그')
                return
            
            game_name, tag_line = arg.split('#')
            
            # API를 통해 플레이어 존재 여부 확인
            account_url = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
            headers = {"X-Riot-Token": self.riot_api_key}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(account_url, headers=headers) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        print(f"Add Player API Error: {response.status} - {error_text}")
                        await ctx.send("존재하지 않는 플레이어입니다.")
                        return
                
            if add_player(game_name, tag_line):
                await ctx.send(f"플레이어 {game_name}#{tag_line} 가 추가되었습니다.")
            else:
                await ctx.send("이미 등록된 플레이어입니다.")
                
        except Exception as e:
            print(f"Add player error: {e}")
            await ctx.send(f"오류가 발생했습니다: {str(e)}")

    @commands.command(name='목록')
    async def list_players_command(self, ctx):
        try:
            players = get_players_from_db()
            embed = create_player_list_embed(players)
            await ctx.send(embed=embed)
        except Exception as e:
            print(f"List players error: {e}")
            await ctx.send(f"오류가 발생했습니다: {str(e)}")

    @commands.command(name='삭제')
    async def remove_player_command(self, ctx, *, arg):
        try:
            if '#' not in arg:
                await ctx.send('올바른 형식: !삭제 게임닉네임#태그')
                return
            
            game_name, tag_line = arg.split('#')
            
            if remove_player(game_name, tag_line):
                await ctx.send(f"플레이어 {game_name}#{tag_line} 가 삭제되었습니다.")
            else:
                await ctx.send("등록되지 않은 플레이어입니다.")
                
        except Exception as e:
            print(f"Remove player error: {e}")
            await ctx.send(f"오류가 발생했습니다: {str(e)}")

    @commands.command(name='롤티어')
    async def get_rank_command(self, ctx, *, arg):
        try:
            if '#' not in arg:
                await ctx.send('올바른 형식: !롤티어 게임닉네임#태그')
                return
            
            game_name, tag_line = arg.split('#')
            lol_headers = {"X-Riot-Token": self.riot_api_key}
            tft_headers = {"X-Riot-Token": self.riot_lolchess_api_key}
            
            # 안전한 함수 사용 (TFT API 오류 시 LOL만 표시)
            player_data = await get_player_all_info_safe(game_name, tag_line, lol_headers, tft_headers)
            
            # 솔로랭크 정보 찾기
            solo_rank = None
            for queue in player_data['rank']:
                if queue['queueType'] == 'RANKED_SOLO_5x5':
                    solo_rank = queue
                    break
            
            # TFT 랭크 정보 찾기
            tft_rank = None
            if player_data['tft_rank']:  # TFT 데이터가 있는 경우만
                for queue in player_data['tft_rank']:
                    if queue['queueType'] == 'RANKED_TFT':
                        tft_rank = queue
                        break
            
            embed = create_rank_embed(game_name, tag_line, player_data['summoner'], solo_rank, tft_rank, ctx)
            await ctx.send(embed=embed)
                
        except Exception as e:
            print(f"Get rank error: {e}")
            await ctx.send(f"오류가 발생했습니다: {str(e)}")

    @commands.command(name='누가짱임')
    async def who_is_best_command(self, ctx):
        try:
            message = await ctx.send(embed=discord.Embed(title="티어 순위 로딩중..."))
            lol_headers = {"X-Riot-Token": self.riot_api_key}
            tft_headers = {"X-Riot-Token": self.riot_lolchess_api_key}
            
            player_ranks = []
            player_tft_ranks = []

            players = get_players_from_db()
            
            # 모든 플레이어의 정보를 병렬로 가져오기 (속도 최적화)
            async def process_player(player):
                try:
                    player_data = await get_player_all_info_safe(player['name'], player['tag'], lol_headers, tft_headers)
                    
                    # LOL 솔로랭크 처리
                    solo_rank = None
                    for queue in player_data['rank']:
                        if queue['queueType'] == 'RANKED_SOLO_5x5':
                            solo_rank = queue
                            break
                    
                    if solo_rank:
                        tier_score = get_tier_score(solo_rank['tier'], solo_rank['rank'], solo_rank['leaguePoints'])
                        lol_result = {
                            'name': f"{player['name']}#{player['tag']}",
                            'tier': solo_rank['tier'],
                            'rank': solo_rank['rank'],
                            'lp': solo_rank['leaguePoints'],
                            'tier_score': tier_score
                        }
                    else:
                        lol_result = {
                            'name': f"{player['name']}#{player['tag']}",
                            'tier': 'UNRANKED',
                            'rank': '',
                            'lp': 0,
                            'tier_score': -1
                        }

                    # TFT 랭크 처리 (안전하게)
                    tft_rank = None
                    if player_data['tft_rank']:  # TFT 데이터가 있는 경우만
                        for queue in player_data['tft_rank']:
                            if queue['queueType'] == 'RANKED_TFT':
                                tft_rank = queue
                                break
                    
                    if tft_rank:
                        tier_score = get_tier_score(tft_rank['tier'], tft_rank['rank'], tft_rank['leaguePoints'])
                        tft_result = {
                            'name': f"{player['name']}#{player['tag']}",
                            'tier': tft_rank['tier'],
                            'rank': tft_rank['rank'],
                            'lp': tft_rank['leaguePoints'],
                            'tier_score': tier_score
                        }
                    else:
                        tft_result = {
                            'name': f"{player['name']}#{player['tag']}",
                            'tier': 'UNRANKED',
                            'rank': '',
                            'lp': 0,
                            'tier_score': -1
                        }
                    
                    return lol_result, tft_result
                        
                except Exception as e:
                    print(f"Error getting rank for {player['name']}: {e}")
                    error_result = {
                        'name': f"{player['name']}#{player['tag']}",
                        'tier': 'ERROR',
                        'rank': '',
                        'lp': 0,
                        'tier_score': -1
                    }
                    return error_result, error_result
            
            # 모든 플레이어를 병렬로 처리
            tasks = [process_player(player) for player in players]
            results = await asyncio.gather(*tasks)
            
            # 결과 분리
            for lol_result, tft_result in results:
                player_ranks.append(lol_result)
                player_tft_ranks.append(tft_result)
            
            # 티어 점수로 정렬
            player_ranks.sort(key=lambda x: x['tier_score'], reverse=True)
            player_tft_ranks.sort(key=lambda x: x['tier_score'], reverse=True)
            
            # LOL 랭크 임베드
            lol_embed = create_rank_table_embed("League of Legends 티어 순위", player_ranks, True)
            await message.edit(embed=lol_embed)
            
            # TFT 랭크 임베드
            tft_embed = create_rank_table_embed("TeamFight Tactics 티어 순위", player_tft_ranks, False)
            await ctx.send(embed=tft_embed)
            
        except Exception as e:
            error_embed = discord.Embed(title="오류 발생", color=0xff0000)
            error_embed.add_field(name="Error", value=str(e), inline=False)
            await message.edit(embed=error_embed) 