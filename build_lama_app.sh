#!/bin/bash
set -e

# =========================================================
#  Build-Skript für LaMA als AppImage mit zsync-Update-Support
#  Kompatibel mit Ubuntu 20.04–25.10
# =========================================================

APP_NAME="LaMA"
MAIN_FILE="LaMA.pyw"
PORTABLE_DIR="portable"
ICON_FILE="lama_icon.png"
APPDIR="LaMA.AppDir"
VENV="venv_lama"
OUTPUT="${APP_NAME}.AppImage"
UPDATE_URL="gh-releases-zsync|mylama|lama|latest|${OUTPUT}.zsync"  # 🔁 GitHub-Update-Link

echo "🔧 Starte AppImage-Build für $APP_NAME ..."

# ---------------------------------------------------------
# 1. Vorprüfungen
# ---------------------------------------------------------
for f in "$MAIN_FILE" "$ICON_FILE"; do
  [ -f "$f" ] || { echo "❌ $f nicht gefunden!"; exit 1; }
done
[ -d "$PORTABLE_DIR" ] || { echo "❌ Ordner $PORTABLE_DIR nicht gefunden!"; exit 1; }

# ---------------------------------------------------------
# 2. Prüfe auf FUSE (AppImage braucht libfuse2)
# ---------------------------------------------------------
if ! ldconfig -p | grep -q libfuse.so.2; then
  echo "⚙️  Installiere libfuse2 ..."
  sudo apt update
  sudo apt install -y libfuse2 || echo "⚠️  libfuse2 konnte nicht installiert werden – eventuell ist fuse3 bereits vorhanden."
fi

# ---------------------------------------------------------
# 3. Virtuelle Umgebung (mit allen Abhängigkeiten)
# ---------------------------------------------------------
if [ ! -d "$VENV" ]; then
  echo "📦 Erstelle virtuelle Umgebung ..."
  python3 -m venv "$VENV"
fi
source "$VENV/bin/activate"

pip install --upgrade pip
pip install pyqt5 pyyaml pillow dulwich==0.22.8 bcrypt tinydb requests sympy setuptools

deactivate

# ---------------------------------------------------------
# 4. appimagetool sicherstellen
# ---------------------------------------------------------
if ! command -v appimagetool &>/dev/null; then
  echo "⚙️  Lade appimagetool herunter ..."
  mkdir -p ~/tools
  cd ~/tools
  wget -q https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage -O appimagetool
  chmod +x appimagetool
  cd - >/dev/null
  export PATH="$HOME/tools:$PATH"
fi

# ---------------------------------------------------------
# 5. AppDir-Struktur aufbauen
# ---------------------------------------------------------
echo "📂 Erstelle AppDir ..."
rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin"
mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"

cp "$MAIN_FILE" "$APPDIR/usr/bin/"
cp -r $PORTABLE_DIR "$APPDIR/usr/bin/"
cp -r *.py "$APPDIR/usr/bin/"
cp -r "$VENV" "$APPDIR/usr/bin/"
cp "$ICON_FILE" "$APPDIR/${APP_NAME}.png"
cp "$ICON_FILE" "$APPDIR/usr/share/icons/hicolor/256x256/apps/${APP_NAME}.png"

# ---------------------------------------------------------
# 6. AppRun erzeugen
# ---------------------------------------------------------
cat > "$APPDIR/AppRun" <<'EOF'
#!/bin/bash
HERE="$(dirname "$(readlink -f "$0")")"
export PATH="$HERE/usr/bin/venv_lama/bin:$PATH"
export PYTHONPATH="$HERE/usr/bin"
cd "$HERE/usr/bin"
exec python3 LaMA.pyw "$@"
EOF
chmod +x "$APPDIR/AppRun"

# ---------------------------------------------------------
# 7. Desktop-Datei erzeugen
# ---------------------------------------------------------
cat > "$APPDIR/${APP_NAME}.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=${APP_NAME}
Comment=Python-Anwendung LaMA
Exec=${APP_NAME}
Icon=${APP_NAME}
Categories=Utility;
Terminal=false
EOF

# ---------------------------------------------------------
# 8. AppImage erzeugen (mit zsync-Metadaten)
# ---------------------------------------------------------
ARCH=$(uname -m)
echo "🏗️  Erzeuge AppImage mit zsync-Updateinfo (${ARCH}) ..."
ARCH=$ARCH appimagetool \
  --updateinformation "${UPDATE_URL}" \
  "$APPDIR" \
  "${OUTPUT}"

# ---------------------------------------------------------
# 9. .zsync-Datei erzeugen
# ---------------------------------------------------------
if ! command -v zsyncmake &>/dev/null; then
  echo "⚙️  Installiere zsync ..."
  sudo apt install -y zsync
fi

echo "🔁 Erzeuge .zsync-Datei ..."
zsyncmake "${OUTPUT}"

# ---------------------------------------------------------
# 10. Fertig 🎉
# ---------------------------------------------------------
echo "✅ Fertig! AppImage wurde erstellt:"
ls -lh "${OUTPUT}" "${OUTPUT}.zsync"
echo
echo "📦 AppImage: ${OUTPUT}"
echo "🔄 Update-Datei: ${OUTPUT}.zsync"
echo
echo "🌍 Lade beide Dateien hoch nach GitHub Releases:"
echo "    https://github.com/mylama/lama/releases/latest"
echo
echo "💡 Nutzer können das AppImage aktualisieren mit:"
echo "    AppImageUpdate ${OUTPUT}"

