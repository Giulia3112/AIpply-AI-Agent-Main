@echo off
echo ========================================
echo AIPPLY API VISUALIZATION COMMANDS
echo ========================================

echo.
echo 1. Running Code Structure Analysis...
python visualize_code.py

echo.
echo 2. Creating Directory Tree...
tree /f /a

echo.
echo 3. Showing File Sizes...
for %%f in (*.py) do echo %%~nxf: %%~zf bytes
for /r startup_opps_api %%f in (*.py) do echo %%~nxf: %%~zf bytes

echo.
echo 4. Running FastAPI Documentation...
echo Starting FastAPI server for interactive docs...
echo Visit: http://localhost:8000/docs
echo Press Ctrl+C to stop
python main.py

pause
