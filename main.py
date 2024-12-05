import pandas as pd
import numpy as np
from datetime import datetime
import msvcrt
import os
import hashlib
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.prompt import Prompt
import logging
import getpass


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

# tools
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
    queue = pd.DataFrame(columns=['Nama', 'Nik', 'gender', 'date', 'diagnosa', 'obat', 'ruangan'])

def clear_screen():
    os.system('cls')

def getch():
    return msvcrt.getch().decode('utf-8')

def load_credentials(keyring_path='keyring.csv'):
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
        print("Incorrect password.")
        return False
    
def login(keyring_path='keyring.csv'):
    df = load_credentials(keyring_path)
    user_logger = setup_user_logging(username)
    try:
        while True:
            username = Prompt.ask("[cyan]Masukkan username[/cyan]")
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
                main_menu()
            elif role == 'dokter':
                dokter_menu(username)
    except Exception as e:
        log_user_error(user_logger, f"Unexpected Error: {str(e)}")
    except Exception as e:
        log_user_error(user_logger, f"Unexpected Error: {str(e)}")
    
def login_menu():
    print ("login")
    print ("reservasi")
    print ('prees esc to exit')
    
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
    clear_screen()
    print("\n=== Sistem Informasi Kesehatan ===")
    print("1. Data Pasien")
    print("2. Jadwal Dokter")
    print("3. Konsul dan Diagnosa")
    print("4. Ruang Rawat Inap")
    print("5. Resep Obat")
    print("6. Pembayaran")
    print("7. New user")
    print("\nPress ESC to exit")
    
def main_menu():    
    show_main_menu
    while True:
        key = getch()
        if key == '1':
            show_data_pasien_menu()
        elif key == '2':
            show_doctor_schedule()
        elif key == '3':
            konsul_dan_diagnosa()
        elif key == '4':
            menu_kamar()
        elif key == '5':
            resep_obat()
        elif key == '6':
            pembayaran()
        elif key == '7':
            add_user()
        elif key == '\x1b':  # ESC key
            print("Exiting program...")
            break
        show_main_menu()

#fitur 1
def data_pasien_menu():
    clear_screen()
    print("\n=== Data Pasien ===")
    print("1. Tambah Pasien")
    print("2. Hapus Pasien")
    print("3. Edit Pasien")
    print("4. Lihat Daftar Pasien")
    print("\nPress ESC to return to main menu")

def antrian(logger):
    global queue
    clear_screen()
    print("\n=== Tambah Pasien ===")
    
    while True:
        try:
            Nama = input("Nama (or ESC to cancel): ")
            if Nama.lower() == 'esc':
                return
            
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

            gender = input("Gender (F/M): ").upper()
            if gender not in ["F", "M"]:
                print("Gender harus diisi dengan F atau M (kapital).")

            current_time = datetime.now()
            waktu = input("Waktu (MM-DD HH:MM) [default: sekarang]: ") or current_time.strftime("%m-%d %H:%M")
            log_user_action(logger, "Patient Added to Queue", {
                "Name": Nama,
                "NIK": NIK,
                "Gender": gender,
                "Time": waktu
            })

            temp = pd.DataFrame({
                'Nama': [Nama],
                'Nik': [NIK],
                'gender': [gender],
                'date': [waktu],
                'diagnosa': [np.nan],
                'obat': [np.nan],
                'ruangan': [np.nan]
            })

            queue = pd.concat([queue, temp], ignore_index=True)
            queue.to_csv('queue.csv', index=False)
            print("Antrian diperbarui dan disimpan ke 'queue.csv'.")
            break

        except Exception as e:
            print(f"Error: {e}")
            log_user_error(logger, f"Unexpected Error in Antrian", {
                "error": str(e)})
            
def handle_data_pasien():
    show_main_menu
    while True:
        key = getch()
        if key == '1':
            antrian()
        elif key == '2':
            show_remove_patient()
        elif key == '3':
            show_edit_patient()
        elif key == '4':
            show_patient_list()
        elif key == '\x1b':  # ESC key
            break
        show_data_pasien_menu()

def show_data_pasien_menu():
    clear_screen()
    print("\n=== Data Pasien ===")
    print("1. Tambah Pasien")
    print("2. Hapus Pasien")
    print("3. Edit Pasien")
    print("4. Lihat Daftar Pasien")
    print("\nPress ESC to return to main menu")
    handle_data_pasien()

def show_remove_patient(logger):
    global queue
    clear_screen()
    print("\n=== Hapus Pasien ===")
    print(queue)
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
        
        pause()
    except Exception as e:
        print(f"Error: {e}")
        pause()

