import hashlib
import sys
import shutil
import os, time
import zipfile
from cryptography.fernet import Fernet
from fpdf import FPDF
from prettytable import PrettyTable
from datetime import datetime


def calculate_hash(file_path, hash_type):
    hash_func = None
    if hash_type.lower() == 'md5':
        hash_func = hashlib.md5()
    elif hash_type.lower() == 'sha512':
        hash_func = hashlib.sha512()
    else:
        raise ValueError("Tipe hash tidak valid. Gunakan 'md5' atau 'sha512'.")
    try:
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                hash_func.update(data)
    except FileNotFoundError:
        print(f"File '{file_path}' tidak ditemukan.")
        return None
    except IOError as e:
        print(f"Terjadi kesalahan saat membaca file: {e}")
        return None
    return hash_func.hexdigest()


def copy_file_and_check_hash(source_path, destination_path, hash_type, original_hash_value):
    try:
        print(f"========= Case 1️⃣  - Copy file {source_path} =========")
        if not os.path.isfile(source_path):
            print(f"File sumber '{source_path}' tidak ditemukan.")
            return False
        shutil.copy2(source_path, destination_path)
        print(f"Menyalin file '{source_path}' menjadi '{destination_path}'")
        copied_file_hash = calculate_hash(destination_path, hash_type)
        if copied_file_hash is not None:
            print(f"Nilai hash {destination_path} ({hash_type.upper()}): \n↳ 🔑 {copied_file_hash}")
            print(f"↳ {'✅ NILAI HASH TIDAK BERUBAH' if original_hash_value == copied_file_hash else '❗️ NILAI HASH BERUBAH'}\n")
            mac = show_mac(destination_path)
            new_data_table = {"action": "Copy file ke dir sama", "hash_value": copied_file_hash, "status_change": f"{'✅ TIDAK BERUBAH' if original_hash_value == copied_file_hash else '❗️ BERUBAH'}", "mac": mac}
            data_result_table.append(new_data_table)
            time.sleep(3)
            shutil.copy2(source_path, "tes_folder_copy/"+destination_path)
            print(f"Menyalin file {source_path} menjadi tes_folder_copy/{destination_path}")
            copied_file_hash = calculate_hash("tes_folder_copy/"+destination_path, hash_type)
            mac = show_mac("tes_folder_copy/"+destination_path)
            new_data_table = {"action": "Copy file ke dir berbeda", "hash_value": copied_file_hash, "status_change": f"{'✅ TIDAK BERUBAH' if original_hash_value == copied_file_hash else '❗️ BERUBAH'}", "mac": mac}
            data_result_table.append(new_data_table)
            return True
        else:
            return False
    except IOError as e:
        print(f"Terjadi kesalahan saat mengcopy file: {e}")
        return False
    except Exception as e:
        print(f"Kesalahan: {e}")
        return False

def append_delete_text(source_path, destination_path, hash_type, original_hash_value):
    print(f"========= Case 2️⃣  - Mengubah konten {source_path} =========")
    shutil.copy2(source_path, 'add_line_'+source_path)
    shutil.copy2(source_path, 'remove_line_'+source_path)
    print(f"(1) Menambah text")
    with open('add_line_'+source_path, 'a') as f:
        f.write(f"\ntambah line baru")
    result_hash = calculate_hash('add_line_'+source_path, hash_type)
    if result_hash is not None:
        print(f"Nilai hash setelah Menambah text ({hash_type.upper()}): \n↳ 🔑 {result_hash}")
        print(f"↳ {'✅ NILAI HASH TIDAK BERUBAH' if original_hash_value == result_hash else '❗️ NILAI HASH BERUBAH'}\n")
        mac = show_mac('add_line_'+source_path)
        new_data_table = {"action": "Menambah konten", "hash_value": result_hash, "status_change": f"{'✅ TIDAK BERUBAH' if original_hash_value == result_hash else '❗️ BERUBAH'}", "mac": mac}
        data_result_table.append(new_data_table)
    time.sleep(2)
    with open('remove_line_'+source_path, 'r+') as f:
        lines = f.readlines()
        if len(lines) > 0:
            f.seek(0)
            f.writelines(lines[:-1])
            f.truncate()
            print(f"(2) Menghapus text")
        else:
            print(f"Gagal menghapus text")
    result_hash2 = calculate_hash('remove_line_'+source_path, hash_type)
    if result_hash2 is not None:
        print(f"Nilai hash setelah menghapus text ({hash_type.upper()}): \n↳ 🔑 {result_hash2}")
        print(f"↳ {'✅ NILAI HASH TIDAK BERUBAH' if original_hash_value == result_hash2 else '❗️ NILAI HASH BERUBAH'}\n")
        mac = show_mac('remove_line_'+source_path)
        new_data_table = {"action": "Menghapus konten", "hash_value": result_hash2, "status_change": f"{'✅ TIDAK BERUBAH' if original_hash_value == result_hash2 else '❗️ BERUBAH'}", "mac": mac}
        data_result_table.append(new_data_table)
    

