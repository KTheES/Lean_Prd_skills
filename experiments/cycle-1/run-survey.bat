@echo off
cd /d "%~dp0"
python survey_gui.py
if errorlevel 1 pause
