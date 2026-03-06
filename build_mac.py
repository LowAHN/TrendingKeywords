#!/usr/bin/env python3
"""Mac용 .app 및 .dmg 빌드 스크립트"""
import subprocess
import shutil
from pathlib import Path

BASE = Path(__file__).parent
DIST = BASE / "dist"
BUILD = BASE / "build"
APP_NAME = "TrendingKeywords"

def clean():
    print("  이전 빌드 정리...")
    for d in [DIST, BUILD, BASE / f"{APP_NAME}.spec"]:
        if d.is_dir():
            shutil.rmtree(d)
        elif d.is_file():
            d.unlink()

def build_app():
    print("  PyInstaller로 .app 빌드 중...")
    cmd = [
        "pyinstaller",
        "--name", APP_NAME,
        "--windowed",
        "--onedir",
        "--noconfirm",
        "--clean",
        "--add-data", "app.py:.",
        "--hidden-import", "webview",
        "--hidden-import", "requests",
        "--hidden-import", "feedparser",
        "--hidden-import", "openpyxl",
        "--hidden-import", "sgmllib",
        "--hidden-import", "sgmllib3k",
        "--collect-all", "webview",
        "--collect-all", "feedparser",
        "--collect-all", "openpyxl",
        str(BASE / "app.py"),
    ]
    subprocess.run(cmd, cwd=str(BASE), check=True)
    print(f"  .app 빌드 완료: {DIST / APP_NAME}.app")

def create_dmg():
    print("  DMG 생성 중...")
    app_path = DIST / APP_NAME / f"{APP_NAME}.app"
    dmg_path = DIST / f"{APP_NAME}.dmg"

    if not app_path.exists():
        print(f"  [오류] {app_path} 없음")
        return

    # DMG 임시 폴더
    dmg_dir = DIST / "dmg_temp"
    if dmg_dir.exists():
        shutil.rmtree(dmg_dir)
    dmg_dir.mkdir()

    # .app 복사
    shutil.copytree(str(app_path), str(dmg_dir / f"{APP_NAME}.app"))

    # Applications 심볼릭 링크
    (dmg_dir / "Applications").symlink_to("/Applications")

    # DMG 생성
    if dmg_path.exists():
        dmg_path.unlink()

    subprocess.run([
        "hdiutil", "create",
        "-volname", APP_NAME,
        "-srcfolder", str(dmg_dir),
        "-ov",
        "-format", "UDZO",
        str(dmg_path),
    ], check=True)

    shutil.rmtree(dmg_dir)
    print(f"  DMG 생성 완료: {dmg_path}")

if __name__ == "__main__":
    print(f"\n  {APP_NAME} Mac 빌드 시작\n")
    clean()
    build_app()
    create_dmg()
    print(f"\n  빌드 완료!")
    print(f"  DMG: {DIST / f'{APP_NAME}.dmg'}\n")
