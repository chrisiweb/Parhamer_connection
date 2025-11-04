import os
import shutil
import subprocess
import sys
import re
import time
from datetime import datetime
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, TimeElapsedColumn

console = Console()

# ------------------------------------------------------------
# Einstellungen
# ------------------------------------------------------------
PYINSTALLER_EXE = r"c:\users\cwebe\appdata\roaming\python\python313\scripts\pyinstaller.exe"
EXE_NAME = "LaMA.exe"
BUILD_DIR = "dist"
DEST_DIR = r"C:\Users\cwebe\Desktop\_create_lama_installer"
SETUP_PATH = os.path.join(DEST_DIR, r"lama_installer\LaMA_setup.exe")
ARCHIVE_DIR = os.path.join(DEST_DIR, r"lama_installer\Archiv")
INNO_COMPILER = r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
INNO_SCRIPT = r"C:\Users\cwebe\Desktop\_create_lama_installer\script_create_installer - includetinylatex.iss"

# ------------------------------------------------------------
# Hilfsfunktionen
# ------------------------------------------------------------
def section(title: str):
    console.print(f"\n[bold cyan]{'='*70}[/]")
    console.print(f"[bold yellow]{title}[/]")
    console.print(f"[bold cyan]{'='*70}[/]\n")

def safe_copy(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst):
        os.remove(dst)
    shutil.copy2(src, dst)

def run_process_with_progress(cmd, title="Prozess läuft", detect_pattern=None):
    """
    Führt Subprozess aus und zeigt Fortschritt mit rich an.
    detect_pattern – Regex mit (current, total)
    """
    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        transient=True,
        console=console,
    ) as progress:
        task = progress.add_task(title, total=100)
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="ignore")
        total = 0
        current = 0
        for line in iter(process.stdout.readline, ""):
            line = line.strip()
            if detect_pattern:
                m = re.search(detect_pattern, line)
                if m:
                    try:
                        current = int(m.group(1))
                        total = int(m.group(2))
                        percent = int((current / total) * 100)
                        progress.update(task, completed=percent)
                    except Exception:
                        pass
            else:
                # Keine echte Prozentbasis: Simuliere Fortschritt
                current += 1
                if current <= 100:
                    progress.update(task, completed=current)
            # Wichtige Zeilen im Terminal ausgeben
            if any(k in line.lower() for k in ["error", "warn", "compile", "building"]):
                console.print(f"[dim]{line}[/]")
        process.wait()
        progress.update(task, completed=100)
        if process.returncode != 0:
            console.print(f"[bold red]❌ Fehler beim Prozess:[/] {cmd[0]}")
            sys.exit(1)

# ------------------------------------------------------------
# 1️⃣ Baue LaMA.exe mit PyInstaller
# ------------------------------------------------------------
section("🧠  Baue LaMA.exe mit PyInstaller")

if not os.path.exists(PYINSTALLER_EXE):
    console.print(f"[bold red]PyInstaller nicht gefunden:[/] {PYINSTALLER_EXE}")
    sys.exit(1)

cmd = ["python", PYINSTALLER_EXE, "-F", "-i", "icon_lama.ico", "LaMA.pyw"]
console.print("[green]Starte PyInstaller...[/]")
run_process_with_progress(cmd, title="PyInstaller", detect_pattern=None)
console.print("[bold green]✅ LaMA.exe erfolgreich erstellt.[/]\n")

# ------------------------------------------------------------
# 2️⃣ Kopiere LaMA.exe ins Zielverzeichnis
# ------------------------------------------------------------
section("📁  Kopiere LaMA.exe ins Zielverzeichnis")

src_exe = os.path.join(BUILD_DIR, EXE_NAME)
dst_exe = os.path.join(DEST_DIR, EXE_NAME)
if not os.path.exists(src_exe):
    console.print(f"[bold red]FEHLER:[/] {src_exe} wurde nicht gefunden!")
    sys.exit(1)

safe_copy(src_exe, dst_exe)
console.print("[bold green]✅ EXE erfolgreich kopiert.[/]\n")

# ------------------------------------------------------------
# 3️⃣ Alte Setup-Datei archivieren
# ------------------------------------------------------------
section("🗄️  Alte Setup-Datei archivieren")

if os.path.exists(SETUP_PATH):
    date_str = datetime.fromtimestamp(os.path.getmtime(SETUP_PATH)).strftime("%Y_%m_%d")
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    archive_name = f"LaMA_setup_{date_str}.exe"
    dst_archive = os.path.join(ARCHIVE_DIR, archive_name)
    console.print(f"Verschiebe alte Setup-Datei nach Archiv als [bold]{archive_name}[/] ...")
    shutil.move(SETUP_PATH, dst_archive)
    console.print("[green]Archivierung abgeschlossen.[/]")
else:
    console.print("[yellow]Keine alte Setup-Datei gefunden – überspringe Archivierung.[/]")
time.sleep(0.5)

# ------------------------------------------------------------
# 4️⃣ Neues Setup mit Inno Setup bauen
# ------------------------------------------------------------
section("⚙️  Starte Inno Setup Compiler")

if not os.path.exists(INNO_COMPILER):
    console.print(f"[bold red]FEHLER:[/] Inno Setup Compiler wurde nicht gefunden:\n{INNO_COMPILER}")
    sys.exit(1)
if not os.path.exists(INNO_SCRIPT):
    console.print(f"[bold red]FEHLER:[/] Inno Setup Script nicht gefunden:\n{INNO_SCRIPT}")
    sys.exit(1)

console.print(f"[cyan]Starte Inno Setup Compiler:[/]\n{INNO_COMPILER}\n{INNO_SCRIPT}\n")

# Nutze /Qp → Fortschrittsausgabe in Prozent
run_process_with_progress(
    [INNO_COMPILER, "/Qp", INNO_SCRIPT],
    title="Inno Setup",
    detect_pattern=r"Progress:\s*(\d+)%"
)

console.print("[bold green]✅ Neuer Installer erfolgreich erstellt.[/]\n")

# ------------------------------------------------------------
# 5️⃣ Fertigmeldung
# ------------------------------------------------------------
section("🎉  Build erfolgreich abgeschlossen!")
console.print(f"[bold]Neuer Installer befindet sich in:[/]\n{os.path.join(DEST_DIR, 'lama_installer')}")
time.sleep(1)

# Explorer öffnen
try:
    os.startfile(os.path.join(DEST_DIR, "lama_installer"))
except Exception:
    console.print("[yellow]Konnte Explorer nicht öffnen.[/]")