def show_edit_patient(logger):
    global queue
    clear_screen()
    print("\n=== Edit Pasien ===")
    print(queue, logger)
    try:
        index_x = int(input("Enter row index: "))
        index_y = int(input("Enter column index: "))
        old_value = queue.iloc[index_x, index_y]
        new_value = input("Enter new value: ") or queue.iloc[index_x, index_y]
        queue.iat[index_x, index_y] =  new_value
        queue.to_csv('queue.csv', index=False)
        log_user_action(logger, "patient data edited successfully", {"old dvalue": old_value,"new value": new_value})
        print("Patient data updated successfully")
        pause()
    except Exception as e:
        log_user_error(logger, f"Unexpected Error in Antrian", {
                "error": str(e)})
        print(f"Error: {e}")
        pause()
def show_patient_list(logger):
    clear_screen()
    print("\n=== Daftar Pasien ===")
    print(queue)
    input("\nPress Enter to continue...")
    log_user_action(logger, "opened patient list")

def show_doctor_schedule(logger):
    try:
        with open('jadwal_dokter.csv', 'r') as f:
            print(f.read())
            log_user_action(logger, "opened doctor schedule")
    except FileNotFoundError:
        log_user_action(logger, "doctor schedule not found")
    pause()

def konsul_dan_diagnosa(logger):
    global queue
    clear_screen()
    print("\n=== Konsul dan Diagnosa ===")
    print(queue[queue['diagnosa'].isna()])
    
    try:
        index = int(input("Pilih index pasien untuk diagnosa: "))
        diagnosa = input("Masukkan diagnosa: ")
        queue.loc[index, 'diagnosa'] = diagnosa
        queue.to_csv('queue.csv', index=False)
        log_user_action(logger, "patient data edited successfully", {"nomor pasien": index,"diagnosa": diagnosa})
        print("Diagnosa berhasil ditambahkan")
        input("Press Enter to continue...")
    except Exception as e:
        print(f"Error: {e}")
        pause()

#fitur 4

def tampilkan_kamar(df,logger):
        print("\nStatus Kamar:")
        print(df.to_string(index=False))
        log_user_action(logger, "opened room data")

def check_in(df, nama_pasien, nomor_kamar, logger):
    indeks_kamar = df[df["Nomor Kamar"] == nomor_kamar].index
    if not indeks_kamar.empty:
        indeks = indeks_kamar[0]
        if df.at[indeks, "Status"] == "Kosong":
            df.at[indeks, "Status"] = "Terisi"
            df.at[indeks, "Nama Pasien"] = nama_pasien
            df.to_csv("data_kamar.csv", index=False)
            print(f"Pasien '{nama_pasien}' telah check-in ke kamar {nomor_kamar}.")
            log_user_action(logger, "pasien berhasil di check in",{"nama pasien": nama_pasien, "kamar": nomor_kamar } )
        else:
            print(f"Kamar {nomor_kamar} sudah terisi.")
    else:
        print("Nomor kamar tidak valid.")

def check_out(df, nomor_kamar):
    indeks_kamar = df[df["Nomor Kamar"] == nomor_kamar].index
    if not indeks_kamar.empty:
        indeks = indeks_kamar[0]
        if df.at[indeks, "Status"] == "Terisi":
            df.at[indeks, "Status"] = "Kosong"
            df.at[indeks, "Nama Pasien"] = "Kosong"
            df.to_csv("data_kamar.csv", index=False)
            print(f"Kamar {nomor_kamar} sekarang kosong.")
        else:
            print(f"Kamar {nomor_kamar} sudah kosong.")
    else:
        print("Nomor kamar tidak valid.")

def menu_kamar():
    daftar_kamar = pd.read_csv("data_kamar.csv")
    pilihan = getch()
    while True:
        print("\nMenu:")
        print("1. Tampilkan Status Kamar")
        print("2. Check-In Pasien")
        print("3. Check-Out Kamar")
        print("4. Keluar")

        if pilihan == "1":
            tampilkan_kamar(daftar_kamar)

        elif pilihan == "2":
            try:
                nomor_kamar = int(input("Masukkan nomor kamar untuk check-out: "))
                check_out(daftar_kamar, nomor_kamar)
            except ValueError:
                print("Input tidak valid. Masukkan nomor kamar yang benar.")

        elif pilihan == '\x1b':  # ESC
            break
        main_menu()

#fitur 5

def resep_obat():
    global queue
    clear_screen()
    print("\n=== Resep Obat ===")
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
def pembayaran():
    print("Pembayaran menu - To be implemented")
    input("Press Enter to continue...")
