
@echo off
chcp 65001 > nul

cd /d "%~dp0\.."

echo ==========================================
echo       DEPENDENCY VISUALIZER
echo             DEMO STAGE 1
echo ==========================================
echo.

echo [1] Correct configuration
echo ------------------------------------------
py -m src.main --package flask --repo https://pypi.org/pypi/flask/json
echo.

echo [2] Invalid package name
echo ------------------------------------------
py -m src.main --package "bad package!" --repo https://pypi.org/pypi/flask/json
echo.

echo [3] Invalid repository URL
echo ------------------------------------------
py -m src.main --package flask --repo invalid_url
echo.

echo [4] Invalid test mode
echo ------------------------------------------
py -m src.main --package flask --repo https://pypi.org/pypi/flask/json --test-mode yes
echo.

echo [5] Invalid output file
echo ------------------------------------------
py -m src.main --package flask --repo https://pypi.org/pypi/flask/json --output graph.txt
echo.

echo [6] Invalid ASCII argument
echo ------------------------------------------
py -m src.main --package flask --repo https://pypi.org/pypi/flask/json --ascii yes
echo.

echo [7] Invalid maximum depth
echo ------------------------------------------
py -m src.main --package flask --repo https://pypi.org/pypi/flask/json --max-depth -1
echo.

echo ==========================================
echo             DEMO COMPLETED
echo ==========================================

pause