def rename_file(source_path, destination_path, hash_type, original_hash_value):
    print(f"========= Case 3️⃣  - Mengubah nama file {source_path} =========")
    shutil.copy2(source_path, 'rename_file_'+source_path)
    if os.path.exists('rename_file_'+source_path):
        os.rename('rename_file_'+source_path, '2_rename_file_'+source_path)
        result_hash = calculate_hash('2_rename_file_'+source_path, hash_type)
        if result_hash is not None:
            print(f"Nilai hash setelah mengubah nama file ({hash_type.upper()}): \n↳ 🔑 {result_hash}")
            print(f"↳ {'✅ NILAI HASH TIDAK BERUBAH' if original_hash_value == result_hash else '❗️ NILAI HASH BERUBAH'}\n")
            mac = show_mac('2_rename_file_'+source_path)
            new_data_table = {"action": "Mengubah nama file", "hash_value": result_hash, "status_change": f"{'✅ TIDAK BERUBAH' if original_hash_value == result_hash else '❗️ BERUBAH'}", "mac": mac}
            data_result_table.append(new_data_table)
    else:
        print(f"File {'rename_file_'+source_path} does not exist.")

def change_ext_file(source_path, destination_path, hash_type, original_hash_value):
    print(f"========= Case 4️⃣  - Mengubah ekstensi file {source_path} =========")
    shutil.copy2(source_path, 'change_ext_file_'+source_path)
    shutil.copy2(source_path, 'change_ext_file2_'+source_path)
    if os.path.exists('change_ext_file_'+source_path):
        base = os.path.splitext('change_ext_file_'+source_path)[0]
        new_file = base + '.pdf'
        os.rename('change_ext_file_'+source_path, new_file)
        print(f"Mengubah ekstensi {os.path.splitext('change_ext_file_'+source_path)[1]} ke .pdf")
        result_hash = calculate_hash(new_file, hash_type)
        if result_hash is not None:
            print(f"Nilai hash setelah mengubah ekstensi file ({hash_type.upper()}): \n↳ 🔑 {result_hash}")
            print(f"↳ {'✅ NILAI HASH TIDAK BERUBAH' if original_hash_value == result_hash else '❗️ NILAI HASH BERUBAH'}\n")
        mac = show_mac(new_file)
        new_data_table = {"action": "Mengubah ekstensi file txt ke pdf", "hash_value": result_hash, "status_change": f"{'✅ TIDAK BERUBAH' if original_hash_value == result_hash else '❗️ BERUBAH'}", "mac": mac}
        data_result_table.append(new_data_table)
        if os.path.splitext(source_path)[1] == 'txt':
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            with open('change_ext_file2_'+source_path, 'r') as file:
                for line in file:
                    pdf.cell(200, 10, txt=line.encode('latin-1', 'replace').decode('latin-1'), ln=True)
            pdf.output('hasil_export_txt_ke_pdf.pdf')
            print(f"Export ekstensi {os.path.splitext('change_ext_file2_'+source_path)[1]} ke .pdf")
            result_hash = calculate_hash('hasil_export_txt_ke_pdf.pdf', hash_type)
            if result_hash is not None:
                print(f"Nilai hash setelah export file {os.path.splitext('change_ext_file2_'+source_path)[1]} ke .pdf ({hash_type.upper()}): \n↳ 🔑 {result_hash}")
                print(f"↳ {'✅ NILAI HASH TIDAK BERUBAH' if original_hash_value == result_hash else '❗️ NILAI HASH BERUBAH'}\n")
            mac = show_mac('hasil_export_txt_ke_pdf.pdf')
            new_data_table = {"action": "Mengeksport file txt ke pdf", "hash_value": result_hash, "status_change": f"{'✅ TIDAK BERUBAH' if original_hash_value == result_hash else '❗️ BERUBAH'}", "mac": mac}
            data_result_table.append(new_data_table)
    else:
        print(f"File {'change_ext_file_'+source_path} does not exist.")

