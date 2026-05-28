import pyautogui
import pydirectinput
import keyboard
import threading
import time
import sys

try:
    import pygetwindow as gw
    HAS_PYGETWINDOW = True
except ImportError:
    HAS_PYGETWINDOW = False

# --- Configurações ---
TOGGLE_KEY = 'F8'
INITIAL_SCREEN_IMG = './images/initial.png'
WIN_SCREEN_IMG = './images/finish_screen.png'

# --- Estado do bot ---
running = False
bot_thread = None
lock = threading.Lock()


def interruptible_sleep(seconds):
    """Sleep que pode ser interrompido pelo F8"""
    end_time = time.time() + seconds
    while running and time.time() < end_time:
        time.sleep(0.1)


def focus_forza():
    if not HAS_PYGETWINDOW:
        return
    windows = gw.getWindowsWithTitle('Forza Horizon 6')
    if windows:
        try:
            windows[0].activate()
            time.sleep(0.5)
        except Exception:
            pass


def bot_loop():
    global running
    pyautogui.FAILSAFE = True

    while running:
        # Aguarda tela inicial
        pydirectinput.keyUp('w')
        print("Aguardando tela inicial...")
        while running:
            try:
                pyautogui.locateOnScreen(INITIAL_SCREEN_IMG, confidence=0.5)
                print("Tela inicial detectada. Iniciando corrida.")
                break
            except pyautogui.ImageNotFoundException:
                pass
            interruptible_sleep(0.5)

        if not running:
            break

        # Inicia a corrida
        print("Iniciando corrida...")
        pydirectinput.press('enter')
        interruptible_sleep(2)
        
        if not running:
            break
            
        pydirectinput.keyDown('w')
        print("Acelerando...")

        # Aguarda linha de chegada
        check_count = 0
        while running:
            try:
                pyautogui.locateOnScreen(WIN_SCREEN_IMG, confidence=0.6)
                print("Chegada detectada. Parando o carro.")
                pydirectinput.keyUp('w')
                break
            except pyautogui.ImageNotFoundException:
                check_count += 1
                if check_count % 10 == 0:  # Print a cada 10 tentativas (~10 segundos)
                    print(f"Procurando linha de chegada... ({check_count} verificações)")
            interruptible_sleep(1)

        # Garante que a tecla W seja solta em qualquer situação
        pydirectinput.keyUp('w')

        if not running:
            print("Bot desativado. Encerrando...")
            break

        # Reinicia a corrida
        print("Reiniciando ciclo...")
        interruptible_sleep(4.5)
        
        if not running:
            break
            
        pydirectinput.press('x')
        interruptible_sleep(0.8)
        
        if not running:
            break
            
        pydirectinput.press('enter')
        interruptible_sleep(1)
        
        if not running:
            break
            
        pydirectinput.press('enter')

    print("Bot parado.")
    pydirectinput.keyUp('w')

def toggle_bot():
    global running, bot_thread
    with lock:
        if not running:
            running = True
            focus_forza()
            bot_thread = threading.Thread(target=bot_loop, daemon=True)
            bot_thread.start()
            print(f"[{TOGGLE_KEY}] Bot ATIVADO.")
        else:
            running = False
            print(f"[{TOGGLE_KEY}] Bot DESATIVADO.")


def main():
    print("Bot Forza Horizon pronto.")
    print(f"  {TOGGLE_KEY}  → ativar/desativar o bot")
    print("  Ctrl+C → encerrar o programa")

    keyboard.add_hotkey(TOGGLE_KEY, toggle_bot)

    try:
        keyboard.wait()
    except KeyboardInterrupt:
        global running
        running = False
        print("\nEncerrando...")
        sys.exit(0)


if __name__ == '__main__':
    main()