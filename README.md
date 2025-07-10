# LOL Bot

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/your-username/lolbot/releases)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![Discord.py](https://img.shields.io/badge/discord.py-2.0+-purple.svg)](https://github.com/Rapptz/discord.py)
[![Riot API](https://img.shields.io/badge/Riot%20API-v4-red.svg)](https://developer.riotgames.com/)

디스코드에서 리그 오브 레전드와 TFT 플레이어들의 랭크 정보를 추적하고 관리하는 봇입니다.

## 📋 목차

- [🚀 최신 업데이트](#-최신-업데이트)
- [⚡ 주요 기능](#-주요-기능)
- [📦 설정 방법](#-설정-방법)
- [🎮 주요 명령어](#-주요-명령어)
- [🔧 디버깅](#-디버깅)
- [📈 성능](#-성능)
- [📝 변경내역](#-변경내역)

## 🚀 최신 업데이트

### v2.0.0 - 라이엇 API v2 업데이트 및 성능 최적화
- ⚡ **5-8배 빠른 속도**: 병렬 비동기 처리로 대폭 개선
- 🔄 **새로운 API**: PUUID 기반 엔드포인트 적용
- 🛡️ **안정성 향상**: TFT API 오류 안전 처리
- 🔧 **디버깅 도구**: 체계적인 API 테스트 기능 추가

👉 **[전체 변경내역 보기](./CHANGELOG.md)**

## ⚡ 주요 기능

- 🎯 **실시간 랭크 조회**: LOL 솔로랭크 & TFT 랭크 동시 조회
- 👥 **플레이어 관리**: 추가/삭제/목록 관리
- 🏆 **순위 비교**: 등록된 플레이어들의 티어 순위
- ⚡ **고속 처리**: 병렬 비동기 처리로 빠른 응답
- 🛡️ **안전한 처리**: API 오류 시 자동 폴백
- 🔧 **디버깅 도구**: 개발자용 API 테스트 도구

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

## 🎮 주요 명령어

- `!추가 게임닉네임#태그`: 새로운 플레이어를 등록합니다
- `!목록`: 등록된 플레이어 목록을 보여줍니다
- `!삭제 게임닉네임#태그`: 등록된 플레이어를 삭제합니다
- `!롤티어 게임닉네임#태그`: 플레이어의 롤/TFT 랭크 정보를 조회합니다
- `!누가짱임`: 등록된 플레이어들 중 최고 랭크를 조회합니다

## 🔧 디버깅

API 연결 문제나 오류가 발생할 때 사용할 수 있는 디버깅 도구를 제공합니다:

### 빠른 상태 확인
```bash
python debug_api.py
# 메뉴에서 1번 선택
```

### 특정 플레이어 테스트
```bash
python debug_api.py "Hide on bush#KR1"
```

### 대화형 디버깅
```bash
python debug_api.py
# 메뉴에서 원하는 옵션 선택
```

## 📈 성능

### v2.0.0 성능 개선사항
- **API 응답 속도**: 5-8배 개선 (병렬 비동기 처리)
- **메모리 사용량**: 세션 재사용으로 최적화
- **동시 처리**: 모든 플레이어 정보를 병렬로 조회
- **오류 처리**: TFT API 오류 시 LOL 정보만 표시하여 중단 방지

### 기술 스택
- **비동기 처리**: `asyncio.gather()` 활용
- **HTTP 클라이언트**: `aiohttp` (기존 `requests` 대체)
- **세션 관리**: 글로벌 세션 재사용
- **오류 복구**: 안전한 폴백 메커니즘

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

## 📝 변경내역

모든 주요 변경사항과 릴리스 정보는 [CHANGELOG.md](./CHANGELOG.md)에서 확인할 수 있습니다.

### 최근 릴리스
- **[v2.0.0](./CHANGELOG.md#200---2025-07-10)** - 라이엇 API v2 업데이트 및 성능 최적화
- **[v1.0.0](./CHANGELOG.md#100---2025-05-28)** - 초기 릴리스

---

## 📄 라이선스

이 프로젝트는 개인용 프로젝트입니다.

## 🤝 기여하기

이슈나 개선사항이 있으시면 GitHub Issues를 통해 알려주세요! 