def change_file_metadata(source_path, destination_path, hash_type, original_hash_value):
    print(f"========= Case 5️⃣  - Mengubah metadata file {source_path} =========")
    shutil.copy2(source_path, 'change_meta_file_'+source_path)
    print(f"Metadata waktu terakhir akses: {time.ctime(os.stat('change_meta_file_'+source_path).st_atime)}")
    new_access_time = time.time() - 100000
    new_modified_time = time.time() - 500000000
    os.utime('change_meta_file_'+source_path, (new_access_time, new_modified_time))
    print(f"Metadata waktu terakhir akses (setelah dirubah): {time.ctime(os.stat('change_meta_file_'+source_path).st_atime)}")
    result_hash = calculate_hash('change_meta_file_'+source_path, hash_type)
    if result_hash is not None:
        print(f"Nilai hash setelah mengubah metadata file ({hash_type.upper()}): \n↳ 🔑 {result_hash}")
        print(f"↳ {'✅ NILAI HASH TIDAK BERUBAH' if original_hash_value == result_hash else '❗️ NILAI HASH BERUBAH'}\n")
    mac = show_mac('change_meta_file_'+source_path)
    new_data_table = {"action": "Mengubah metadata file", "hash_value": result_hash, "status_change": f"{'✅ TIDAK BERUBAH' if original_hash_value == result_hash else '❗️ BERUBAH'}", "mac": mac}
    data_result_table.append(new_data_table)

