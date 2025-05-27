# LOL Bot

디스코드에서 리그 오브 레전드와 TFT 플레이어들의 랭크 정보를 추적하고 관리하는 봇입니다.

## 설정 방법

1. 프로젝트를 클론합니다:
```bash
git clone https://github.com/your-username/lolbot.git
cd lolbot
```

2. 필요한 패키지를 설치합니다:
```bash
pip install -r requirements.txt
```

3. `.env` 파일을 생성하고 다음 정보를 입력합니다:
```env
# Discord Bot Token
DISCORD_TOKEN=your_discord_token_here

# Riot API Keys
RIOT_API_KEY=your_riot_api_key_here
RIOT_LOLCHESS_API_KEY=your_lolchess_api_key_here

# Database Configuration
DB_HOST=mysql
DB_PORT=3306
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
DB_CHARSET=utf8mb4
```

4. 데이터베이스를 설정합니다:
   - MySQL 데이터베이스를 생성하고 위의 DB 설정을 업데이트합니다.
   - 다음 SQL 명령어로 필요한 테이블을 생성합니다:
   ```sql
   CREATE TABLE players (
       id INT AUTO_INCREMENT PRIMARY KEY,
       game_name VARCHAR(255) NOT NULL,
       tag_line VARCHAR(10) NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       UNIQUE KEY unique_player (game_name, tag_line)
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
   ```

5. 봇을 실행합니다:
```bash
python bot.py
```

## 주요 명령어

- `!추가 게임닉네임#태그`: 새로운 플레이어를 등록합니다
- `!목록`: 등록된 플레이어 목록을 보여줍니다
- `!삭제 게임닉네임#태그`: 등록된 플레이어를 삭제합니다
- `!롤티어 게임닉네임#태그`: 플레이어의 롤/TFT 랭크 정보를 조회합니다
- `!누가짱임`: 등록된 플레이어들 중 최고 랭크를 조회합니다

## 환경 변수 설명

- `DISCORD_TOKEN`: 디스코드 봇 토큰
- `RIOT_API_KEY`: Riot Games API 키
- `RIOT_LOLCHESS_API_KEY`: TFT API 키
- `DB_HOST`: 데이터베이스 호스트
- `DB_PORT`: 데이터베이스 포트
- `DB_USER`: 데이터베이스 사용자 이름
- `DB_PASSWORD`: 데이터베이스 비밀번호
- `DB_NAME`: 데이터베이스 이름
- `DB_CHARSET`: 데이터베이스 문자 인코딩

## 데이터베이스 스키마

### players 테이블
플레이어 정보를 저장하는 테이블입니다.

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| id | INT | 자동 증가 기본 키 |
| game_name | VARCHAR(255) | 게임 닉네임 |
| tag_line | VARCHAR(10) | 태그 라인 |
| created_at | TIMESTAMP | 레코드 생성 시간 (자동 설정) |

#### 제약 조건
- `game_name`과 `tag_line`의 조합은 유니크해야 합니다 (UNIQUE KEY)
- 문자셋은 utf8mb4를 사용하여 이모지 등도 저장 가능
- 기본 엔진은 InnoDB 사용 