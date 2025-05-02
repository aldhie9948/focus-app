import subprocess
import re
import time

def get_list_windows():
    try:
        result = subprocess.run(["wmctrl", "-l"], capture_output=True, text=True, check=True)
        windows = []
        lines = result.stdout.strip().split("\n")
        for line in lines:
            parts = line.split(None, 3)
            if len(parts) == 4:
                win_id, _, _, title = parts
                windows.append((win_id, title))
        return windows
    except Exception as e:
        print(f"Error mengambil daftar window: {e}")
        return []

def get_active_window_id():
    try:
        result = subprocess.run(["xdotool", "getactivewindow"], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"Gagal menjadi window aktif: {e}")
        return None

def get_idle_time_ms() :
    try:
        result = subprocess.run(["xprintidle"], capture_output=True, text=True)
        idle = result.stdout.split()[0] or "0"
        return int(idle)
    except Exception as e:
        print(f"Gagal mengambil idle time: {e}")

def focus_window(win_id: int):
    try:   
        subprocess.run(["wmctrl", "-i", "-a", win_id])
        print(f"Memfokuskan window ID: {win_id}")
    except Exception as e:
        print(f"Gagal memfokuskan window: {e}")

def focus_if_idle(pattern:str, idle_threshold_ms=5000):
    windows = get_list_windows()
    try:
        regex = re.compile(pattern, re.IGNORECASE)
    except re.error as e:
        print(f"Regex tidak valid: {e}")
        return 
    
    for win_id, title in windows:
        if regex.search(title):
            current_active = get_active_window_id()
            if current_active and win_id.lower() != current_active.lower():
                idle_time = get_idle_time_ms()
                if idle_time is not None and idle_time >= idle_threshold_ms:
                    print(f"Idle selama {idle_time} ms. Window '{title}' cocok dan tidak aktif.")
                    focus_window(win_id)
                else:
                    print(f"Idle belum cukup lama ({idle_time}) ms.")
            else:
                print(f"Window {title} sudah aktif.")
            break

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        pattern = ' '.join(sys.argv[1:])
        while True:
            focus_if_idle(pattern)
            time.sleep(1)
    else:
        print("Gunakan: python focus_if_idle.py <regex pattern window>")