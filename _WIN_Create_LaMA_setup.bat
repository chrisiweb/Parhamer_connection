@echo off
setlocal enabledelayedexpansion

rem ============================================================
rem  LaMA Build & Installer Automation Script (CMD-kompatibel)
rem ============================================================

rem -----------------------------
rem Einstellungen
rem -----------------------------
set "PYINSTALLER_EXE=c:\users\cwebe\appdata\roaming\python\python313\scripts\pyinstaller.exe"
set "EXE_NAME=LaMA.exe"
set "BUILD_DIR=dist"
set "DEST_DIR=C:\Users\cwebe\Desktop\_create_lama_installer"
set "SETUP_PATH=%DEST_DIR%\lama_installer\LaMA_setup.exe"
set "ARCHIVE_DIR=%DEST_DIR%\lama_installer\Archiv"
set "INNO_COMPILER=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
set "INNO_SCRIPT=C:\Users\cwebe\Desktop\_create_lama_installer\script_create_installer - includetinylatex.iss"

echo =============================================
echo   🧠  Baue LaMA.exe mit PyInstaller ...
echo =============================================

if not exist "%PYINSTALLER_EXE%" (
    echo [FEHLER] PyInstaller wurde nicht gefunden:
    echo %PYINSTALLER_EXE%
    pause
    exit /b 1
)

python "%PYINSTALLER_EXE%" -F -i icon_lama.ico LaMA.pyw
if errorlevel 1 (
    echo [FEHLER] PyInstaller-Build fehlgeschlagen!
    pause
    exit /b 1
)

echo LaMA.exe erfolgreich erstellt.
echo.

echo =============================================
echo   📁  Kopiere LaMA.exe ins Zielverzeichnis ...
echo =============================================

if not exist "%BUILD_DIR%\%EXE_NAME%" (
    echo [FEHLER] "%BUILD_DIR%\%EXE_NAME%" wurde nicht gefunden!
    pause
    exit /b 1
)

if not exist "%DEST_DIR%" (
    echo Erstelle Zielverzeichnis: "%DEST_DIR%"
    mkdir "%DEST_DIR%"
)

if exist "%DEST_DIR%\%EXE_NAME%" del /f /q "%DEST_DIR%\%EXE_NAME%"

echo Quelle: "%BUILD_DIR%\%EXE_NAME%"
echo Ziel:   "%DEST_DIR%\"
echo.

xcopy "%BUILD_DIR%\%EXE_NAME%" "%DEST_DIR%\" /Y /Q /I >nul
if errorlevel 1 (
    echo [FEHLER] Konnte EXE nicht kopieren!
    pause
    exit /b 1
)

echo EXE erfolgreich kopiert.
echo.

echo =============================================
echo   🗄️  Alte Setup-Datei archivieren ...
echo =============================================

if exist "%SETUP_PATH%" (
    echo Alte Setup-Datei gefunden: "%SETUP_PATH%"

    for %%F in ("%SETUP_PATH%") do (
        set "filedate=%%~tF"
    )

    rem Datum formatieren (JJJJ_MM_TT)
    for /f "tokens=1-3 delims=." %%a in ("!filedate:~0,10!") do (
        set "DATE_TAG=%%c_%%b_%%a"
    )

    set "ARCHIVE_NAME=LaMA_setup_!DATE_TAG!.exe"

    if not exist "%ARCHIVE_DIR%" mkdir "%ARCHIVE_DIR%"

    echo Verschiebe alte Setup-Datei nach Archiv als !ARCHIVE_NAME! ...
    move /Y "%SETUP_PATH%" "%ARCHIVE_DIR%\!ARCHIVE_NAME!" >nul
    echo Archivierung abgeschlossen.
) else (
    echo Keine alte Setup-Datei gefunden - ueberspringe Archivierung.
)
echo.


echo =============================================
echo   ⚙️  Starte Inno Setup Compiler ...
echo =============================================

echo Starte Inno Setup Compiler:
echo   Compiler: [%INNO_COMPILER%]
echo   Script:   [%INNO_SCRIPT%]
echo.

call "%INNO_COMPILER%" "%INNO_SCRIPT%"
if errorlevel 1 (
    echo [FEHLER] Inno Setup Build fehlgeschlagen!
    pause
    exit /b 1
)


rem ------------------------------------------------------------
rem 5. Fertigmeldung
rem ------------------------------------------------------------
echo =============================================
echo   Build erfolgreich abgeschlossen!
echo   Neuer Installer befindet sich in:
echo   %DEST_DIR%\lama_installer\
echo =============================================

explorer "%DEST_DIR%\lama_installer\"
exit /b 0
