# Trending Keywords - 실시간 인기 키워드 수집기

구글, 네이버에서 실시간 인기 키워드를 자동으로 수집하는 데스크톱 앱입니다.
블로그 키워드 발굴, 트렌드 분석, 콘텐츠 기획에 활용하세요.

## 주요 기능

- 네이버 실시간 검색어 TOP 10 수집 (순위 변동 표시)
- 구글 트렌드 실시간 급상승 검색어 수집
- 구글 / 네이버 자동완성 연관 키워드 수집
- 원하는 키워드 입력 시 관련 인기 검색어 자동 탐색
- TXT / 엑셀(XLSX) / JSON 형식으로 저장
- 키워드 클립보드 복사

## 설치 파일 다운로드

[Releases 페이지](../../releases)에서 최신 버전을 다운로드하세요.

| 운영체제 | 파일 | 설명 |
|---------|------|------|
| Mac | `TrendingKeywords.dmg` | macOS용 설치 파일 |
| Windows | `TrendingKeywords.exe` | Windows용 실행 파일 |

### Mac 설치 방법

1. [Releases 페이지](../../releases)에서 `TrendingKeywords.dmg` 다운로드
2. DMG 파일을 더블클릭하여 열기
3. `TrendingKeywords` 앱을 `Applications` 폴더로 드래그
4. 처음 실행 시 보안 경고가 뜰 수 있습니다:
   - `TrendingKeywords` 앱을 **우클릭** → **열기** 클릭
   - 또는 **시스템 설정** → **개인정보 보호 및 보안** → 하단에서 **확인 없이 열기** 클릭

### Windows 설치 방법

1. [Releases 페이지](../../releases)에서 `TrendingKeywords.exe` 다운로드
2. 다운로드된 exe 파일을 더블클릭하여 실행 (별도 설치 과정 없음)
3. Windows Defender SmartScreen 경고가 뜰 경우:
   - **추가 정보** 클릭 → **실행** 클릭

## 사용 방법

1. 앱을 실행합니다
2. 상단 입력란에 키워드를 쉼표로 구분하여 입력합니다 (예: `맛집, 여행, 다이어트`)
3. **검색 시작** 버튼을 클릭하거나 Enter를 누릅니다
4. 탭별로 결과를 확인합니다:
   - **네이버 실시간**: 네이버 실시간 검색어 TOP 10 (상승/하락/신규 표시)
   - **구글 연관검색어**: 입력한 키워드의 구글 인기 연관 검색어
   - **네이버 연관검색어**: 입력한 키워드의 네이버 인기 연관 검색어
   - **구글 급상승**: 한국 전체 구글 실시간 급상승 검색어
   - **전체 키워드**: 수집된 모든 키워드 모아보기
5. 원하는 형식으로 저장합니다:
   - **TXT 저장**: 보기 편한 텍스트 형식
   - **엑셀 저장**: 시트별 분류된 엑셀 파일
   - **JSON 저장**: 프로그램용 원본 데이터
6. **키워드 복사** 버튼으로 전체 키워드를 클립보드에 복사할 수 있습니다

## 소스에서 직접 실행하기

Python 3.10 이상이 필요합니다.

```bash
# 저장소 클론
git clone https://github.com/LowAHN/TrendingKeywords.git
cd TrendingKeywords

# 패키지 설치
pip install pywebview requests feedparser openpyxl

# 실행
python app.py
```

## 직접 빌드하기

### Mac
```bash
pip install pywebview pyinstaller requests feedparser openpyxl
python build_mac.py
# 결과: dist/TrendingKeywords.dmg
```

### Windows
```cmd
build_windows.bat
# 결과: dist\TrendingKeywords.exe
```

## 데이터 출처

| 소스 | 설명 |
|------|------|
| 네이버 실시간 검색어 | 실시간 인기 검색어 TOP 10 |
| 구글 트렌드 | 한국 실시간 급상승 검색어 |
| 구글 자동완성 | 구글 검색창 추천어 |
| 네이버 자동완성 | 네이버 검색창 추천어 |

## 라이선스

MIT License
