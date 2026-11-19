
@echo off
chcp 65001 > nul

echo Starting Dependency Visualizer...
echo.

py -u -m src.main %*

echo.
echo Exit code: %ERRORLEVEL%
pause
