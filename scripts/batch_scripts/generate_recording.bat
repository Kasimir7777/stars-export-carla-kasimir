@echo off
::Kill the new threads (but no other)
taskkill /F /IM "CarlaUE4-Win64-Shipping.exe"
taskkill /F /IM "CarlaUE4.exe"

::First save current pids with the wanted process name
setlocal EnableExtensions EnableDelayedExpansion

::Get CARLA_HOME variable
call config.bat

::Spawn new Carla instance
echo "Start Carla"
start %CARLA_HOME%
timeout /t 10 /nobreak
set PYTHONPATH=.\..\..\

echo "Got seed %1%"
call .\..\..\venv\Scripts\python.exe ./../../helpers/carla_recording_generator.py -l 5 -n 100 -w 50 -s %1
timeout /t 10 /nobreak

::Kill the new threads (but no other)
taskkill /F /IM "CarlaUE4-Win64-Shipping.exe"
taskkill /F /IM "CarlaUE4.exe"
endlocal