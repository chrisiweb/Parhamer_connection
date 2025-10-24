import subprocess
import os
import platform
from pathlib import Path

def compile_tex_to_pdf(tex_file):
    base = Path(tex_file).with_suffix("")
    tex_path = Path(tex_file).resolve()
    workdir = tex_path.parent
    print(workdir)
    print(os.path.dirname(os.path.realpath(__file__)))
    # Betriebssystem erkennen
    system = platform.system().lower()

    # Portable Verzeichnisse
    tinytex_bin = Path("portable/tinytex/bin")
    ghost_bin = Path("portable/ghostscript/bin")

    # Passender Unterordner für TeXLive je nach OS
    if system == "windows":
        tex_bin = next(tinytex_bin.glob("win*"))
        gs_exec = next(ghost_bin.glob("gswin64c.exe"), None)
    elif system == "darwin":  # macOS
        tex_bin = next(tinytex_bin.glob("universal-darwin*"))
        gs_exec = "gs"
    else:  # Linux
        tex_bin = next(tinytex_bin.glob("x86_64-linux*"))
        gs_exec = "gs"

    env = os.environ.copy()
    env["PATH"] = f"{tex_bin}{os.pathsep}{ghost_bin}{os.pathsep}{env['PATH']}"

    print("Kompiliere:", tex_file)
    latex = os.path.join(workdir, 'portable', 'tinytex', 'bin', 'windows', 'latex.exe')

    subprocess.run([latex, tex_path.name], cwd=workdir, env=env, check=True)
    subprocess.run(["dvips", f"{base.name}.dvi"], cwd=workdir, env=env, check=True)
    subprocess.run([
        gs_exec,
        "-dBATCH", "-dNOPAUSE", "-sDEVICE=pdfwrite",
        f"-sOutputFile={base.with_suffix('.pdf').name}",
        f"{base.with_suffix('.ps').name}"
    ], cwd=workdir, env=env, check=True)

    print("PDF erfolgreich erstellt:", base.with_suffix('.pdf'))

if __name__ == "__main__":
    compile_tex_to_pdf("A.tex")
