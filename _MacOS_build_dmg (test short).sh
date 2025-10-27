#!/bin/bash
set -e

# === 🏗️ Einstellungen ===
APP_NAME="LaMA"
ICON_APP="icon_lama.icns"
ICON_DMG="icon_lama_installer.icns"
PYTHON_SCRIPT="LaMA.pyw"
DMG_NAME="${APP_NAME}_setup"
DIST_DIR="dist"

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
