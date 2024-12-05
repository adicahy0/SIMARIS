import pandas as pd
import numpy as np
from datetime import datetime
import msvcrt
import os
import hashlib
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.align import Align
import logging
import pyfiglet
from colorama import Fore, Style, init
from tabulate import tabulate


# Global variables
queue = None
console = Console()
patients = {}
doctor_schedule = []
appointments = []
prescriptions = []

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

def log_management():
    
    clear_screen()
    print("== Log Management System ==")
    
    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        print("No log directories found.")
        pause()
        return

    users = [d for d in os.listdir(logs_dir) if os.path.isdir(os.path.join(logs_dir, d))]
    
    if not users:
        print("No user log directories found.")
        pause()
        return

    print("\nAvailable Users:")
    for idx, user in enumerate(users, 1):
        print(f"{idx}. {user}")

    try:
        user_choice = input("Select user by number: ")
        selected_user = users[int(user_choice) - 1]
    except (ValueError, IndexError):
        print("Invalid user selection.")
        pause()
        return

    # Get log files for selected user
    user_logs_dir = os.path.join(logs_dir, selected_user)
    log_files = [f for f in os.listdir(user_logs_dir) if f.endswith('.log')]

    if not log_files:
        print(f"No log files found for user {selected_user}.")
        pause()
        return

    # Display log files
    print(f"\nLog Files for {selected_user}:")
    for idx, log_file in enumerate(log_files, 1):
        print(f"{idx}. {log_file}")

    # Log file selection
    try:
        log_choice = input("Select log file by number: ")
        selected_log_file = log_files[int(log_choice) - 1]
    except (ValueError, IndexError):
        print("Invalid log file selection.")
        pause()
        return

    # Read and display log file contents
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
def show_title(title):
    clear_screen()
    ascii_art = pyfiglet.figlet_format(title)
    print(Fore.CYAN + ascii_art)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def show_title(title):
    """Tampilkan judul di tengah layar"""
    clear_screen()
    title_text = Text(title, justify="center", style="bold cyan")
    console.print(Panel.fit(title_text))

def pause():
    console.print("\n[bold yellow]Tekan Enter untuk melanjutkan...[/bold yellow]")
    input()


def load_csv_data():
    """Memuat data pasien dan jadwal dokter dari file CSV"""
    global patients, doctor_schedule
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
    show_title("LOGIN")
    df = load_credentials(keyring_path)
    
    try:
        while True:
            username = Prompt.ask("[cyan]Masukkan username[/cyan]")
            user_logger = setup_user_logging(username)
            user_row = df[df['username'] == username]
            if user_row.empty:
                print("Username not found.")
                return False
            password = Prompt.ask("[cyan]Masukkan Password[/cyan]", password=True)
            role = login_processing(username, password,keyring_path='keyring.csv')
            if role:
                log_user_action(user_logger, "User Login", {
                "username": username, 
                "role": role })
            if role == 'admin':
                main_menu(user_logger)
            elif role == 'dokter':
                dokter_menu(username)
                
    except Exception as e:
        log_user_error(user_logger, f"Unexpected Error: {str(e)}")

    
    while True:
        key = getch()
        if key == '1':
            login ()
        if key == '2':
            print ("ini punya mu el, kalo menu pake getch ya, pengunaannya kaya function ini")
        if key == '\x1b':
            break
            
#admin
def show_main_menu():
    show_title("SIMORES")
    clear_screen()
    print("\n=== Sistem Informasi Kesehatan ===")
    print("1. Data Pasien")
    print("2. Jadwal Dokter")
    print("3. Checkout Ruang Inap")
    print("4. Pembayaran")
    print("5. New user")
    print("6. managemen log")
    print("\nPress ESC to exit")
    
def main_menu(logger):    

    while True:
        show_main_menu()
        key = getch()
        if key == '1':
            handle_data_pasien(logger)
        elif key == '2':
            show_doctor_schedule(logger)  
        elif key == '3':
            check_out()
        elif key == '4':
            handle_payment()
        elif key == '5':
            add_user()
        elif key == '6':
            log_management()
        elif key == '\x1b':  # ESC key
            print("Exiting program...")
            break