#fitur 7
def add_user(keyring_path='keyring.csv'):
    username = input()
    df = load_credentials(keyring_path)
    if not df[df['username'] == username].empty:
        print(f"Userame {username} sudah ada")
    password = input() #add that usual check where the user inputs twice and checks if they are the same then hash it
    password_hash = hash_password(password)
    print ('role')
    print ("1.admin")
    print ('2.dokter')
    while True:
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
    """Menu utama dengan layout terminal"""
    while True:
        show_title("Menu Utama")
        table = Table(title="Pilih Menu", box=None, title_style="bold cyan", header_style="bold yellow")
        table.add_column("No", style="bold white", justify="center")
        table.add_column("Menu", style="bold green")
        table.add_row("1", "Data Pasien")
        table.add_row("2", "Jadwal Dokter")
        table.add_row("3", "Hasil Diagnosa")
        table.add_row("4", "Resep Obat")
        table.add_row("5", "Pembayaran")
        table.add_row("6", "Keluar")

        console.print(Align.center(table))
        choice = Prompt.ask("[cyan]Pilih menu[/cyan]")

        if choice == "1":
            patient_data()
        elif choice == "2":
            doctor_schedule_menu()
        elif choice == "3":
            show_diagnosis()
        elif choice == "4":
            show_prescriptions()
        elif choice == "5":
            handle_payment()
        elif choice == "6":
            console.print("[bold cyan]Terima kasih telah menggunakan aplikasi.[/bold cyan]", justify="center")
            break
        else:
            console.print("[bold red]Pilihan tidak valid.[/bold red]", justify="center")
            pause()

def patient_data():
    """Tampilkan data pasien"""
    show_title("Data Pasien")
    nik = Prompt.ask("[cyan]Masukkan NIK[/cyan]")

    if nik in patients:
        patient = patients[nik]
        patient_panel = Panel.fit(
            f"[bold green]Nama:[/bold green] {patient['name']}\n"
            f"[bold green]Usia:[/bold green] {patient['age']}\n"
            f"[bold green]Riwayat:[/bold green] {', '.join(patient['history']) if patient['history'] else 'Belum ada riwayat'}",
            title="Informasi Pasien",
            border_style="green",
        )
        console.print(patient_panel)
    else:
        console.print("[bold red]Data pasien tidak ditemukan.[/bold red]", justify="center")

    pause()

def doctor_schedule_menu():
    """Tampilkan jadwal dokter dengan pilihan terpusat"""
    show_title("Jadwal Dokter")
    table = Table(title="Jadwal Dokter", box=None, title_style="bold cyan", header_style="bold yellow")
    table.add_column("No", justify="center", style="bold white")
    table.add_column("Nama Dokter", style="bold green")
    table.add_column("Spesialis", style="bold cyan")
    table.add_column("Jam Tersedia", style="bold magenta")

    for idx, doctor in enumerate(doctor_schedule, 1):
        table.add_row(str(idx), doctor["name"], doctor["specialty"], ", ".join(doctor["available_times"]))

    console.print(Align.center(table))

    choice = Prompt.ask("[cyan]Pilih dokter berdasarkan nomor[/cyan]", default="0")
    if choice.isdigit() and 0 < int(choice) <= len(doctor_schedule):
        doctor = doctor_schedule[int(choice) - 1]
        time_choice = Prompt.ask(f"[magenta]Pilih jam untuk {doctor['name']} ({', '.join(doctor['available_times'])})[/magenta]")
        if time_choice in doctor["available_times"]:
            appointments.append({"doctor": doctor["name"], "time": time_choice})
            console.print("[bold green]Antrean berhasil ditambahkan.[/bold green]", justify="center")
        else:
            console.print("[bold red]Jam tidak valid.[/bold red]", justify="center")
    pause()

def show_diagnosis():
    """Tampilkan diagnosa dokter"""
    show_title("Hasil Diagnosa")
    for idx, doctor in enumerate(doctor_schedule, 1):
        panel = Panel.fit(
            f"[bold cyan]Nama Dokter:[/bold cyan] {doctor['name']}\n"
            f"[bold cyan]Spesialis:[/bold cyan] {doctor['specialty']}\n"
            f"[bold cyan]Diagnosa:[/bold cyan] {', '.join(doctor['diagnosis'])}",
            title=f"Dokter {idx}",
            border_style="cyan",
        )
        console.print(panel)
    pause()

def show_prescriptions():
    """Tampilkan resep obat berdasarkan dokter"""
    show_title("Resep Obat")
    for idx, doctor in enumerate(doctor_schedule, 1):
        panel = Panel.fit(
            f"[bold cyan]Nama Dokter:[/bold cyan] {doctor['name']}\n"
            f"[bold cyan]Spesialis:[/bold cyan] {doctor['specialty']}\n"
            f"[bold cyan]Resep:[/bold cyan] {', '.join(doctor['resep'])}",
            title=f"Dokter {idx}",
            border_style="cyan",
        )
        console.print(panel)
    pause()

