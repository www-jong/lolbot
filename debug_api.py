"""
라이엇 API 디버깅 도구
사용법: python debug_api.py [플레이어명#태그]
"""
import asyncio
import sys
from utils import get_account_info, get_summoner_info, get_rank_info, get_tft_summoner_info, get_tft_rank_info
import os
from dotenv import load_dotenv

load_dotenv()

class APIDebugger:
    def __init__(self):
        self.riot_api_key = os.getenv('RIOT_API_KEY')
        self.riot_lolchess_api_key = os.getenv('RIOT_LOLCHESS_API_KEY')
        self.lol_headers = {"X-Riot-Token": self.riot_api_key}
        self.tft_headers = {"X-Riot-Token": self.riot_lolchess_api_key}

    def print_section(self, title):
        print(f"\n{'='*50}")
        print(f" {title}")
        print(f"{'='*50}")

    def print_subsection(self, title):
        print(f"\n[{title}]")

    async def test_player(self, game_name, tag_line):
        """특정 플레이어의 모든 API를 테스트합니다."""
        self.print_section(f"플레이어 테스트: {game_name}#{tag_line}")
        
        try:
            # 1. Account API 테스트
            self.print_subsection("Account API")
            account_data = await get_account_info(game_name, tag_line, self.lol_headers)
            print(f"✅ 성공: PUUID = {account_data['puuid']}")
            print(f"   Game Name: {account_data['gameName']}")
            print(f"   Tag Line: {account_data['tagLine']}")
            
            # 2. LOL Summoner API 테스트
            self.print_subsection("LOL Summoner API")
            summoner_data = await get_summoner_info(account_data['puuid'], self.lol_headers)
            print(f"✅ 성공: Summoner ID = {summoner_data['id']}")
            print(f"   Level: {summoner_data['summonerLevel']}")
            print(f"   Profile Icon: {summoner_data['profileIconId']}")
            
            # 3. LOL Rank API 테스트
            self.print_subsection("LOL Rank API")
            rank_data = await get_rank_info(account_data['puuid'], self.lol_headers)
            print(f"✅ 성공: {len(rank_data)}개의 랭크 정보")
            for i, queue in enumerate(rank_data):
                print(f"   {i+1}. {queue['queueType']}: {queue.get('tier', 'UNRANKED')} {queue.get('rank', '')} {queue.get('leaguePoints', 0)}LP")
            
            # 4. TFT Summoner API 테스트
            self.print_subsection("TFT Summoner API")
            tft_summoner_data = await get_tft_summoner_info(account_data['puuid'], self.tft_headers)
            print(f"✅ 성공: TFT Summoner ID = {tft_summoner_data['id']}")
            
            # 5. TFT Rank API 테스트
            self.print_subsection("TFT Rank API")
            tft_rank_data = await get_tft_rank_info(account_data['puuid'], self.tft_headers)
            print(f"✅ 성공: {len(tft_rank_data)}개의 TFT 랭크 정보")
            for i, queue in enumerate(tft_rank_data):
                print(f"   {i+1}. {queue['queueType']}: {queue.get('tier', 'UNRANKED')} {queue.get('rank', '')} {queue.get('leaguePoints', 0)}LP")
            
            self.print_section("테스트 완료")
            print("✅ 모든 API가 정상적으로 작동합니다!")
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")

    async def test_api_endpoints(self):
        """API 엔드포인트들을 테스트합니다."""
        self.print_section("API 엔드포인트 테스트")
        
        # 테스트용 플레이어 (Faker)
        test_player = "Hide on bush"
        test_tag = "KR1"
        
        print(f"테스트 플레이어: {test_player}#{test_tag}")
        
        endpoints = [
            ("Account API", f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{test_player}/{test_tag}"),
            ("LOL Summoner API", "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"),
            ("LOL Rank API", "https://kr.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}"),
            ("TFT Summoner API", "https://kr.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/{puuid}"),
            ("TFT Rank API", "https://kr.api.riotgames.com/tft/league/v1/by-puuid/{puuid}"),
        ]
        
        for name, url in endpoints:
            print(f"{name}: {url}")
        
        print("\n실제 테스트 시작...")
        await self.test_player(test_player, test_tag)

    async def quick_test(self):
        """빠른 API 상태 확인"""
        self.print_section("빠른 API 상태 확인")
        
        try:
            # Hide on bush 테스트
            account_data = await get_account_info("Hide on bush", "KR1", self.lol_headers)
            print("✅ API 키가 정상적으로 작동합니다")
            print(f"✅ 계정 조회 성공: {account_data['gameName']}#{account_data['tagLine']}")
            
            # Rank API 테스트
            rank_data = await get_rank_info(account_data['puuid'], self.lol_headers)
            print(f"✅ 랭크 조회 성공: {len(rank_data)}개의 랭크 정보")
            
            # TFT API 테스트
            tft_rank_data = await get_tft_rank_info(account_data['puuid'], self.tft_headers)
            print(f"✅ TFT 랭크 조회 성공: {len(tft_rank_data)}개의 TFT 랭크 정보")
            
        except Exception as e:
            print(f"❌ API 오류: {e}")

async def main():
    debugger = APIDebugger()
    
    if len(sys.argv) > 1:
        # 특정 플레이어 테스트
        player_input = sys.argv[1]
        if '#' in player_input:
            game_name, tag_line = player_input.split('#')
            await debugger.test_player(game_name, tag_line)
        else:
            print("❌ 올바른 형식으로 입력하세요: python debug_api.py 플레이어명#태그")
    else:
        # 메뉴 선택
        print("라이엇 API 디버깅 도구")
        print("1. 빠른 상태 확인")
        print("2. 엔드포인트 테스트")
        print("3. 특정 플레이어 테스트")
        
        choice = input("선택하세요 (1-3): ")
        
        if choice == "1":
            await debugger.quick_test()
        elif choice == "2":
            await debugger.test_api_endpoints()
        elif choice == "3":
            player_input = input("플레이어명#태그를 입력하세요: ")
            if '#' in player_input:
                game_name, tag_line = player_input.split('#')
                await debugger.test_player(game_name, tag_line)
            else:
                print("❌ 올바른 형식으로 입력하세요")

if __name__ == "__main__":
    asyncio.run(main()) 