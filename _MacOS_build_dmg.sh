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

# === 🎨 Icon zur DMG hinzufügen ===
echo "🎨 Füge Icon zur DMG hinzu..."
cd "$(dirname "$0")"

# Schreibbare Kopie erzeugen
hdiutil convert "$DIST_DIR/${DMG_NAME}.dmg" -format UDRW -o "$DIST_DIR/${DMG_NAME}_rw.dmg"

# Icon anwenden
sips -i "$ICON_DMG"
DeRez -only icns "$ICON_DMG" > /tmp/tmpicns.rsrc
Rez -append /tmp/tmpicns.rsrc -o "$DIST_DIR/${DMG_NAME}_rw.dmg"
SetFile -a C "$DIST_DIR/${DMG_NAME}_rw.dmg"
rm /tmp/tmpicns.rsrc

# Zurückkonvertieren in finale DMG
hdiutil convert "$DIST_DIR/${DMG_NAME}_rw.dmg" -format UDZO -imagekey zlib-level=9 -o "$DIST_DIR/${DMG_NAME}_final.dmg"

# Aufräumen & umbenennen
rm "$DIST_DIR/${DMG_NAME}_rw.dmg"
mv "$DIST_DIR/${DMG_NAME}_final.dmg" "$DIST_DIR/${DMG_NAME}.dmg"

echo "✅ Fertig! Deine DMG-Datei befindet sich hier:"
echo "➡️  $DIST_DIR/${DMG_NAME}.dmg"
