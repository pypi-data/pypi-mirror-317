import sys
import os
from colorama import Fore, Style

def generate_structure():
    """Fungsi untuk membuat struktur dasar project SPIPS."""
    directories = [
        "database",
        "models",
        "routes",
        "views",
        "static/css",
        "static/js",
    ]

    # Membuat direktori
    for dir_name in directories:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(Fore.GREEN + f"Dibuat direktori: {dir_name}" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + f"Direktori {dir_name} sudah ada." + Style.RESET_ALL)

    # Membuat file template
    with open("database/example.data.spips", "w") as f:
        f.write("# Database template\n")
        f.write("key=value\n")
    print(Fore.GREEN + "Created 'database/example.data.spips'" + Style.RESET_ALL)

    with open("models/model.py", "w") as f:
        f.write("# Model file template\n")
        f.write("class Model:\n")
        f.write("    pass\n")
    print(Fore.GREEN + "Created 'models/model.py'" + Style.RESET_ALL)

    with open("routes/routes.py", "w") as f:
        f.write("# Routes file template\n")
        f.write("def routes(app):\n")
        f.write("    pass\n")
    print(Fore.GREEN + "Created 'routes/routes.py'" + Style.RESET_ALL)

    with open("views/home.part.spips", "w") as f:
        f.write("# Home template\n")
        f.write("<h1>{#title}</h1>\n<p>{#message}</p>\n")
    print(Fore.GREEN + "Created 'views/home.part.spips'" + Style.RESET_ALL)

    with open("static/css/style.css", "w") as f:
        f.write("/* CSS Template */\nbody {\n    font-family: Arial, sans-serif;\n}\n")
    print(Fore.GREEN + "Created 'static/css/style.css'" + Style.RESET_ALL)

    with open("static/js/script.js", "w") as f:
        f.write("// JS Template\nconsole.log('SPIPS Loaded');\n")
    print(Fore.GREEN + "Created 'static/js/script.js'" + Style.RESET_ALL)

    with open("app.py", "w") as f:
        f.write("# Main application for SPIPS\n")
        f.write("from spips_framework import Spips, auto_reload\n")
        f.write("from routes.routes import routes\n")
        f.write("\n")
        f.write("app = Spips()\n")
        f.write("routes(app)\n")
        f.write("\n")
        f.write("if __name__ == '__main__':\n")
        f.write("    app.serve()\n")
    print(Fore.GREEN + "Created 'app.py'" + Style.RESET_ALL)

def version():
    """Menampilkan versi SPIPS."""
    print(Fore.CYAN + "SPIPS versi 0.2.7" + Style.RESET_ALL)

def main():
    """Fungsi utama CLI SPIPS."""
    if len(sys.argv) < 2:
        print(Fore.RED + "Gunakan perintah: spips <command>" + Style.RESET_ALL)
        return

    command = sys.argv[1].lower()
    if command == "generate":
        generate_structure()
    elif command == "version":
        version()
    else:
        print(Fore.RED + f"Perintah '{command}' tidak dikenal." + Style.RESET_ALL)

if __name__ == '__main__':
    main()