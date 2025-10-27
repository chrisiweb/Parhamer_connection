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
rm -rf build "$DIST_DIR" "$APP_NAME.spec"

# === 🐍 App mit PyInstaller erstellen ===
echo "🐍 Erstelle macOS App..."
python3 -m PyInstaller \
  --windowed \
  --name="$APP_NAME" \
  --icon="$ICON_APP" \
  --add-data="portable:portable" \
  "$PYTHON_SCRIPT"

# === 💽 DMG mit create-dmg erstellen ===
echo "💽 Erstelle DMG..."
create-dmg \
  --volname "$DMG_NAME" \
  --volicon "$ICON_DMG" \
  --window-pos 200 120 \
  --window-size 450 210 \
  --icon-size 100 \
  --icon "${APP_NAME}.app" 10 80 \
  --app-drop-link 210 80 \
  "$DIST_DIR/${DMG_NAME}.dmg" \
  "$DIST_DIR/${APP_NAME}.app"

echo "✅ Fertig! Deine DMG-Datei befindet sich hier:"
echo "➡️  $DIST_DIR/${DMG_NAME}.dmg"
