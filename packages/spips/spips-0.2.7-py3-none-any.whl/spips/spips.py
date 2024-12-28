from http.server import HTTPServer, BaseHTTPRequestHandler
import re
from colorama import Fore, Style

class Spips:
    def __init__(self):
        self.routes = {}  # Menyimpan semua route dan handler-nya
        self.output = ""  # Hasil render HTML

    def route(self, path, method):
        """Dekorator untuk mendefinisikan route."""
        def decorator(func):
            self.routes[(path, method.lower())] = func
            return func
        return decorator

    def parse_template(self, template_content, **kwargs):
        """Fungsi untuk mem-parsing template menggunakan regex."""
        pattern = re.compile(r"{#(.+?)}")  # Pola untuk menangkap placeholder {#...}
        result = template_content

        for key, value in kwargs.items():
            placeholder = f"{{#{key}}}"
            result = re.sub(placeholder, str(value), result)

        return result

    def render(self, template_file, **kwargs):
        """Fungsi untuk merender template HTML."""
        try:
            with open(f"views/{template_file}.part.spips", 'r') as file:  # .part.spips template enginenya
                template_content = file.read()
            
            self.output = self.parse_template(template_content, **kwargs)
        except FileNotFoundError:
            self.output = f"<h1>Error: File '{template_file}' not found.</h1>"

    def serve(self, host='localhost', port=8000):
        """Menjalankan server HTTP."""
        class RequestHandler(BaseHTTPRequestHandler):
            def do_GET(handler_self):
                route_key = (handler_self.path, 'get')
                if route_key in self.routes:
                    self.routes[route_key]()  # Panggil handler yang sesuai
                else:
                    self.output = "<h1>404 Not Found</h1>"
                handler_self.send_response(200)
                handler_self.send_header('Content-type', 'text/html')
                handler_self.end_headers()
                handler_self.wfile.write(self.output.encode('utf-8'))

        # Jalankan server HTTP
        server = HTTPServer((host, port), RequestHandler)
        print()
        print(Fore.GREEN + "    Spips server running on the " + Fore.CYAN + f"http://localhost:{port}" + Style.RESET_ALL)
        print()
        print(Fore.YELLOW + "      ctrl + c to stop the server" + Style.RESET_ALL)

        server.serve_forever()

import os

