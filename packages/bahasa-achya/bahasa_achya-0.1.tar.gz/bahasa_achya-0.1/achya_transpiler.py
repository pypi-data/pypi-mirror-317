import re
import sys
import os

translations = {
    'dan': 'and',
    'atau': 'or',
    'fungsi': 'def',
    'kalo': 'if',
    'lain': 'else',
    'kaloenggak': 'elif',
    'sbg': 'as',
    'tampilin': 'print',
    'Benar': 'True',
    'Salah': 'False',
    'impor': 'import',
    'dari': 'from',
    'kelas': 'class',
    'coba': 'try',
    'kecuali': 'except',
    'akhirnya': 'finally',
    'untuk': 'for',
    'selama': 'while',
    'berhenti': 'break',
    'lanjutkan': 'continue',
    'kembali': 'return',
    'fungsi_pendek': 'lambda',
    'dalam': 'in',
    'adalah': 'is',
    'bukan': 'not',
    'global': 'global',
    'nonlokal': 'nonlocal',
    'hapus': 'del',
    'lewatkan': 'pass',
    'pastikan': 'assert',
    'print': 'tampilin',
}

def translate_line(line):
    for key, value in translations.items():
        line = re.sub(r'\b' + key + r'\b', value, line)
    return line

def transpile(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    translated_lines = [translate_line(line) for line in lines]

    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(translated_lines)

    print(f"File {input_file} telah berhasil diterjemahkan menjadi {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Penggunaan: python achya_transpiler.py <namafile.al>")
        sys.exit(1)

    input_file = sys.argv[1]

    if not input_file.endswith('.al'):
        print("File input harus memiliki ekstensi .al")
        sys.exit(1)

    output_file = os.path.splitext(input_file)[0] + '.py'
    transpile(input_file, output_file)