#fitur 1
def antrian(logger):
    global queue
    clear_screen()
    show_title("TAMBAH PASIEN")
    
    while True:
        try:
            Nama = input("Nama : ")
            if any(char.isdigit() for char in Nama):
                print("Nama tidak boleh berisi angka.")
                continue
            elif len(Nama) < 3:
                print("Nama terlalu pendek.")
                continue

            NIK = input("NIK: ")
            if not NIK.isdigit():
                print("NIK harus berupa angka.")
                continue
            elif len(NIK) != 16:
                print("NIK harus 16 digit.")
                continue

            try :
                age = int(input("Umur: "))
            except ValueError :
                print("Umur harus berupa angka.")

            current_time = datetime.now()
            waktu = input("Waktu (MM-DD HH:MM) [default: sekarang]: ") or current_time.strftime("%m-%d %H:%M")
            log_user_action(logger, "Patient Added to Queue", {
                "Name": Nama,
                "NIK": NIK,
                "Umur" : age,
                "Time": waktu
            })

            temp = pd.DataFrame({
                'Nama': [Nama],
                'Nik': [NIK],
                'umur': [age],
                'date': [waktu],
                'diagnosa': [np.nan],
                'obat': [np.nan],
                'ruangan': [np.nan]
            })

            queue = pd.concat([queue, temp], ignore_index=True)
            queue.to_csv('queue.csv', index=False)
            print("Antrian diperbarui dan disimpan ke 'queue.csv'.")
            return True
            break

        except Exception as e:
            print(f"Error: {e}")
            log_user_error(logger, f"Unexpected Error in Antrian", {
                "error": str(e)})

def handle_data_pasien(logger):
    while True:
        show_title(" Data Pasien")
        queue = pd.read_csv("queue.csv")
        print(tabulate(queue, headers="firstrow", tablefmt="fancy_grid"))
        print("1. Tambah Pasien")
        print("2. Hapus Pasien")
        print("3. Edit Pasien")
        print("\nPress ESC to return to main menu")
        key = getch()
        if key == '1':
            antrian(logger)
        elif key == '2':
            show_remove_patient(logger)
        elif key == '3':
            show_edit_patient(logger)
        elif key == '\x1b':  # ESC key
            break

def show_remove_patient(logger):
    global queue
    show_title ("Hapus Pasien")
    print(tabulate(queue, headers="firstrow", tablefmt="fancy_grid"))
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

def show_edit_patient(data,logger):
    data = pd.read_csv(f"{data}.csv")
    show_title("EDIT DATA")
    print(tabulate(data, headers="firstrow", tablefmt="fancy_grid"))
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


def show_doctor_schedule(logger):
    while True:
        show_title("JADWAL DOKTOR")
        try:
            jadwal_dokter= pd.read_csv("jadwal_dokter.csv")
            print (tabulate(jadwal_dokter, headers="firstrow", tablefmt="fancy_grid"))
            key = getch()
            if key == '\x1b':
                break
        except :
            print ("error")
            
#fitur 4

def check_out():
    while True:
        df = pd.read_csv("data_kamar.csv")
        clear_screen()
        show_title ("CHECKOUT")
        print(tabulate(df,headers="firstrow", tablefmt="fancy_grid"))
        nomor_kamar = int(input("Masukkan nomor kamar untuk check-out: "))
        if not nomor_kamar:
            break
        indeks_kamar = df[df["Nomor Kamar"] == nomor_kamar].index
        if not indeks_kamar.empty:
            indeks = indeks_kamar[0]
            if df.at[indeks, "Status"] == "Terisi":
                df.at[indeks, "Status"] = "Kosong"
                df.at[indeks, "Nama Pasien"] = "Kosong"
                df.to_csv("data_kamar.csv", index=False)
                print(f"Kamar {nomor_kamar} sekarang kosong.")
                return True
            else:
                print(f"Kamar {nomor_kamar} sudah kosong.")
        else:
            print("Nomor kamar tidak valid.")
#fitur 5
def resep_obat():
    global queue
    clear_screen()
    show_title("RESEP OBAT")
    print(queue[queue['obat'].isna()])
    
    try:
        index = int(input("Pilih index pasien untuk resep obat: "))
        obat = input("Masukkan obat: ")
        queue.loc[index, 'obat'] = obat
        queue.to_csv('queue.csv', index=False)
        print("Resep obat berhasil ditambahkan")
        input("Press Enter to continue...")
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to continue...")

#fitur 6
def handle_payment():
    show_title("Pembayaran")
    bpjs = Prompt.ask("[cyan]Apakah menggunakan BPJS? (y/n)[/cyan]").lower()
    if bpjs == "y":
        console.print("[bold green]Pembayaran ditanggung oleh BPJS.[/bold green]", justify="center")
    else:
        biaya_rawat = Prompt.ask("[yellow]Masukkan biaya rawat inap (0 jika tidak ada)[/yellow]", default="0")
        biaya_dokter = Prompt.ask("[yellow]Masukkan biaya konsultasi dokter[/yellow]")
        biaya_obat = Prompt.ask("[yellow]Masukkan biaya obat[/yellow]")
        total = int(biaya_rawat) + int(biaya_dokter) + int(biaya_obat)

        struk = (
            f"[bold yellow]--- STRUK PEMBAYARAN ---[/bold yellow]\n"
            f"[bold green]Biaya Rawat Inap  : Rp {biaya_rawat}[/bold green]\n"
            f"[bold green]Biaya Dokter      : Rp {biaya_dokter}[/bold green]\n"
            f"[bold green]Biaya Obat        : Rp {biaya_obat}[/bold green]\n"
            f"[bold white]Total            : Rp {total}[/bold white]"
        )
        console.print(Align.center(struk))
    pause()

