#!/bin/bash
set -e

# =========================================================
#  Build-Skript für LaMA  (Ubuntu 25.10)
# =========================================================

APP_NAME="LaMA"
MAIN_FILE="LaMA.pyw"
PORTABLE_DIR="portable"
ICON_FILE="lama_icon.png"
APP_DIR="$HOME/${APP_NAME}-App"
VENV=".venv_lama"

echo "🔧 Starte Build-Prozess für $APP_NAME ..."

# ---------------------------------------------------------
# 1. Prüfen, ob Dateien vorhanden sind
# ---------------------------------------------------------
for f in "$MAIN_FILE" "$ICON_FILE"; do
  [ -f "$f" ] || { echo "❌ $f nicht gefunden!"; exit 1; }
done
[ -d "$PORTABLE_DIR" ] || { echo "❌ Ordner $PORTABLE_DIR nicht gefunden!"; exit 1; }

# ---------------------------------------------------------
# 2. Virtuelle Umgebung erzeugen
# ---------------------------------------------------------
if [ ! -d "$VENV" ]; then
  echo "📦 Erstelle virtuelle Umgebung ($VENV)..."
  python3 -m venv "$VENV"
fi
# shellcheck disable=SC1091
source "$VENV/bin/activate"

# ---------------------------------------------------------
# 3. PyInstaller installieren
# ---------------------------------------------------------
pip install --upgrade pip
pip install pyinstaller

# ---------------------------------------------------------
# 4. PyInstaller-Build
# ---------------------------------------------------------
echo "🏗️  Erstelle ausführbare Datei..."
rm -rf build dist "${APP_NAME}.spec"
pyinstaller --onefile --noconsole "$MAIN_FILE" \
  --add-data "${PORTABLE_DIR}:${PORTABLE_DIR}" \
  --add-data "${ICON_FILE}:."

# ---------------------------------------------------------
# 5. App-Verzeichnis erstellen
# ---------------------------------------------------------
echo "📂 Kopiere Dateien nach ${APP_DIR}..."
mkdir -p "$APP_DIR"
cp "dist/${APP_NAME}" "$APP_DIR/${APP_NAME}"
cp "$ICON_FILE" "$APP_DIR/"

# ---------------------------------------------------------
# 6. Desktop-Datei erstellen
# ---------------------------------------------------------
DESKTOP_FILE="$APP_DIR/${APP_NAME}.desktop"
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=${APP_NAME}
Comment=Python-Anwendung LaMA
Exec=${APP_DIR}/${APP_NAME}
Icon=${APP_DIR}/$(basename "$ICON_FILE")
Terminal=false
Categories=Utility;
EOF
chmod +x "$DESKTOP_FILE"

# ---------------------------------------------------------
# 7. Menü-Eintrag installieren
# ---------------------------------------------------------
echo "🧩 Installiere Menü-Eintrag..."
mkdir -p "$HOME/.local/share/applications"
cp "$DESKTOP_FILE" "$HOME/.local/share/applications/${APP_NAME}.desktop"

# ---------------------------------------------------------
# 8. Aufräumen
# ---------------------------------------------------------
echo "🧹 Bereinige temporäre Dateien..."
rm -rf build dist "${APP_NAME}.spec"
deactivate

echo "✅ Fertig!"
echo "📍 App-Ordner: $APP_DIR"
echo "🚀 Starte über: Startmenü → ${APP_NAME}  oder  ${APP_DIR}/${APP_NAME}"

