@echo off
title CYBERMOKSHA WEEK 2 - DEPLOY TO GITHUB ACTIONS 24/7 STREAM ENGINE
echo ============================================================================
echo   CYBERMOKSHA WEEK 2 - DEPLOY STREAM WORKFLOW ^& RELEASE ASSETS
echo ============================================================================
echo.

if "%GH_PAT%"=="" (
    set /p GH_PAT="Enter your GitHub PAT (Personal Access Token) with repo scope: "
)

if "%GH_PAT%"=="" (
    echo [!] No token provided. Exiting.
    pause
    exit /b
)

echo.
echo [+] Committing and pushing updated stream.yml to GitHub main branch...
git add .github/workflows/stream.yml
git commit -m "Update stream.yml for Week 2 24/7 Live Stream multi-mode support" 2>nul
git push https://%GH_PAT%@github.com/madpunks007/cybermoksha-stream-engine.git main
if %ERRORLEVEL% NEQ 0 (
    echo [!] Note: Git push encountered an issue. Check network or PAT permissions.
)

echo.
echo [+] Uploading Week 2 master videos to GitHub Release v2.0...
python upload_week2_release.py "%GH_PAT%"

echo.
echo ============================================================================
echo [+] DEPLOYMENT FINISHED!
echo     Go to Actions in your GitHub repo and run "24/7 CYBERMOKSHA Live Stream Engine"
echo ============================================================================
pause
