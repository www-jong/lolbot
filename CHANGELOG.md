# Changelog

## [2.0.0] - 2025-07-10

### 🚀 Major Updates
- **API 엔드포인트 업데이트**: 라이엇 API 변경사항 적용
- **성능 대폭 개선**: 병렬 비동기 처리로 5-8배 속도 향상

### ✨ Added
- 새로운 PUUID 기반 LOL 랭크 API 지원 (`/lol/league/v4/entries/by-puuid/{puuid}`)
- 새로운 TFT 랭크 API 지원 (`/tft/league/v1/by-puuid/{puuid}`)
- 병렬 비동기 처리로 모든 플레이어 정보 동시 조회
- API 세션 재사용으로 성능 최적화
- 체계적인 디버깅 도구 (`debug_api.py`)
- TFT API 오류 시 안전한 폴백 처리

### 🔧 Changed
- `requests` → `aiohttp`로 비동기 HTTP 클라이언트 변경
- API 호출 구조 개선 (순차 → 병렬)
- 더 상세한 오류 로깅 및 상태 코드 표시

### 🐛 Fixed
- 라이엇 API 엔드포인트 변경으로 인한 403 오류 해결
- TFT API PUUID 암호화 오류 안전 처리
- API 키 만료 관련 오류 메시지 개선
- 세션 관리 및 메모리 누수 방지

### 🚮 Removed
- 기존 summoner ID 기반 랭크 API (deprecated)
- 임시 디버깅 로그 제거

### 📈 Performance
- API 응답 속도 5-8배 개선
- 메모리 사용량 최적화
- 동시 연결 처리 개선

---

## [1.0.0] - 2025-05-28

### ✨ Initial Release
- Discord 봇 기본 기능
- 라이엇 API 연동
- 플레이어 관리 (추가/삭제/목록)
- LOL 및 TFT 랭크 조회
- 티어 순위 비교 기능 