
@echo off
chcp 65001 > nul

cd /d "%~dp0\.."

echo [1] Successful dependency retrieval
echo ------------------------------------------
py -m src.main --package flask --repo https://pypi.org/pypi/flask/json
echo.

echo [2] Package not found
echo ------------------------------------------
py -m src.main --package unknown-package-123456 --repo https://pypi.org/pypi/unknown-package-123456/json
echo.

echo [3] Invalid repository response
echo ------------------------------------------
py -m src.main --package flask --repo https://example.com
echo.
pause
