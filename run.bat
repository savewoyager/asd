
@echo off
chcp 65001 > nul

py -u -m src.main %*

echo.
echo Exit code: %ERRORLEVEL%


pause
