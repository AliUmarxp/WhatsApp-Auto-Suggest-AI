@echo off
echo Setting up WhatsApp AI Assistant to run on startup...
set STARTUP_DIR="%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set VBS_PATH=%STARTUP_DIR%\whatsapp_ai.vbs
set SCRIPT_DIR=%~dp0

echo Set WshShell = CreateObject("WScript.Shell") > %VBS_PATH%
echo WshShell.Run "cmd.exe /c cd """ ^& "%SCRIPT_DIR%" ^& """ & python main.py", 0, False >> %VBS_PATH%

echo.
echo Done! Next time you turn on your PC, the assistant will automatically run in the background.
pause
