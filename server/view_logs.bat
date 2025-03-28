@echo off
echo Monitoring data exploration server logs (press Ctrl+C to exit)
echo =====================================================
echo.

:loop
cls
type server\logs\data_exploration.log
timeout /t 2 /nobreak > nul
goto loop 