import pandas as pd
import numpy as np
from datetime import datetime
import msvcrt
import os
import hashlib
import logging
import pyfiglet
from colorama import Fore
from tabulate import tabulate
# logger
def setup_user_logging(username):
    # Create a logs directory if it doesn't exist
    logs_dir = os.path.join('logs', username)
    os.makedirs(logs_dir, exist_ok=True)
    
    # Current year for log filename
    current_year = datetime.now().strftime("%Y")
    log_filename = os.path.join(logs_dir, f'{username}_{current_year}.log')
    
    # Configure logger
    logger = logging.getLogger(username)
    logger.setLevel(logging.INFO)
    
    # Clear existing handlers to prevent duplicate logging
    logger.handlers.clear()
    
    # Create file handler
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)  # Only print warnings and errors to console
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def log_user_action(logger, action, details=None):
    log_message = action
    if details:
        # Convert details to a readable string representation
        details_str = ', '.join(f"{k}: {v}" for k, v in details.items())
        log_message += f" - {details_str}"
    
    logger.info(log_message)

def log_user_error(logger, error, details=None):

    log_message = error
    if details:
        # Convert details to a readable string representation
        details_str = ', '.join(f"{k}: {v}" for k, v in details.items())
        log_message += f" - {details_str}"
    
    logger.error(log_message)
    
def riwayat():
    
    clear_screen()
    header("Riwayat pengguna")
    
    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        print("folder 'logs' tidak ditemukan")
        pause()
        return

    users = [d for d in os.listdir(logs_dir) if os.path.isdir(os.path.join(logs_dir, d))]
    
    if not users:
        print("folder user tidak ditemukan.")
        pause()
        return

    print("\n Users:")
    for idx, user in enumerate(users, 1):
        print(f"{idx}. {user}")

    try:
        user_choice = input("pilih dengan nomor: ")
        selected_user = users[int(user_choice) - 1]
    except (ValueError, IndexError):
        print("Invalid user selection.")
        pause()
        return
    
    user_logs_dir = os.path.join(logs_dir, selected_user)
    log_files = [f for f in os.listdir(user_logs_dir) if f.endswith('.log')]

    if not log_files:
        print(f"tidak ada riwayat untuk {selected_user}.")
        pause()
        return

    print(f"\nRiwayat {selected_user}:")
    for idx, log_file in enumerate(log_files, 1):
        print(f"{idx}. {log_file}")

    try:
        log_choice = input("Select log file by number: ")
        selected_log_file = log_files[int(log_choice) - 1]
    except (ValueError, IndexError):
        print("Invalid log file selection.")
        pause()
        return

    full_log_path = os.path.join(user_logs_dir, selected_log_file)
    
    try:
        while True:
            with open(full_log_path, 'r', encoding='utf-8') as file:
                log_contents = file.read()
            # Display log contents
            print("\n" + "=" * 50)
            print(f"Log File: {selected_log_file}")
            print("=" * 50)
            print(log_contents)
            print("=" * 50)
            key = getch()
            if key == "\x1b":
                break
    except Exception as e:
        print(f"Error reading log file: {e}")
        
def log_user_action(logger, action, details=None):
    log_message = action
    if details:
        # Convert details to a readable string representation
        details_str = ', '.join(f"{k}: {v}" for k, v in details.items())
        log_message += f" - {details_str}"
    
    logger.info(log_message)

def log_user_error(logger, error, details=None):

    log_message = error
    if details:
        # Convert details to a readable string representation
        details_str = ', '.join(f"{k}: {v}" for k, v in details.items())
        log_message += f" - {details_str}"
    
    logger.error(log_message)

# tools
def create_medical_record(nik, name=None, blood_type=None, gender=None, ):
    os.makedirs("medical_log", exist_ok=True)
    file_path_csv = f"medical_log/{nik}_record.csv"
    file_path_txt = f"medical_log/{nik}_record.txt"
    patient_data = {
        'Name': name,
        'Blood Type': blood_type,
        'Gender': gender,
    }
    patient_data = {k: v for k, v in patient_data.items() if v is not None}
    if not os.path.exists(file_path_csv):
        df = pd.DataFrame([patient_data])
        df.to_csv(file_path_csv, index=False)
    if not os.path.exists(file_path_txt):
        df_txt = pd.DataFrame()
        df_txt.to_csv(file_path_txt, index=False, header=False)
        return True

def log_medical_entry(nik, entry):
    
    log_path = f"medical_log/{nik}_log.txt"
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {entry}\n"
    
    with open(log_path, 'a') as logfile:
        logfile.write(log_entry)
def riwayat_txt(nik):
    file_path_txt = f"medical_log/{nik}_record.txt"
    try:
        df_txt = pd.read_csv(file_path_txt)
        return df_txt
    except:
        return None

