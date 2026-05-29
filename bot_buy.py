import time
import threading
import pydirectinput

try:
    import pygetwindow as gw
    _HAS_PYGETWINDOW = True
except ImportError:
    _HAS_PYGETWINDOW = False


class BotBuy:
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
        self._focus()
        self.log("Bot de compra iniciado. Executando sequências...")

        steps = [
            ("space", 0.7),
            ("s",     0.7),
            ("enter", 0.7),
            ("enter", 0.7),
            ("enter", 0.7),
        ]

        cycle_count = 0
        while self.running:
            cycle_count += 1
            self.log(f"Executando ciclo #{cycle_count}...")
            
            for key, delay in steps:
                if not self.running:
                    return
                pydirectinput.press(key)
                if delay:
                    self._sleep(delay)

            self.log(f"Ciclo #{cycle_count} concluído.")
            
            # Aguarda 2 segundos antes de repetir
            if self.running:
                self._sleep(2.0)
