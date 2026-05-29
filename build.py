"""
Build script — gera Azw Forza Bot.exe com privilégios de administrador.

Pré-requisitos:
    pip install pyinstaller customtkinter pyautogui pydirectinput keyboard pygetwindow

Uso:
    python build.py
"""

import subprocess
import sys
import os

APP_NAME = "Azw Forza Bot"
ENTRY    = "gui.py"

ICON = "Azw.ico"

cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile",
    "--windowed",
    "--uac-admin",                       # Solicita elevação UAC no Windows
    "--collect-data", "customtkinter",   # Inclui temas e assets do customtkinter
    "--add-data", "images;images",       # Copia a pasta images para o bundle
    "--name", APP_NAME,
    "--clean",
    ENTRY,
]

if os.path.exists(ICON):
    cmd += ["--icon", ICON,             # Ícone do .exe e da barra de tarefas
            "--add-data", f"{ICON};."]  # Embute o .ico para uso em runtime

print("=" * 52)
print(f"  Construindo:  {APP_NAME}.exe")
print("=" * 52)

result = subprocess.run(cmd)

if result.returncode == 0:
    exe_path = os.path.join("dist", f"{APP_NAME}.exe")
    print()
    print("Build concluído com sucesso!")
    print(f"  → {os.path.abspath(exe_path)}")
else:
    print()
    print("Erro durante o build. Verifique os logs acima.")
    sys.exit(1)