def riwayat_csv(nik):
    file_path_csv = f"medical_log/{nik}_record.csv"
    try:
        df_csv = pd.read_csv(file_path_csv)
        return df_csv
    except FileNotFoundError:
        return None

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def header(text):
    separator = "=" * 80
    Garis = "\n".join(
        line.center(80) for line in ( separator).splitlines()
        )
    header = pyfiglet.figlet_format(text, font="slant", justify="center")
    if text:
        print(header)
    print(Garis)
    
def pause():
    print("Tekan Enter untuk melanjutkan...")
    input()
    
try:
    queue = pd.read_csv('queue.csv')
except FileNotFoundError:
    queue = pd.DataFrame(columns=['Nama', 'Nik', 'umur', 'date', 'diagnosa', 'obat', 'ruangan'])

def clear_screen():
    os.system('cls')

def getch():
    return msvcrt.getch().decode('utf-8')

def load_credentials(keyring_path='keyring.csv'):
    pd.read_csv(keyring_path)
    if not os.path.exists(keyring_path):
        print(f"Warning: {keyring_path} not found. Creating empty credentials file.")
        df = pd.DataFrame(columns=['username', 'password_hash', 'role'])
        df.to_csv(keyring_path, index=False)
        return df
    
    try:
        df = pd.read_csv(keyring_path)
        return df
    
    except pd.errors.EmptyDataError:
        print("Empty credentials file. Creating with default columns.")
        df = pd.DataFrame(columns=['username', 'password_hash','role'])
        df.to_csv(keyring_path, index=False)
        return df

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_processing(username, password, keyring_path='keyring.csv'):
    df = load_credentials(keyring_path)
    
    user_row = df[df['username'] == username]
    input_hash = hash_password(password)
    role = user_row['role'].values[0]
    
    if input_hash == user_row['password_hash'].values[0]:
        print("Login successful!")
        return role
    else:
        print("Incorrect password.")
        return False
    
def login(keyring_path='keyring.csv'):
    clear_screen()
    header("L o g i n")
    df = load_credentials(keyring_path)
    
    try:
        while True:
            username = input("Username : ")
            user_logger = setup_user_logging(username)
            user_row = df[df['username'] == username]
            if user_row.empty:
                print("Username not found.")
                return False
            password = input("Password : ")
            role = login_processing(username, password,keyring_path='keyring.csv')
            if role:
                log_user_action(user_logger, "User Login", {
                "username": username, 
                "role": role })
            if role == 'admin':
                main_menu(user_logger)
            elif role == 'dokter':
                dokter_menu(username,user_logger)
                
    except Exception as e:
        log_user_error(user_logger, f"Unexpected Error: {str(e)}")
            
#admin
def show_main_menu():
    clear_screen()
    header("S I M O R E S")
    print("1. Data Pasien")
    print("2. Jadwal Dokter")
    print("3. Checkout Ruang Inap")
    print("4. Pembayaran")
    print("5. New user")
    print("6. tampilkan riwayat pennguna")
    print("7. riwayat medis")
    print("\nPress ESC to exit")
    
def main_menu(logger):    
    while True:
        show_main_menu()
        key = getch()
        if key == '1':
            menu_data_pasien(logger)
        elif key == '2':
            jadwal_dokter_menu(logger)  
        elif key == '3':
            check_out ( ) 
        elif key == '4':
            pembayaran()
        elif key == '5':
            add_user(logger)
        elif key == '6':
            riwayat()
        elif key == "7":
            show_riwayat()
        elif key == '\x1b':  # ESC key
            print("Exiting program...")
            break