def compress_to_zip(source_path, destination_path, hash_type, original_hash_value):
    print(f"========= Case 6️⃣  - Kompresi dan Ekstraksi file {source_path} ke ZIP =========")
    shutil.copy2(source_path, 'compress_file_zip_'+source_path)
    with zipfile.ZipFile('output_compress_zip_file.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Jika source adalah file
        if os.path.isfile('compress_file_zip_'+source_path):
            zipf.write('compress_file_zip_'+source_path, os.path.basename('compress_file_zip_'+source_path))
            print(f"(1) Kompresi file ke ZIP")
            result_hash = calculate_hash('output_compress_zip_file.zip', hash_type)
            if result_hash is not None:
                print(f"Nilai hash setelah mengkompresi file ({hash_type.upper()}): \n↳ 🔑 {result_hash}")
                print(f"↳ {'✅ NILAI HASH TIDAK BERUBAH' if original_hash_value == result_hash else '❗️ NILAI HASH BERUBAH'}\n")
                mac = show_mac('output_compress_zip_file.zip')
                new_data_table = {"action": "Kompresi file", "hash_value": result_hash, "status_change": f"{'✅ TIDAK BERUBAH' if original_hash_value == result_hash else '❗️ BERUBAH'}", "mac":mac}
                data_result_table.append(new_data_table)
    with zipfile.ZipFile('output_compress_zip_file.zip', 'r') as zipf:
        os.makedirs('hasil_compress_file', exist_ok=True)
        zipf.extractall('hasil_compress_file')
        print(f"(2) Ekstraksi file ZIP")
        result_hash = calculate_hash('hasil_compress_file/compress_file_zip_'+source_path, hash_type)
        if result_hash is not None:
            print(f"Nilai hash setelah ekstraksi file ({hash_type.upper()}): \n↳ 🔑 {result_hash}")
            print(f"↳ {'✅ NILAI HASH TIDAK BERUBAH' if original_hash_value == result_hash else '❗️ NILAI HASH BERUBAH'}\n")
            mac = show_mac('hasil_compress_file/compress_file_zip_'+source_path)
            new_data_table = {"action": "Ekstraksi file", "hash_value": result_hash, "status_change": f"{'✅ TIDAK BERUBAH' if original_hash_value == result_hash else '❗️ BERUBAH'}", "mac":mac}
            data_result_table.append(new_data_table)

def encrypt_decrypt(source_path, destination_path, hash_type, original_hash_value):
    print(f"========= Case 7️⃣  - Enkripsi dan Dekripsi file {source_path} =========")
    key = Fernet.generate_key()
    fernetKey = Fernet(key)
    shutil.copy2(source_path, 'calon_encrypt_'+source_path)
    with open('calon_encrypt_'+source_path, 'rb') as f:
        original = f.read()
    encrypted = fernetKey.encrypt(original)
    with open('hasil_encrypt_'+source_path, 'wb') as f:
        f.write(encrypted)
    print(f"(1) Enkripsi file")
    print(f"== Isi file:")
    with open('calon_encrypt_'+source_path, 'r') as file:
        calon_encrypt_ = file.read()
        print(calon_encrypt_+"\n")
    print(f"== Isi file (encrypted):")
    with open('hasil_encrypt_'+source_path, 'r') as file:
        hasil_encrypt_ = file.read()
        print(hasil_encrypt_+"\n")
    result_hash = calculate_hash('hasil_encrypt_'+source_path, hash_type)
    if result_hash is not None:
        print(f"Nilai hash setelah enkripsi file ({hash_type.upper()}): \n↳ 🔑 {result_hash}")
        print(f"↳ {'✅ NILAI HASH TIDAK BERUBAH' if original_hash_value == result_hash else '❗️ NILAI HASH BERUBAH'}\n")
    mac = show_mac('hasil_encrypt_'+source_path)
    new_data_table = {"action": "Enkripsi file", "hash_value": result_hash, "status_change": f"{'✅ TIDAK BERUBAH' if original_hash_value == result_hash else '❗️ BERUBAH'}", "mac":mac}
    data_result_table.append(new_data_table)
    time.sleep(2)
    with open('hasil_encrypt_'+source_path, 'rb') as f:
        encrypted = f.read()
    decrypted = fernetKey.decrypt(encrypted)
    with open('hasil_decrypt_'+source_path, 'wb') as f:
        f.write(decrypted)
    print(f"(2) Dekripsi file")
    print(f"== Isi file (encrypted):")
    with open('hasil_encrypt_'+source_path, 'r') as file:
        hasil_encrypt_ = file.read()
        print(hasil_encrypt_+"\n")
    print(f"== Isi file (decrypted):")
    with open('hasil_decrypt_'+source_path, 'r') as file:
        calon_encrypt_ = file.read()
        print(calon_encrypt_+"\n")
    result_hash = calculate_hash('hasil_decrypt_'+source_path, hash_type)
    if result_hash is not None:
        print(f"Nilai hash setelah dekripsi file ({hash_type.upper()}): \n↳ 🔑 {result_hash}")
        print(f"↳ {'✅ NILAI HASH TIDAK BERUBAH' if original_hash_value == result_hash else '❗️ NILAI HASH BERUBAH'}\n")
    mac = show_mac('hasil_decrypt_'+source_path)
    new_data_table = {"action": "Dekripsi file", "hash_value": result_hash, "status_change": f"{'✅ TIDAK BERUBAH' if original_hash_value == result_hash else '❗️ BERUBAH'}", "mac":mac}
    data_result_table.append(new_data_table)

def change_file_permissions(source_path, destination_path, hash_type, original_hash_value):
    print(f"========= Case 8️⃣  - Mengubah permission file {source_path} =========")
    shutil.copy2(source_path, 'change_perm_file_'+source_path)
    try:
        os.chmod('change_perm_file_'+source_path, 0o755)
        result_hash = calculate_hash('change_perm_file_'+source_path, hash_type)
        if result_hash is not None:
            print(f"Nilai hash setelah rubah permission file ({hash_type.upper()}): \n↳ 🔑 {result_hash}")
            print(f"↳ {'✅ NILAI HASH TIDAK BERUBAH' if original_hash_value == result_hash else '❗️ NILAI HASH BERUBAH'}\n")
            mac = show_mac('change_perm_file_'+source_path)
            new_data_table = {"action": "Mengubah permission file", "hash_value": result_hash, "status_change": f"{'✅ TIDAK BERUBAH' if original_hash_value == result_hash else '❗️ BERUBAH'}", "mac":mac}
            data_result_table.append(new_data_table)
    except FileNotFoundError:
        print(f"File '{'change_perm_file_'+source_path}' tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def show_table(data):
    table = PrettyTable()
    table.field_names = ["No Case", "Tindakan", "Nilai Hash", "Status", "MAC"]
    table.align = "l"
    table.hrules = True
    for index, entry in enumerate(data, start=1):
        table.add_row([index, entry["action"], entry["hash_value"], entry["status_change"], entry["mac"]])
    print(table)

def show_mac(file_name):
    modify_time = os.path.getmtime(file_name)
    access_time = os.path.getatime(file_name)
    create_time = os.path.getctime(file_name)
    modify_time_d = datetime.fromtimestamp(modify_time).strftime('%Y-%m-%d %H:%M:%S')
    access_time_d = datetime.fromtimestamp(access_time).strftime('%Y-%m-%d %H:%M:%S')
    create_time_d = datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M:%S')
    response = f"""M:
{modify_time_d}
{modify_time}
A:
{access_time_d}
{access_time}
C:
{create_time_d}
{create_time}"""
    return response

data_result_table = []

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python check_hash.py <nama_file> <tipe_hash>")
        print("Hash type: 'md5' atau 'sha512'")
        sys.exit(1)

    file_name = sys.argv[1]
    hash_type = sys.argv[2]

    original_hash_value = calculate_hash(file_name, hash_type)
    print(f"\nOriginal Hash {file_name} ({hash_type.upper()}): \n↳ 🔑 {original_hash_value}\n")
    time.sleep(1)
    copy_file_and_check_hash(file_name, 'working_file_'+file_name, hash_type, original_hash_value)
    time.sleep(1)
    if os.path.splitext(file_name)[1] == '.txt':
        append_delete_text(file_name, 'working_file_'+file_name, hash_type, original_hash_value)
        time.sleep(1)
    rename_file(file_name, 'working_file_'+file_name, hash_type, original_hash_value)
    time.sleep(1)
    change_ext_file(file_name, 'working_file_'+file_name, hash_type, original_hash_value)
    time.sleep(1)
    change_file_metadata(file_name, 'working_file_'+file_name, hash_type, original_hash_value)
    time.sleep(1)
    compress_to_zip(file_name, 'working_file_'+file_name, hash_type, original_hash_value)
    time.sleep(1)
    if os.path.splitext(file_name)[1] == '.txt':
        encrypt_decrypt(file_name, 'working_file_'+file_name, hash_type, original_hash_value)
        time.sleep(1)
    change_file_permissions(file_name, 'working_file_'+file_name, hash_type, original_hash_value)
    time.sleep(2)
    print("\n")
    print(f"Original hash: {original_hash_value}")
    modify_time = os.path.getmtime(file_name)
    access_time = os.path.getatime(file_name)
    create_time = os.path.getctime(file_name)
    modify_time_d = datetime.fromtimestamp(modify_time).strftime('%Y-%m-%d %H:%M:%S')
    access_time_d = datetime.fromtimestamp(access_time).strftime('%Y-%m-%d %H:%M:%S')
    create_time_d = datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M:%S')
    response = f"""M: {modify_time_d} -> {modify_time}
A: {access_time_d} -> {access_time}
C: {create_time_d} -> {create_time}"""
    print(response)
    show_table(data_result_table)
    
