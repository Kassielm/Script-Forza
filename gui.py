import sys
import os
import ctypes
import threading
import keyboard
import customtkinter as ctk
from bot_forza import BotForza
from bot_buy import BotBuy


def _res(relative: str) -> str:
    """Resolve caminhos tanto em dev quanto no bundle PyInstaller.
    No onefile, arquivos embutidos ficam em sys._MEIPASS."""
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, relative)

try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Azw.forzabot")
except Exception:
    pass

# ── Tema ──────────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ACCENT   = "#00C853"
RED      = "#E53935"
BG       = "#0D1117"
BG_CARD  = "#161B22"
BG_INPUT = "#21262D"
BORDER   = "#30363D"
TEXT     = "#F0F6FC"
TEXT_DIM = "#8B949E"

# ──────────────────────────────────────────────────────────────────────────────

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Azw — Forza Bot")
        self.geometry("440x610")
        self.resizable(False, False)
        self.configure(fg_color=BG)

        self._hotkey     = "F8"
        self._bot        = None
        self._is_running = False

        self._build_ui()
        self._bind_hotkey()

        # Aplica ícone após a janela estar totalmente criada
        self.after(100, self._apply_icon)

    def _apply_icon(self):
        icon_path = _res("azw.ico")
        if not os.path.exists(icon_path):
            return
        # Barra de título
        self.iconbitmap(icon_path)
        # Barra de tarefas via WM_SETICON usando FindWindowW (mais confiável)
        try:
            LR_LOADFROMFILE = 0x0010
            IMAGE_ICON      = 1
            WM_SETICON      = 0x0080
            ICON_SMALL      = 0
            ICON_BIG        = 1
            hicon_big = ctypes.windll.user32.LoadImageW(
                None, icon_path, IMAGE_ICON, 32, 32, LR_LOADFROMFILE
            )
            hicon_small = ctypes.windll.user32.LoadImageW(
                None, icon_path, IMAGE_ICON, 16, 16, LR_LOADFROMFILE
            )
            hwnd = ctypes.windll.user32.FindWindowW(None, self.title())
            if hwnd:
                if hicon_big:
                    ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG,   hicon_big)
                if hicon_small:
                    ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon_small)
        except Exception:
            pass

    # ── Construção da UI ──────────────────────────────────────────────────────

    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=0, height=72)
        header.pack(fill="x")
        header.pack_propagate(False)

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", padx=20, pady=10)
        ctk.CTkLabel(
            title_frame, text="Azw",
            font=("Segoe UI", 30, "bold"), text_color=ACCENT
        ).pack(side="left")
        ctk.CTkLabel(
            title_frame, text="  Forza Bot",
            font=("Segoe UI", 19), text_color=TEXT_DIM
        ).pack(side="left", pady=(6, 0))

        # Body
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=24, pady=8)

        # Script
        self._section_label(body, "SCRIPT")
        self._script_var = ctk.StringVar(value="Bot de Corrida")
        self._script_combo = ctk.CTkOptionMenu(
            body,
            values=["Bot de Corrida", "Bot de Compra"],
            variable=self._script_var,
            font=("Segoe UI", 13),
            height=40,
            fg_color=BG_INPUT,
            button_color=BG_INPUT,
            button_hover_color=BG_CARD,
            dropdown_fg_color=BG_CARD,
            dropdown_hover_color=BG_INPUT,
            text_color=TEXT,
            command=self._on_script_change,
        )
        self._script_combo.pack(fill="x")

        # Hotkey
        self._section_label(body, "HOTKEY", pady_top=16)
        hk_row = ctk.CTkFrame(body, fg_color="transparent")
        hk_row.pack(fill="x")

        self._hotkey_display = ctk.CTkLabel(
            hk_row,
            text=f"  {self._hotkey}  ",
            font=("Consolas", 15, "bold"),
            fg_color=BG_INPUT,
            corner_radius=6,
            text_color=ACCENT,
            height=40,
            anchor="center",
        )
        self._hotkey_display.pack(side="left", fill="x", expand=True)

        self._change_btn = ctk.CTkButton(
            hk_row,
            text="Alterar",
            width=100,
            height=40,
            fg_color=BG_CARD,
            hover_color=BG_INPUT,
            border_color=BORDER,
            border_width=1,
            font=("Segoe UI", 12),
            text_color=TEXT_DIM,
            command=self._on_change_hotkey,
        )
        self._change_btn.pack(side="right", padx=(10, 0))

        # Botão principal
        self._toggle_btn = ctk.CTkButton(
            body,
            text="▶   INICIAR",
            height=54,
            font=("Segoe UI", 17, "bold"),
            fg_color=ACCENT,
            hover_color="#00A844",
            text_color="#000000",
            corner_radius=10,
            command=self._toggle,
        )
        self._toggle_btn.pack(fill="x", pady=(22, 6))

        # Status
        self._status_label = ctk.CTkLabel(
            body, text="● Inativo",
            font=("Segoe UI", 12), text_color=TEXT_DIM
        )
        self._status_label.pack(anchor="w")

        # Log
        self._section_label(body, "LOG", pady_top=14)
        self._log_box = ctk.CTkTextbox(
            body,
            height=175,
            font=("Consolas", 11),
            fg_color=BG_CARD,
            border_color=BORDER,
            border_width=1,
            state="disabled",
            text_color="#ADBAC7",
            scrollbar_button_color=BG_INPUT,
        )
        self._log_box.pack(fill="both", expand=True)

        # Footer
        footer = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=0, height=28)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        ctk.CTkLabel(
            footer, text="by  Azw",
            font=("Segoe UI", 10, "italic"), text_color="#444C56"
        ).pack(side="right", padx=16)

    def _section_label(self, parent, text, pady_top=8):
        ctk.CTkLabel(
            parent, text=text,
            font=("Segoe UI", 10, "bold"), text_color="#444C56"
        ).pack(anchor="w", pady=(pady_top, 3))

    # ── Controle do bot ───────────────────────────────────────────────────────

    def _toggle(self):
        if self._is_running:
            self._stop()
        else:
            self._start()

    def _start(self):
        self._is_running = True
        script = self._script_var.get()
        self._bot = (
            BotForza(self._log) if script == "Bot de Corrida" else BotBuy(self._log)
        )
        self._bot.start()

        self._toggle_btn.configure(
            text="■   PARAR", fg_color=RED, hover_color="#C62828", text_color=TEXT
        )
        self._status_label.configure(text="● Ativo", text_color=ACCENT)
        self._script_combo.configure(state="disabled")
        self._log(f"'{script}' ativado  —  [{self._hotkey}] para parar.")

    def _stop(self):
        if self._bot:
            self._bot.stop()
        self._is_running = False

        self._toggle_btn.configure(
            text="▶   INICIAR", fg_color=ACCENT, hover_color="#00A844", text_color="#000000"
        )
        self._status_label.configure(text="● Inativo", text_color=TEXT_DIM)
        self._script_combo.configure(state="normal")
        self._log("Bot desativado.")

    def _on_script_change(self, _):
        if self._is_running:
            self._stop()

    # ── Hotkey ────────────────────────────────────────────────────────────────

    def _bind_hotkey(self):
        try:
            keyboard.add_hotkey(self._hotkey, self._toggle)
        except Exception:
            pass

    def _on_change_hotkey(self):
        self._change_btn.configure(text="Pressione...", state="disabled")
        self._hotkey_display.configure(text="  ...  ", text_color=TEXT_DIM)
        threading.Thread(target=self._capture_key, daemon=True).start()

    def _capture_key(self):
        try:
            keyboard.unhook_all_hotkeys()
        except Exception:
            pass

        key = keyboard.read_key(suppress=True)
        self._hotkey = key.upper()

        def _apply():
            self._hotkey_display.configure(text=f"  {self._hotkey}  ", text_color=ACCENT)
            self._change_btn.configure(text="Alterar", state="normal")
            self._bind_hotkey()
            self._log(f"Hotkey alterada para  [{self._hotkey}].")

        self.after(0, _apply)

    # ── Log ───────────────────────────────────────────────────────────────────

    def _log(self, msg: str):
        def _write():
            self._log_box.configure(state="normal")
            self._log_box.insert("end", f"> {msg}\n")
            self._log_box.see("end")
            self._log_box.configure(state="disabled")
        self.after(0, _write)

    # ── Fechar ────────────────────────────────────────────────────────────────

    def _on_close(self):
        if self._bot:
            self._bot.stop()
        try:
            keyboard.unhook_all()
        except Exception:
            pass
        self.destroy()
        sys.exit(0)


# ──────────────────────────────────────────────────────────────────────────────

def main():
    app = App()
    app.protocol("WM_DELETE_WINDOW", app._on_close)
    app.mainloop()


if __name__ == "__main__":
    main()