#fitur 1
def tambah_pasien(logger):
    global queue
    clear_screen()
    header("TAMBAH PASIEN")
    while True:
            Nama = input("Nama : ")
            if any(char.isdigit() for char in Nama):
                print("Nama tidak boleh berisi angka.")
                continue
            elif len(Nama) < 3:
                print("Nama terlalu pendek.")
                continue
            else:
                break
    while True:
            nomor_induk = input("NIK: ")
            if not nomor_induk.isdigit():
                print("NIK harus berupa angka.")
                continue
            elif len(nomor_induk) != 16:
                print("NIK harus 16 digit.")
                continue
            else:
                break
    while True:
            try :
                age = int(input("Umur: "))
            except ValueError :
                print("Umur harus berupa angka.")
                continue
            print ("golongan darah pasien")
            print("1.A+")
            print("2.A-")
            print("3.B+")
            print("4.B-")
            print("5.AB+")
            print("6.AB-")
            print("7.O+")
            print("8.O-")
            print("Tidak diketathui")
            
            key = getch()
            if key =='1':
                darah ="A+"
            elif key =='2':
                darah ="A-"
            elif key =='3':
                darah ="B+"
            elif key =='4':
                darah = "B-"
            elif key =='5':
                darah = "AB+"
            elif key =='6':
                darah = "AB-"
            elif key =='7':
                darah = "O+"
            elif key =='8':
                darah = "O-"
            elif key =='9':
                darah = "-"
                
            print("GENDER? [M/F]")
            key2 = getch()
            if key2 == 'm':
                gender= "Pria"
            elif key2 == 'f':
                gender= "wanita"
            
            current_time = datetime.now()
            waktu = input("Waktu (MM-DD HH:MM) [default: sekarang]: ") or current_time.strftime("%m-%d %H:%M")
            log_user_action(logger, "pasien ditambahkan", {
                "Name": Nama,
                "Nik": nomor_induk,
                "Umur" : age,
                "Time": waktu
            })

            temp = pd.DataFrame({
                'Nama': [Nama],
                'Nik': [nomor_induk],
                'Umur': [age],
                'Tanggal': [waktu],
                'Diagnosa': ["-"],
                'Resep': ["-"],
                'Ruangan': ["-"]
            })
            create_medical_record(
                    nomor_induk, 
                    Nama, 
                    darah, 
                    gender, 
                )
            queue = pd.concat([queue, temp], ignore_index=True)
            queue.to_csv('queue.csv', index=False)
            print("Antrian diperbarui dan disimpan ke 'queue.csv'.")
            return True

def menu_data_pasien(logger):
    clear_screen()
    while True:
        header("D a t a   P a s i e n")
        queue = pd.read_csv("queue.csv")
        print(tabulate(queue, headers=["Nama","Nik","Usia","Tangga;","Diagnosa","Resep","Ruangan"], tablefmt="fancy_grid"))
        print("1. Tambah Pasien")
        print("2. Hapus Pasien")
        print("3. Edit Pasien")
        print("\nPress ESC to return to main menu")
        key = getch()
        if key == '1':
            tambah_pasien(logger)
        elif key == '2':
            hapus_pasien(logger)
        elif key == '3':
            edit_data(logger)
        elif key == '\x1b':  # ESC key
            break
        
def hapus_pasien(logger):
    global queue
    header ("H a p u s   P a s i e n")
    print(tabulate(queue, headers=["Nama","Nik","Usia","Tangga;","Diagnosa","Resep","Ruangan"], tablefmt="fancy_grid"))
    try:
        index_antrian = int(input("Enter index to remove: "))
        patient_to_remove = queue.loc[index_antrian].to_dict()
        queue = queue.drop(index=index_antrian).reset_index(drop=True)
        log_user_action(logger, "Patient Removed Successfully", {
            "Index": index_antrian,
            "Removed Patient Details": patient_to_remove
        })
        queue.to_csv('queue.csv', index=False)
        print("Patient removed successfully")
        return True
    except Exception as e:
        print(f"Error: {e}")

def edit_data(data,logger):
    data = pd.read_csv(f"{data}.csv")
    header("E d i t   D a t a")
    print(tabulate(data, headers=["Nama","Nik","Usia","Tangga;","Diagnosa","Resep","Ruangan"], tablefmt="fancy_grid"))
    try:
        index_x = int(input("Enter row index: "))
        index_y = int(input("Enter column index: "))
        old_value = queue.iloc[index_x, index_y]
        new_value = input("Enter new value: ") or queue.iloc[index_x, index_y]
        data.iat[index_x, index_y] =  new_value
        data.to_csv(f'{data}.csv', index=False)
        log_user_action(logger, f"patient data edited successfully in {data} ", {"old dvalue": old_value,"new value": new_value})
        print("Patient data updated successfully")
        pause()
    except Exception as e:
        log_user_error(logger, f"Unexpected Error in {data}", {
                "error": str(e)})
        print(f"Error: {e}")


def jadwal_dokter_menu(logger):
    while True:
        clear_screen()
        header("J A D W A L   D O K T O R")
        try:
            jadwal_dokter= pd.read_csv("jadwal_dokter.csv")
            print (tabulate(jadwal_dokter, headers="firstrow", tablefmt="fancy_grid"))
            log_user_action(logger, f"admin buka jadwal doktor")
            print("tekan ESC untuk keluar")
            key = getch()
            if key == '\x1b':
                break
        except :
            print ("error")
            
#fitur 2

def check_out():
    while True:
        df = pd.read_csv("data_kamar.csv")
        clear_screen()
        header ("CHECKOUT")
        print(tabulate(df,headers="firstrow", tablefmt="fancy_grid"))
        nomor_kamar = int(input("Masukkan nomor kamar untuk check-out: "))
        if not nomor_kamar:
            break
        indeks_kamar = df[df["Nomor Kamar"] == nomor_kamar].index
        if not indeks_kamar.empty:
            indeks = indeks_kamar[0]
            if df.at[indeks, "Status"] == "Terisi":
                df.at[indeks, "Status"] = "Kosong"
                df.at[indeks, "Nama Pasien"] = "-"
                df.to_csv("data_kamar.csv", index=False)
                print(f"Kamar {nomor_kamar} sekarang kosong.")
                return True
            else:
                print(f"Kamar {nomor_kamar} sudah kosong.")
        else:
            print("Nomor kamar tidak valid.")

