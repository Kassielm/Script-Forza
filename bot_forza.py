import sys
import os
import time
import threading
import pyautogui
import pydirectinput

try:
    import pygetwindow as gw
    _HAS_PYGETWINDOW = True
except ImportError:
    _HAS_PYGETWINDOW = False


def _res(relative: str) -> str:
    """Resolve caminhos tanto em dev quanto no bundle PyInstaller."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative)


INITIAL_SCREEN = _res("images/initial.png")
WIN_SCREEN     = _res("images/finish_screen.png")


class BotForza:
    def __init__(self, log_callback=None):
        self.log     = log_callback or print
        self.running = False
        self._thread = None
        self._lock   = threading.Lock()

    def start(self):
        with self._lock:
            if not self.running:
                self.running = True
                self._thread = threading.Thread(target=self._loop, daemon=True)
                self._thread.start()

    def stop(self):
        self.running = False

    # ── Internals ────────────────────────────────────────────

    def _sleep(self, secs: float):
        end = time.time() + secs
        while self.running and time.time() < end:
            time.sleep(0.1)

    def _focus(self):
        if not _HAS_PYGETWINDOW:
            return
        wins = gw.getWindowsWithTitle("Forza Horizon")
        if wins:
            try:
                wins[0].activate()
                time.sleep(0.3)
            except Exception:
                pass

    def _loop(self):
        pyautogui.FAILSAFE = True
        self._focus()

        while self.running:
            pydirectinput.keyUp("w")
            self.log("Aguardando tela inicial...")

            while self.running:
                try:
                    pyautogui.locateOnScreen(INITIAL_SCREEN, confidence=0.5)
                    self.log("Tela inicial detectada.")
                    break
                except pyautogui.ImageNotFoundException:
                    pass
                self._sleep(0.5)

            if not self.running:
                break

            self.log("Iniciando corrida...")
            pydirectinput.press("enter")
            self._sleep(2)
            if not self.running:
                break

            pydirectinput.keyDown("w")
            self.log("Acelerando...")

            checks = 0
            while self.running:
                try:
                    pyautogui.locateOnScreen(WIN_SCREEN, confidence=0.6)
                    self.log("Chegada detectada. Parando.")
                    pydirectinput.keyUp("w")
                    break
                except pyautogui.ImageNotFoundException:
                    checks += 1
                    if checks % 10 == 0:
                        self.log(f"Procurando chegada... ({checks}x)")
                self._sleep(1)

            pydirectinput.keyUp("w")
            if not self.running:
                break

            self.log("Reiniciando ciclo...")
            self._sleep(4.5)
            if not self.running: break
            pydirectinput.press("x");     self._sleep(0.8)
            if not self.running: break
            pydirectinput.press("enter"); self._sleep(1)
            if not self.running: break
            pydirectinput.press("enter")

        pydirectinput.keyUp("w")
        self.log("Bot de corrida encerrado.")