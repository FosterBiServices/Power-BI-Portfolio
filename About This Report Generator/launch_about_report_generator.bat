@echo off
call C:\ProgramData\anaconda3\Scripts\activate.bat
cd /d "%~dp0"
python -m about_report_generator
if errorlevel 1 pause
