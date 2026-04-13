#!/bin/bash
set -e

# === 🏗️ Einstellungen ===
APP_NAME="LaMA"
ICON_APP="icon_lama.icns"
ICON_DMG="icon_lama_installer.icns"
PYTHON_SCRIPT="LaMA.pyw"
DMG_NAME="${APP_NAME}_setup"
DIST_DIR="dist"

# === 🧹 Vorherige Builds löschen ===
echo "🧹 Entferne alte Build-Dateien..."
# Entfernt alle Schutzattribute
rm -rf build "$DIST_DIR" "$APP_NAME.spec"

echo "📦 Erstelle macOS-spezifischen portable-Ordner..."
rm -rf portable_mac
mkdir -p portable_mac/tinytex/bin
mkdir -p portable_mac/ghostscript

# ✅ 1. Gesamten portable Ordner kopieren
cp -R portable/* portable_mac/

# ✅ 2. Bin-Verzeichnis bereinigen → nur universal-darwin behalten
rm -rf portable_mac/tinytex/bin/windows
rm -rf portable_mac/tinytex/bin/x86_64-linux

echo "✅ Fertig! portable_mac enthält nur die macOS-Binaries."

echo "🐍 Baue macOS App..."
python3 -m PyInstaller \
  --windowed \
  --name="$APP_NAME" \
  --icon="$ICON_APP" \
  --add-data="portable_mac:portable" \
  "$PYTHON_SCRIPT"

echo "🧹 Bereinige temporäre Dateien..."
rm -rf portable_mac

echo "✅ macOS Build abgeschlossen!"

# === 🔏 App lokal signieren (ad-hoc) ===
echo "🔏 Entferne .DS_Store-Dateien..."
find "$DIST_DIR/${APP_NAME}.app" -name ".DS_Store" -delete

echo "🔏 Signiere App..."
codesign --force --deep --sign - "$DIST_DIR/${APP_NAME}.app"

echo "🧹 Entferne Quarantäne-Attribute..."
xattr -cr "$DIST_DIR/${APP_NAME}.app"

# === 💽 DMG mit create-dmg erstellen ===
echo "💽 Erstelle DMG..."
create-dmg \
  --volname "$DMG_NAME" \
  --volicon "$ICON_DMG" \
  --background "bg_mac_installer.png" \
  --window-pos 200 120 \
  --window-size 500 300 \
  --icon-size 100 \
  --icon "${APP_NAME}.app" 10 160 \
  --app-drop-link 280 160 \
  "$DIST_DIR/${DMG_NAME}.dmg" \
  "$DIST_DIR/${APP_NAME}.app"

echo "✅ Fertig! Deine DMG-Datei befindet sich hier:"
echo "➡️  $DIST_DIR/${DMG_NAME}.dmg"
