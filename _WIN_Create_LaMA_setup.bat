@echo off
setlocal

:: ==============================
:: Variablen
:: ==============================
set "PYINSTALLER_EXE=C:\Users\cwebe\AppData\Roaming\Python\Python313\Scripts\pyinstaller.exe"
:: WORKING: C:\Users\cwebe\AppData\Local\Programs\Python\Python312\Scripts\pyinstaller.exe
:: C:\Users\cwebe\AppData\Roaming\Python\Python313\Scripts\pyinstaller.exe
set "EXE_NAME=LaMA.exe"
set "BUILD_DIR=dist"
set "DEST_DIR=C:\Users\cwebe\Desktop\_create_lama_installer"
set "SETUP_PATH=%DEST_DIR%\lama_installer\LaMA_setup.exe"
set "ARCHIVE_DIR=%DEST_DIR%\lama_installer\Archiv"
set "INNO_COMPILER=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
set "INNO_SCRIPT=C:\Users\cwebe\Desktop\_create_lama_installer\script_create_installer - includetinylatex.iss"


set /p APP_VERSION=Bitte Versionsnummer eingeben (z.B. 1.2.3): 
echo Aktuelle Version:%APP_VERSION%

echo ==============================
echo Schritt 1: L�sche dist & build
echo ==============================
if exist "%BUILD_DIR%" rd /s /q "%BUILD_DIR%"
if exist build rd /s /q build

echo ==============================
echo Schritt 2: Erstelle LaMA.exe mit PyInstaller
echo ==============================
"%PYINSTALLER_EXE%" -F -i icon_lama.ico LaMA.pyw
if errorlevel 1 (
    echo Fehler beim Erstellen der EXE.
    exit /b 1
)

echo ==============================
echo Schritt 3: Alte Installer archivieren
echo ==============================
if exist "%SETUP_PATH%" (
    for %%F in ("%SETUP_PATH%") do (
        set FILEDATE=%%~tF
    )
    :: Extrahiere aktuelles Datum für den neuen Namen
    for /f "tokens=1-3 delims=." %%a in ("%DATE%") do (
        set NEWNAME=LaMA_setup_%%c_%%b_%%a.exe
    )
    echo Umbenennen in %NEWNAME% und verschieben nach Archiv...
    ren "%SETUP_PATH%" "%NEWNAME%"
    move "%DEST_DIR%\lama_installer\%NEWNAME%" "%ARCHIVE_DIR%"
)

echo ==============================
echo Schritt 4: Kopiere neue EXE und starte Inno Setup
echo ==============================
copy /y "%BUILD_DIR%\%EXE_NAME%" "%DEST_DIR%"
if errorlevel 1 (
    echo Fehler beim Kopieren der EXE.
    exit /b 1
)

echo Starte Inno Setup Compiler...
"%INNO_COMPILER%" "/dMyAppVersion=%APP_VERSION%" "%INNO_SCRIPT%"

echo ==============================
echo Fertig!
echo ==============================
pause