#fitur 3
def pembayaran():
    header("Pembayaran")
    clear_screen()
    bpjs = input("Apakah nakan BPJS? (y/n)").lower()
    if bpjs == "y":
        print("Pembayaran ditanggung oleh BPJS.")
    else:
        biaya_rawat = input("Masukkan biaya rawat inap (0 jika tidak ada) :") or 0
        biaya_dokter = input("Masukkan biaya konsultasi dokter :")
        biaya_obat = input("Masukkan biaya obat : ")
        total = int(biaya_rawat) + int(biaya_dokter) + int(biaya_obat)

        struk = (
            f"--- STRUK PEMBAYARAN ---\n"
            f"Biaya Rawat Inap  : Rp {biaya_rawat}\n"
            f"Biaya Dokter      : Rp {biaya_dokter}\n"
            f"Biaya Obat        : Rp {biaya_obat}\n"
            f"Total            : Rp {total}"
        )
        clear_screen()
        print(struk)
    pause()

#fitur 4
def add_user(logger,keyring_path='keyring.csv'):
    clear_screen()
    while True:
        username = input( "username : ")
        df = load_credentials(keyring_path)
        if not df[df['username'] == username].empty:
            print(f"Userame {username} sudah ada")
            pause()
            return False
        else:    
            password = input("password : ")
            password_hash = hash_password(password)
            while True:
                print ('role')
                print ("1.admin")
                print ('2.dokter')
                key = getch()
                if key == '1':
                    role = 'admin'
                    break
                if key == '2':
                    role = 'dokter'
                    break
            new_user = pd.DataFrame({
            'username': [username], 
            'password_hash': [password_hash],
            'role' : [role]
        })
        
        updated_df = pd.concat([df, new_user], ignore_index=True)
        updated_df.to_csv(keyring_path, index=False)
        print(f"User {username} added successfully.")
        return True
    
def show_riwayat():
    clear_screen()
    header("Riwayat Medis")
    nik = input("NIK pasien : ")
    csv = riwayat_csv(nik)
    txt = riwayat_txt(nik)
    print(tabulate(csv, headers = ["Nik", "Nama", "Tipe Darah", "Gender"],tablefmt="fancy_grid"))
    print (txt)
    print ("tekan ESC untuk keluar")
    Key = getch()
    if Key == "\x1b":
        return
    
    
    
    
#user
def menu_login():
    clear_screen
    logger = setup_user_logging("user")
    while True:
        header("MENU UTAMA")
        print(Fore.YELLOW + "1. login")
        print(Fore.YELLOW + "2. reservasi")
        print(Fore.YELLOW + "3. Antrean Pasien")
        print(Fore.YELLOW + "4. Jadwal Dokter")
        print(Fore.YELLOW + "5. Pembayaran")
        print(Fore.YELLOW + "tekan ESC TO EXIT")

        choice = getch()
        print (Fore.CYAN + "Pilih menu: ")
        if choice == "1":
            login()
        elif choice == "2":
            schedule_appointment(logger)
        elif choice == "3":
            show_patient_data()
        elif choice == "4":
            jadwal()
        elif choice == "5":
            pembayaran()
        elif choice == '\x1b':
            break
        else:
            print(Fore.RED + "Pilihan tidak valid.")
            input(Fore.YELLOW + "Tekan Enter untuk kembali...")

def show_patient_data():
    while True:
        queue = pd.read_csv("queue.csv")
        header("DATA ANTRIAN")
        print (tabulate(queue, headers="firstrow", tablefmt="fancy_grid"))
        
        key = getch()
        if key == '\x1b':
            break

def schedule_appointment(logger):
    while True: 
        X = tambah_pasien(logger)
        if X == True:
            break

def jadwal():
    while True:
        header("JADWAL")
        jadwal_dokter= pd.read_csv("jadwal_dokter.csv")
        print (tabulate(jadwal_dokter, headers="firstrow", tablefmt="fancy_grid"))
        
        key = getch()
        if key == '\x1b':
            break

#dokter
def login_dokter(username):
    dokter = username
    print(f"Selamat datang, dr. {dokter.capitalize()}!")
    return dokter