#fitur 7
def add_user(keyring_path='keyring.csv'):
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
    
#user
def main_menu_user():
    logger = setup_user_logging("user")
    while True:
        show_title("MENU UTAMA")
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
            handle_payment()
        elif choice == '\x1b':
            break
        else:
            print(Fore.RED + "Pilihan tidak valid.")
            input(Fore.YELLOW + "Tekan Enter untuk kembali...")

def show_patient_data():
    while True:
        queue = pd.read_csv("queue.csv")
        show_title("DATA ANTRIAN")
        print (tabulate(queue, headers="firstrow", tablefmt="fancy_grid"))
        
        key = getch()
        if key == '\x1b':
            break

def schedule_appointment(logger):
    while True: 
        X = antrian(logger)
        if X == True:
            break

def jadwal():
    while True:
        show_title("JADWAL")
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

def tambah_jadwal(dokter):
    show_title("TAMBAH JADWAL DOKTER")
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

def diagnosa_pasien():
    clear_screen()
    show_title("DIAGNOSA")
    df_antrian = pd.read_csv("queue.csv")
    df_kamar= pd.read_csv("data_kamar.csv")
    try:
        nik_pasien = int(input("Masukkan NIK Pasien: "))
    except ValueError:
        print("Masukkan NIK berupa angka.")
        return

    pasien = df_antrian[df_antrian["Nik"] == nik_pasien]
    if pasien.empty:
        print("Pasien tidak ditemukan.")
        pause()
        return
    
    print(f"\nData Pasien: {pasien.iloc[0]['Nama']}, Umur: {pasien.iloc[0]['umur']}")
    diagnosa = input("Masukkan Diagnosa: ")
    tindakan = input("Masukkan Tindakan (Rawat Inap/Resep Obat): ").lower()

    df_diagnosa = pd.read_csv("data_diagnosa.csv")

    new_diagnosa = pd.DataFrame({
        "NIK Pasien": [nik_pasien],
        "Diagnosa": [diagnosa.capitalize()],
        "Tindakan": [tindakan.capitalize()]
    })
    df_diagnosa = pd.concat([df_diagnosa, new_diagnosa], ignore_index=True)
    df_diagnosa.to_csv("data_diagnosa.csv", index=False)

    print(f"Diagnosa untuk pasien {pasien.iloc[0]['Nama']} telah dicatat.")

    if tindakan == "rawat inap":
        atur_rawat_inap(nik_pasien)
    elif tindakan == "resep obat":
        atur_resep_obat(nik_pasien)
    else:
        print("Tindakan tidak dikenali.")
    return nik_pasien

def check_in(df, nama_pasien, nomor_kamar):
    indeks_kamar = df[df["Nomor Kamar"] == nomor_kamar].index
    if not indeks_kamar.empty:
        indeks = indeks_kamar[0]
        if df.at[indeks, "Status"] == "Kosong":
            df.at[indeks, "Status"] = "Terisi"
            df.at[indeks, "Nama Pasien"] = nama_pasien
            simpan_data(df)
            print(f"Pasien '{nama_pasien}' telah check-in ke kamar {nomor_kamar}.")
        else:
            print(f"Kamar {nomor_kamar} sudah terisi.")
    else:
        print("Nomor kamar tidak valid.")

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

    biaya_total = len(total_obat) * 5000
    df_queue.loc[df_queue["Nik"] == nik_pasien, "obat"] = biaya_total
    df_queue.to_csv("queue.csv", index=False)
    pause()

def dokter_menu(username):
    clear_screen()
    while True:
        show_title("MENU DOKTER")
        login_dokter(username)
            
        print("\n1. Lihat dan Edit Jadwal Dokter")
        print("2. Mendiagnosa Pasien")
        print("\nTekan ESC untuk keluar")

        pilihan = getch()
        if pilihan == "1":
            lihat_dan_edit_jadwal(username)
        elif pilihan == "2":
            diagnosa_pasien()
        elif pilihan == "\x1b" :
            break
# jaga jaga buat debug biar gk login melulu
if __name__ == "__main__":
    main_menu_user()
