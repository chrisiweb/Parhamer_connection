@echo off
setlocal

:: ==============================
:: Variablen
:: ==============================
set "PYINSTALLER_EXE=C:\Users\cwebe\AppData\Local\Programs\Python\Python312\Scripts\pyinstaller.exe"
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