def tambah_jadwal(dokter, logger):
    header("T a m b a h  J a d w a l")
    jadwal = pd.read_csv("jadwal_dokter.csv")
    nama = (f"dr. {dokter.capitalize()}")

    while True:
        spesialis = input("Masukkan Spesialis: ").capitalize()
        if spesialis:
            break
        print("Spesialis tidak boleh kosong. Silakan coba lagi.")

    hari_valid = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    while True:
        hari = input(f"Masukkan Hari (pilihan: {', '.join(hari_valid)}): ").capitalize()
        if hari in hari_valid:
            break
        print("Hari tidak valid. Silakan masukkan hari yang benar.")

    while True:
        jam_masuk = input("Masukkan Jam Masuk: (format HH:MM) ")
        if jam_masuk :
            break
        print("Jam masuk tidak boleh kosong. Silakan coba lagi.")
    
    while True:    
        jam_keluar = input("Masukkan Jam Keluar: (format HH:MM) ")
        if jam_keluar:
            break
        print("Jam Keluar tidak boleh kosong. Silakan coba lagi.")

    temp = pd.DataFrame({
        "Nama Dokter" : [nama],
        "Spesialis" : [spesialis],
        "Hari" : [hari],
        "Jam" : [f"{jam_masuk}-{jam_keluar}"]})
    
    jadwal = pd.concat([jadwal, temp], ignore_index=False)
    jadwal.to_csv("jadwal_dokter.csv", index=False)

def lihat_dan_edit_jadwal(dokter):
    clear_screen()
    df_jadwal = pd.read_csv("jadwal_dokter.csv")
    
    while True:
        jadwal_dokter = df_jadwal[df_jadwal["Nama Dokter"] == (f"dr. {dokter.capitalize()}")]
        if jadwal_dokter.empty:
            print("Tidak ada jadwal untuk dokter ini.")
            print("\nApakah anda ingin menambahkan jadwal? (y/n)")
            pilihan = getch()
            if pilihan == "y":
                tambah_jadwal(dokter)
            elif pilihan == "n":
                break
        else :
            print("\nJadwal Anda:")
            print(jadwal_dokter.to_string(index=False))
            print("\nApakah Anda ingin mengedit jadwal? (Y/N): ")
            edit = getch()

            if edit == "y":
                try:
                    index_jadwal = int(input(f"Masukkan nomor jadwal yang ingin diedit (0 hingga {len(jadwal_dokter) - 1}): "))
                    if index_jadwal < 0 or index_jadwal >= len(jadwal_dokter):
                        print("Nomor jadwal tidak valid.")
                        return
                except ValueError:
                    print("Masukkan nomor jadwal yang valid.")
                    return

                print("\nPilih kolom yang ingin Anda edit:")
                print("1. Hari")
                print("2. Jam")
                
                print("Masukkan pilihan (1/2): ")

                pilihan = getch()
                if pilihan == "1":
                    hari_baru = input("Masukkan hari baru: ").strip()
                    df_jadwal.loc[jadwal_dokter.index[index_jadwal], "Hari"] = hari_baru
                elif pilihan == "2":
                    jam_baru = input("Masukkan jam baru (format HH:MM-HH:MM): ").strip()
                    df_jadwal.loc[jadwal_dokter.index[index_jadwal], "Jam"] = jam_baru
                else:
                    print("Pilihan tidak valid.")
                    return
                        
                df_jadwal.to_csv("jadwal_dokter.csv", index=False)
                print("\nJadwal berhasil diperbarui.")
    
            elif edit == "n":
                print("Jadwal tidak diubah.")
                print("Tekan Esc untuk keluar")
            else:
                print("Pilihan tidak valid.")
        key = getch()
        if key == "\x1b":
            break


def hapus_pasien(logger):
    global queue
    header ("H a p u s   P a s i e n")
    print(tabulate(queue, headers=["Nama","Nik","Usia","Tangga;","Diagnosa","Resep","Ruangan"], tablefmt="fancy_grid"))
    try:
        index_antrian = int(input("Enter index to remove: "))
        patient_to_remove = queue.loc[index_antrian].to_dict()
        queue = queue.drop(index=index_antrian).reset_index(drop=True)
        log_user_action(logger, "Patient Removed Successfully", {
            "Index": index_antrian,
            "Removed Patient Details": patient_to_remove
        })
        queue.to_csv('queue.csv', index=False)
        print("Patient removed successfully")
        return True
    except Exception as e:
        print(f"Error: {e}")

def edit_data(data,logger):
    data = pd.read_csv(f"{data}.csv")
    header("E d i t   D a t a")
    print(tabulate(data, headers=["Nama","Nik","Usia","Tanggal;","Diagnosa","Resep","Ruangan"], tablefmt="fancy_grid"))
    try:
        index_x = int(input("Enter row index: "))
        index_y = int(input("Enter column index: "))
        old_value = queue.iloc[index_x, index_y]
        new_value = input("Enter new value: ") or queue.iloc[index_x, index_y]
        data.iat[index_x, index_y] =  new_value
        data.to_csv(f'{data}.csv', index=False)
        log_user_action(logger, f"patient data edited successfully in {data} ", {"old dvalue": old_value,"new value": new_value})
        print("Patient data updated successfully")
        pause()
    except Exception as e:
        log_user_error(logger, f"Unexpected Error in {data}", {
                "error": str(e)})
        print(f"Error: {e}")


