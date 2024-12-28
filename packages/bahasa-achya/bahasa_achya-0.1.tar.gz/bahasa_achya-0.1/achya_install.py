import sys
import subprocess

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    if len(sys.argv) != 2:
        print("Penggunaan: achya-install <nama_paket>")
        sys.exit(1)

    package = sys.argv[1]
    install_package(package)
    print(f"Paket {package} berhasil diinstal.")