def handle_payment():
    """Tampilkan pembayaran dalam format struk"""
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

#dokter
def login_dokter(username):
    dokter = username
    print(f"Selamat datang, {dokter}!")
    return dokter

def lihat_dan_edit_jadwal(id_dokter):
    df_jadwal = pd.read_csv("jadwal_dokter.csv")
    jadwal_dokter = df_jadwal[df_jadwal["ID Dokter"] == id_dokter]
    
    if jadwal_dokter.empty:
        print("Tidak ada jadwal untuk dokter ini.")
    else:
        print("\nJadwal Anda:")
        print(jadwal_dokter.to_string(index=False))

        edit = input("\nApakah Anda ingin mengedit jadwal? (y/n): ").lower()
        if edit == "y":
            id_jadwal = int(input("Masukkan ID Jadwal yang ingin diubah: "))
            jadwal_baru = input("Masukkan jadwal baru: ")
            df_jadwal.loc[df_jadwal["ID Dokter"] == id_dokter, "Jadwal"] = jadwal_baru
            df_jadwal.to_csv("jadwal_dokter", index=False)
            print("Jadwal berhasil diperbarui.")
        else:
            print("Jadwal tidak diubah.")

def diagnosa_pasien():
    df_pasien = pd.read_csv("pasien.csv")
    nik_pasien = int(input("Masukkan NIK Pasien: "))
    pasien = df_pasien[df_pasien["nik"] == nik_pasien]
    
    if pasien.empty:
        print("Pasien tidak ditemukan.")
        return
    
    print(f"\nData Pasien: {pasien.iloc[0]['name']}, Umur: {pasien.iloc[0]['age']}")

    diagnosa = input("Masukkan Diagnosa: ")
    tindakan = input("Masukkan Tindakan (Rawat Inap/Resep Obat): ").lower()

    df_diagnosa = pd.read_csv("data_diagnosa.csv")
    new_diagnosa = pd.DataFrame({
        "NIK Pasien": [nik_pasien],
        "Diagnosa": [diagnosa],
        "Tindakan": [tindakan.capitalize()]
    })
    df_diagnosa = pd.concat([df_diagnosa, new_diagnosa], ignore_index=True)
    df_diagnosa.to_csv("data_diagnosa.csv", index=False)

    print(f"Diagnosa untuk pasien {pasien.iloc[0]['name']} telah dicatat.")

    if tindakan == "rawat inap":
        atur_rawat_inap()
    elif tindakan == "resep obat":
        atur_resep_obat()
    else:
        print("Tindakan tidak dikenali.")

def atur_rawat_inap(nama_pasien):
    df_rawat_inap = pd.read_csv("data_kamar.csv")
    print("\nDaftar Kamar Rawat Inap:")
    print(df_rawat_inap.to_string(index=False))
    
    nomor_kamar = int(input("\nMasukkan Nomor Kamar untuk rawat inap: "))
    kamar = df_rawat_inap[df_rawat_inap["Nomor Kamar"] == nomor_kamar]
    
    if not kamar.empty:
        indeks = kamar[0]
        if kamar.at[indeks, "Status"] == "Kosong":
            kamar.at[indeks, "Status"] = "Terisi"
            kamar.at[indeks, "Nama Pasien"] = nama_pasien
            kamar.to_csv("data_kamar.csv", index=False)
            print(f"Pasien '{nama_pasien}' telah check-in ke kamar {nomor_kamar}.")
        else:
            print(f"Kamar {nomor_kamar} sudah terisi.")
    else:
        print("Nomor kamar tidak valid.")

def atur_resep_obat():
    obat = input("Masukkan nama obat yang diresepkan: ")
    dosis = input("Masukkan dosis obat: ")
    durasi = input("Masukkan durasi penggunaan obat (misal: 5 hari): ")

    print(f"Resep obat untuk pasien: {obat}, Dosis: {dosis}, Durasi: {durasi} telah dicatat.")


def dokter_menu(x):
    login_dokter(x)
    pilihan = getch()

    while True:
        print("\nMenu:")
        print("1. Lihat dan Edit Jadwal Dokter")
        print("2. Mendiagnosa Pasien")
        print("Tekan ESC untuk keluar")
        
        if pilihan == "1":
            lihat_dan_edit_jadwal(x)
        elif pilihan == "2":
            diagnosa_pasien()
        elif pilihan == "\x1b" :
            break
        login(keyring_path='keyring.csv')

# jaga jaga buat debug biar gk login melulu
#if __name__ == "__main__":
#    main_menu()
if __name__ == "__main__":
    login_menu