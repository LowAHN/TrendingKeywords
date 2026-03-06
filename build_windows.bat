@echo off
REM Windows용 빌드 스크립트
REM 사전 준비: Python 3.10+ 설치 후 아래 실행
REM pip install pywebview pyinstaller requests feedparser openpyxl

echo.
echo   TrendingKeywords Windows 빌드 시작
echo.

echo   필요 패키지 설치 중...
pip install pywebview pyinstaller requests feedparser openpyxl

echo.
echo   PyInstaller로 exe 빌드 중...
pyinstaller ^
  --name TrendingKeywords ^
  --windowed ^
  --onefile ^
  --noconfirm ^
  --clean ^
  --hidden-import webview ^
  --hidden-import requests ^
  --hidden-import feedparser ^
  --hidden-import openpyxl ^
  --collect-all webview ^
  --collect-all feedparser ^
  --collect-all openpyxl ^
  app.py

echo.
echo   빌드 완료!
echo   실행파일: dist\TrendingKeywords.exe
echo.
pause