def jadwal_dokter_menu(logger):
    while True:
        header("J A D W A L   D O K T O R")
        try:
            jadwal_dokter= pd.read_csv("jadwal_dokter.csv")
            print (tabulate(jadwal_dokter, headers="firstrow", tablefmt="fancy_grid"))
            log_user_action(logger, f"admin buka jadwal doktor")
            print("tekan ESC untuk keluar")
            key = getch()
            if key == '\x1b':
                break
        except :
            print ("error")
            
#fitur 2

def check_out():
    while True:
        df = pd.read_csv("data_kamar.csv")
        clear_screen()
        header ("CHECKOUT")
        print(tabulate(df,headers="firstrow", tablefmt="fancy_grid"))
        nomor_kamar = int(input("Masukkan nomor kamar untuk check-out: "))
        if not nomor_kamar:
            break
        indeks_kamar = df[df["Nomor Kamar"] == nomor_kamar].index
        if not indeks_kamar.empty:
            indeks = indeks_kamar[0]
            if df.at[indeks, "Status"] == "Terisi":
                df.at[indeks, "Status"] = "Kosong"
                df.at[indeks, "Nama Pasien"] = "-"
                df.to_csv("data_kamar.csv", index=False)
                print(f"Kamar {nomor_kamar} sekarang kosong.")
                return True
            else:
                print(f"Kamar {nomor_kamar} sudah kosong.")
        else:
            print("Nomor kamar tidak valid.")

#fitur 3
def pembayaran():
    header("Pembayaran")
    bpjs = input("[cyan]Apakah nakan BPJS? (y/n)").lower()
    if bpjs == "y":
        print("[bold green]Pembayaran ditanggung oleh BPJS.[/bold green]")
    else:
        biaya_rawat = input("[yellow]Masukkan biaya rawat inap (0 jika tidak ada)[/yellow]", default="0")
        biaya_dokter = input("[yellow]Masukkan biaya konsultasi dokter[/yellow]")
        biaya_obat = input("[yellow]Masukkan biaya obat[/yellow]")
        total = int(biaya_rawat) + int(biaya_dokter) + int(biaya_obat)

        struk = (
            f"[bold yellow]--- STRUK PEMBAYARAN ---[/bold yellow]\n"
            f"[bold green]Biaya Rawat Inap  : Rp {biaya_rawat}[/bold green]\n"
            f"[bold green]Biaya Dokter      : Rp {biaya_dokter}[/bold green]\n"
            f"[bold green]Biaya Obat        : Rp {biaya_obat}[/bold green]\n"
            f"[bold white]Total            : Rp {total}[/bold white]"
        )
        print(struk)
    pause()

#fitur 4
def add_user(logger,keyring_path='keyring.csv'):
    clear_screen()
    while True:
        username = input( "username : ")
        df = load_credentials(keyring_path)
        if not df[df['username'] == username].empty:
            print(f"Userame {username} sudah ada")
            pause()
            return False
        else:    
            password = input("password : ")
            password_hash = hash_password(password)
            while True:
                print ('role')
                print ("1.admin")
                print ('2.dokter')
                key = getch()
                if key == '1':
                    role = 'admin'
                    break
                if key == '2':
                    role = 'dokter'
                    break
            new_user = pd.DataFrame({
            'username': [username], 
            'password_hash': [password_hash],
            'role' : [role]
        })
        
        updated_df = pd.concat([df, new_user], ignore_index=True)
        updated_df.to_csv(keyring_path, index=False)
        print(f"User {username} added successfully.")
        return True
    
def show_riwayat():
    nik = input("NIK pasien : ")
    csv = riwayat_csv(nik)
    txt = riwayat_txt(nik)
    print(tabulate(csv, headers = ["Nik", "Nama", "Tipe Darah", "Gender"],tablefmt="fancy_grid"))
    print (txt)
    print ("tekan ESC untuk keluar")
    Key = getch()
    if Key == "\x1b":
        return
    
    
    
    
