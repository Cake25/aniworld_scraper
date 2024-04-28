@echo off

REM Set default values
set SCRIPT_PATH=main.py
set LANGUAGUE=Deutsch
set DLMODE=Series
set PROVIDER=VOE
echo Welcome to the Aniworld.to Bulkdownloader
echo ---------------------------------------
:GET_NAME
REM Prompt for name
set /p NAME=Enter the name: 
if "%NAME%"=="" (
    echo You must enter a name.
	cls
    goto GET_NAME
)

REM Prompt for other values with defaults
set /p TYPE=Enter the type (anime or serie, press Enter for default "anime"): 
if "%TYPE%"=="" set TYPE=default_anime
set TYPE=%TYPE: =%

set /p SEASON=Enter the season (0 for all seasons, otherwise specify, press Enter for default "all-seasons"): 
if "%SEASON%"=="" set SEASON=default_all_seasons
set SEASON=%SEASON: =%

REM Replace default placeholders with actual default values
if "%TYPE%"=="default_anime" set TYPE=anime
if "%SEASON%"=="default_all_seasons" set SEASON=0

REM Script path = File to run
REM Type = anime or serie
REM Name = Name of the anime or series
REM Language = Language of the anime or series most common: ["Deutsch","Ger-Sub","English"]
REM dlMode = Choose your Content ["Movies", "Series", "All"]
REM Season = 0 means all seasons otherwise specify the season you want
REM Provider = Choose your Provider ["VOE", "Vidoza", "Streamtape"]

python %SCRIPT_PATH% %TYPE% %NAME% %LANGUAGUE% %DLMODE% %SEASON% %PROVIDER%
REM Open File Explorer window
start "" explorer "%~dp0\output\"
pause
