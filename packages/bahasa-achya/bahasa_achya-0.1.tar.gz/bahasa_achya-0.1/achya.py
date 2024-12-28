import sys
import subprocess
import os

def transpile(input_file):
    from achya_transpiler import transpile
    output_file = os.path.splitext(input_file)[0] + '.py'
    transpile(input_file, output_file)
    print(f"File {input_file} berhasil diterjemahkan menjadi {output_file}")

def main():
    if len(sys.argv) != 2:
        print("Penggunaan: achya <namafile.al>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    if not input_file.endswith('.al'):
        print("File input harus memiliki ekstensi .al")
        sys.exit(1)
    
    transpile(input_file)
