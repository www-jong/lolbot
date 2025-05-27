import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from commands import LolCommands

# .env 파일에서 환경변수 로드
load_dotenv()

# 봇 설정
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} 로 로그인했습니다!')
    await bot.add_cog(LolCommands(bot))

# 환경변수에서 토큰 가져오기
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

bot.run(DISCORD_TOKEN)