#user
def menu_login():
    clear_screen
    logger = setup_user_logging("user")
    while True:
        header("MENU UTAMA")
        print(Fore.YELLOW + "1. login")
        print(Fore.YELLOW + "2. reservasi")
        print(Fore.YELLOW + "3. Antrean Pasien")
        print(Fore.YELLOW + "4. Jadwal Dokter")
        print(Fore.YELLOW + "5. Pembayaran")
        print(Fore.YELLOW + "tekan ESC TO EXIT")

        choice = getch()
        print (Fore.CYAN + "Pilih menu: ")
        if choice == "1":
            login()
        elif choice == "2":
            schedule_appointment(logger)
        elif choice == "3":
            show_patient_data()
        elif choice == "4":
            jadwal()
        elif choice == "5":
            pembayaran()
        elif choice == '\x1b':
            break
        else:
            print(Fore.RED + "Pilihan tidak valid.")
            input(Fore.YELLOW + "Tekan Enter untuk kembali...")

def show_patient_data():
    while True:
        queue = pd.read_csv("queue.csv")
        header("DATA ANTRIAN")
        print (tabulate(queue, headers="firstrow", tablefmt="fancy_grid"))
        
        key = getch()
        if key == '\x1b':
            break

def schedule_appointment(logger):
    while True: 
        X = tambah_pasien(logger)
        if X == True:
            break

def jadwal():
    while True:
        header("JADWAL")
        jadwal_dokter= pd.read_csv("jadwal_dokter.csv")
        print (tabulate(jadwal_dokter, headers="firstrow", tablefmt="fancy_grid"))
        
        key = getch()
        if key == '\x1b':
            break

#dokter
def login_dokter(username):
    dokter = username
    print(f"Selamat datang, dr. {dokter.capitalize()}!")
    return dokter

def tambah_jadwal(dokter, logger):
    header("T a m b a h  J a d w a l")
    jadwal = pd.read_csv("jadwal_dokter.csv")
    nama = (f"dr. {dokter.capitalize()}")

    while True:
        spesialis = input("Masukkan Spesialis: ").capitalize()
        if spesialis:
            break
        print("Spesialis tidak boleh kosong. Silakan coba lagi.")

    hari_valid = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    while True:
        hari = input(f"Masukkan Hari (pilihan: {', '.join(hari_valid)}): ").capitalize()
        if hari in hari_valid:
            break
        print("Hari tidak valid. Silakan masukkan hari yang benar.")

    while True:
        jam_masuk = input("Masukkan Jam Masuk: (format HH:MM) ")
        if jam_masuk :
            break
        print("Jam masuk tidak boleh kosong. Silakan coba lagi.")
    
    while True:    
        jam_keluar = input("Masukkan Jam Keluar: (format HH:MM) ")
        if jam_keluar:
            break
        print("Jam Keluar tidak boleh kosong. Silakan coba lagi.")

    temp = pd.DataFrame({
        "Nama Dokter" : [nama],
        "Spesialis" : [spesialis],
        "Hari" : [hari],
        "Jam" : [f"{jam_masuk}-{jam_keluar}"]})
    
    jadwal = pd.concat([jadwal, temp], ignore_index=False)
    jadwal.to_csv("jadwal_dokter.csv", index=False)

def lihat_dan_edit_jadwal(dokter):
    clear_screen()
    df_jadwal = pd.read_csv("jadwal_dokter.csv")
    
    while True:
        jadwal_dokter = df_jadwal[df_jadwal["Nama Dokter"] == (f"dr. {dokter.capitalize()}")]
        if jadwal_dokter.empty:
            print("Tidak ada jadwal untuk dokter ini.")
            print("\nApakah anda ingin menambahkan jadwal? (y/n)")
            pilihan = getch()
            if pilihan == "y":
                tambah_jadwal(dokter)
            elif pilihan == "n":
                break
        else :
            print("\nJadwal Anda:")
            print(jadwal_dokter.to_string(index=False))
            print("\nApakah Anda ingin mengedit jadwal? (Y/N): ")
            edit = getch()

            if edit == "y":
                try:
                    index_jadwal = int(input(f"Masukkan nomor jadwal yang ingin diedit (0 hingga {len(jadwal_dokter) - 1}): "))
                    if index_jadwal < 0 or index_jadwal >= len(jadwal_dokter):
                        print("Nomor jadwal tidak valid.")
                        return
                except ValueError:
                    print("Masukkan nomor jadwal yang valid.")
                    return

                print("\nPilih kolom yang ingin Anda edit:")
                print("1. Hari")
                print("2. Jam")
                
                print("Masukkan pilihan (1/2): ")

                pilihan = getch()
                if pilihan == "1":
                    hari_baru = input("Masukkan hari baru: ").strip()
                    df_jadwal.loc[jadwal_dokter.index[index_jadwal], "Hari"] = hari_baru
                elif pilihan == "2":
                    jam_baru = input("Masukkan jam baru (format HH:MM-HH:MM): ").strip()
                    df_jadwal.loc[jadwal_dokter.index[index_jadwal], "Jam"] = jam_baru
                else:
                    print("Pilihan tidak valid.")
                    return
                        
                df_jadwal.to_csv("jadwal_dokter.csv", index=False)
                print("\nJadwal berhasil diperbarui.")
    
            elif edit == "n":
                print("Jadwal tidak diubah.")
                print("Tekan Esc untuk keluar")
            else:
                print("Pilihan tidak valid.")
        key = getch()
        if key == "\x1b":
            break