class Model:
    @staticmethod
    def create(data, pathing):
        try:
            os.makedirs("database", exist_ok=True)  # Pastikan folder database ada
            with open(f'database/{pathing}.data.spips', 'a') as filedata:
                filedata.write(f"{data}\n")
            print(f"Data berhasil ditambahkan ke '{pathing}.data.spips'")
        except Exception as e:
            print(f"Terjadi kesalahan saat menambahkan data: {e}")

    @staticmethod
    def read(key=None, pathing=""):
        try:
            with open(f'database/{pathing}.data.spips', 'r') as filedata:
                lines = filedata.readlines()

            if key:
                result = [line.strip() for line in lines if key in line]
                if result:
                    print(f"Data ditemukan: {result}")
                else:
                    print(f"Key '{key}' tidak ditemukan.")
                return result
            else:
                print("Semua data:")
                print("".join(lines))
                return lines
        except FileNotFoundError:
            print(f"File database/{pathing}.data.spips tidak ditemukan!")
        except Exception as e:
            print(f"Terjadi kesalahan saat membaca data: {e}")

    @staticmethod
    def change(key, newdata, pathing):
        try:
            filepath = f'database/{pathing}.data.spips'
            with open(filepath, 'r') as filedata:
                lines = filedata.readlines()

            found = False
            with open(filepath, 'w') as filedata:
                for line in lines:
                    if key in line:
                        filedata.write(f"{newdata}\n")
                        found = True
                    else:
                        filedata.write(line)
            
            if found:
                print(f"Data dengan key '{key}' berhasil diubah.")
            else:
                print(f"Key '{key}' tidak ditemukan di '{pathing}.data.spips'.")
        except FileNotFoundError:
            print(f"File database/{pathing}.data.spips tidak ditemukan!")
        except Exception as e:
            print(f"Terjadi kesalahan saat mengubah data: {e}")

    @staticmethod
    def delete(key, pathing):
        try:
            filepath = f'database/{pathing}.data.spips'
            with open(filepath, 'r') as filedata:
                lines = filedata.readlines()

            found = False
            with open(filepath, 'w') as filedata:
                for line in lines:
                    if key in line:
                        found = True
                    else:
                        filedata.write(line)
            
            if found:
                print(f"Data dengan key '{key}' berhasil dihapus.")
            else:
                print(f"Key '{key}' tidak ditemukan di '{pathing}.data.spips'.")
        except FileNotFoundError:
            print(f"File database/{pathing}.data.spips tidak ditemukan!")
        except Exception as e:
            print(f"Terjadi kesalahan saat menghapus data: {e}")

    @staticmethod
    def clear(pathing):
        try:
            with open(f'database/{pathing}.data.spips', 'w') as filedata:
                pass  # Menulis ulang file kosong
            print(f"Semua data di '{pathing}.data.spips' telah dihapus.")
        except Exception as e:
            print(f"Terjadi kesalahan saat menghapus semua data: {e}")

    @staticmethod
    def count(key=None, pathing=""):
        try:
            with open(f'database/{pathing}.data.spips', 'r') as filedata:
                lines = filedata.readlines()

            if key:
                total = sum(1 for line in lines if key in line)
                print(f"Jumlah data dengan key '{key}': {total}")
            else:
                total = len(lines)
                print(f"Total jumlah data: {total}")
            return total
        except FileNotFoundError:
            print(f"File database/{pathing}.data.spips tidak ditemukan!")
        except Exception as e:
            print(f"Terjadi kesalahan saat menghitung data: {e}")

    @staticmethod
    def backup(pathing, backup_path):
        try:
            with open(f'database/{pathing}.data.spips', 'r') as source_file:
                data = source_file.read()

            with open(f'database/{backup_path}.data.spips', 'w') as backup_file:
                backup_file.write(data)

            print(f"Backup berhasil dibuat: '{backup_path}.data.spips'")
        except FileNotFoundError:
            print(f"File database/{pathing}.data.spips tidak ditemukan!")
        except Exception as e:
            print(f"Terjadi kesalahan saat membuat backup: {e}")

    @staticmethod
    def restore(backup_path, pathing):
        try:
            with open(f'database/{backup_path}.data.spips', 'r') as backup_file:
                data = backup_file.read()

            with open(f'database/{pathing}.data.spips', 'w') as target_file:
                target_file.write(data)

            print(f"File '{pathing}.data.spips' berhasil dipulihkan dari backup '{backup_path}.data.spips'.")
        except FileNotFoundError:
            print(f"File database/{backup_path}.data.spips tidak ditemukan!")
        except Exception as e:
            print(f"Terjadi kesalahan saat memulihkan file: {e}")
            
class Controller:
    def __init__(self, app):
        self.app = app  # Instance dari Spips

    def setup_routes(self):
        """Menentukan route dan handler-nya."""
        @self.app.route("/", "get")
        def home():
            # Render halaman utama
            self.app.render("home", title="Selamat Datang di Spips", message="Ini adalah framework sederhana!")

        @self.app.route("/data/add", "get")
        def add_data():
            # Tambah data ke database
            Model.create("Data baru", "example")
            self.app.render("success", message="Data berhasil ditambahkan!")

        @self.app.route("/data/view", "get")
        def view_data():
            # Tampilkan semua data dari database
            data = Model.read(pathing="example")
            self.app.render("view_data", data="\n".join(data))

        @self.app.route("/data/delete", "get")
        def delete_data():
            # Hapus data tertentu berdasarkan key
            key_to_delete = "Data baru"  # Contoh key
            Model.delete(key_to_delete, "example")
            self.app.render("success", message=f"Data dengan key '{key_to_delete}' berhasil dihapus.")

        @self.app.route("/data/clear", "get")
        def clear_data():
            # Hapus semua data
            Model.clear("example")
            self.app.render("success", message="Semua data telah dihapus!")

        @self.app.route("/data/count", "get")
        def count_data():
            # Hitung jumlah data
            total = Model.count(pathing="example")
            self.app.render("success", message=f"Jumlah total data: {total}")

        @self.app.route("/data/backup", "get")
        def backup_data():
            # Backup database
            Model.backup("example", "backup_example")
            self.app.render("success", message="Data berhasil dibackup.")

        @self.app.route("/data/restore", "get")
        def restore_data():
            # Restore dari backup
            Model.restore("backup_example", "example")
            self.app.render("success", message="Data berhasil dipulihkan dari backup.")