import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from colorama import Fore, Style
# Membuat custom event handler
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Hanya mencetak jika file yang dimodifikasi
        # Ada di dalam subfolder, bukan di direktori utama
        if event.is_directory:
            return  # Jangan lakukan apa-apa jika itu folder
        server = HTTPServer((host, port), RequestHandler)
        print()
        print(Fore.GREEN + "    [INFO]Spips server reload on the " + Fore.CYAN + f"http://localhost:{port}" + Style.RESET_ALL)
        print()
        print(Fore.YELLOW + "      press ctrl + c to stop the server" + Style.RESET_ALL)

        server.serve_forever()

# Inisialisasi Observer
observer = Observer()

# Tentukan direktori yang akan dipantau (root atau main.py)
path_to_watch = '.'

# Buat instance handler
event_handler = MyHandler()

# Daftarkan handler dengan observer untuk direktori root (main.py), dengan recursive=True untuk memantau semua subfolder
observer.schedule(event_handler, path_to_watch, recursive=True)

# Mulai observer
observer.start()

try:
    while True:
        time.sleep(1)  # Menjaga program berjalan
except KeyboardInterrupt:
    observer.stop()  # Hentikan observer ketika program dihentikan

observer.join()  # Tunggu observer selesai