def diagnosa_pasien(logger):
    clear_screen()
    header("D I A G N O S A")
    df_antrian = pd.read_csv("queue.csv")
    df_kamar = pd.read_csv("data_kamar.csv")
    print(tabulate(df_antrian, headers="firstrow", tablefmt="fancy_grid"))

    nik_pasien = int(input("Masukkan nomor_induk Pasien: "))
    pasien = df_antrian[df_antrian["Nik"] == nik_pasien].index

    if pasien.empty:
        print("Pasien tidak ditemukan.")
        pause()
        return

    diagnosa = input("Masukkan Diagnosa: ")
    if not diagnosa:
        diagnosa = "-"
    log_medical_entry(nik_pasien, f"pasien tediagnosis: {diagnosa}")
    x= df_antrian.at[nik_pasien, "Diagnosa"] = diagnosa
    x.to_csv("queue.csv")
    print(f"Diagnosa untuk pasien {df_antrian.at[pasien[0], 'Nama']} telah dicatat.")    
    key = getch()
    print("1.Rawat Inap")
    print("2.Resep Obat")
    if key == "1" :
        check_in(df_antrian, df_kamar, nik_pasien,logger)
    elif key == "2":
        atur_resep_obat(nik_pasien,logger)

def check_in(df_antrian, df_kamar, nik_pasien,logger):
    clear_screen()
    header("C h e c k   I n")
    print(tabulate(df_kamar, headers="keys", tablefmt="fancy_grid"))
    
    try:
        nomor_kamar = int(input("Masukkan nomor kamar: "))
    except ValueError:
        print("Input harus berupa angka.")
        return

    indeks_kamar = df_kamar[df_kamar["Nomor Kamar"] == (nomor_kamar)].index
    indeks_pasien = df_antrian[df_antrian["Nik"] == (nik_pasien)].index

    if indeks_kamar.empty:
        print("Nomor kamar tidak valid.")
        return

    indeks_kamar = indeks_kamar[0]  # Get the actual integer index of the room
    if df_kamar.at[indeks_kamar, "Status"] == "Kosong":
        if not indeks_pasien.empty:
            indeks_pasien = indeks_pasien[0]  # Get the integer index of the patient
            df_kamar.at[indeks_kamar, "Status"] = "Terisi"
            df_kamar.at[indeks_kamar, "Nama Pasien"] = str(df_antrian.at[indeks_pasien, "Nama"])
            df_antrian.at[indeks_pasien, "Ruangan"] = int(df_kamar.at[indeks_kamar, "Nomor Kamar"])
            print(f"Pasien '{df_antrian.at[indeks_pasien, 'Nama']}' telah check-in ke kamar {nomor_kamar}.")
            
            df_antrian.to_csv("queue.csv", index=False)
            df_kamar.to_csv("data_kamar.csv", index=False)
        else:
            print("Pasien tidak ditemukan di daftar antrian.")
    else:
        print(f"Kamar {nomor_kamar} sudah terisi.")

def atur_resep_obat(nik_pasien):
    clear_screen()
    df_queue = pd.read_csv("queue.csv")    
    total_obat = []

    while True:
        obat = input("Masukkan nama obat yang diresepkan: ")
        print("Apakah anda ingin menambahkan obat lain? (y/n)")
        total_obat.append(obat)
        lanjut = getch()
        if lanjut == "y":
            continue
        elif lanjut == "n":
            break

    dosis = input("Masukkan dosis obat: ")
    durasi = input("Masukkan durasi penggunaan obat (misal: 5 hari): ")

    print(f"Resep obat untuk pasien: {', '.join(total_obat)}, Dosis: {dosis}, Durasi: {durasi} telah dicatat.")
    log_medical_entry(nik_pasien, f"mendapat resep obat :{total_obat}")
    df_queue.loc[df_queue["Nik"] == nik_pasien, "Resep"] = total_obat
    df_queue.to_csv("queue.csv", index=False)
    pause()

def dokter_menu(username,logger):
    clear_screen()
    while True:
        header("MENU DOKTER")
        login_dokter(username)
            
        print("\n1. Lihat dan Edit Jadwal Dokter")
        print("2. Mendiagnosa Pasien")
        print("\nTekan ESC untuk keluar")

        pilihan = getch()
        if pilihan == "1":
            lihat_dan_edit_jadwal(username,logger)
        elif pilihan == "2":
            diagnosa_pasien(logger)
        elif pilihan == "\x1b" :
            break
# jaga jaga buat debug biar gk login melulu
if __name__ == "__main__":
    menu_login()