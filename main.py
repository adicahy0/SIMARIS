import pandas as pd
import numpy as np
from datetime import datetime
import msvcrt
import os
import hashlib

# Global variables
queue = None
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
    df = load_credentials(keyring_path)
    while True:
        username = input()
        user_row = df[df['username'] == username]
        
        if user_row.empty:
            print("Username not found.")
            return False
        
        password = input()
        
        role = login_processing(username, password,keyring_path='keyring.csv')
        
        if role == 'admin':
            main_menu()
        elif role == 'doktor':
            print ("masukin menu doktor dani")
    
    
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

def data_pasien_menu():
    clear_screen()
    print("\n=== Data Pasien ===")
    print("1. Tambah Pasien")
    print("2. Hapus Pasien")
    print("3. Edit Pasien")
    print("4. Lihat Daftar Pasien")
    print("\nPress ESC to return to main menu")

def antrian():
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
                continue

            current_time = datetime.now()
            waktu = input("Waktu (MM-DD HH:MM) [default: sekarang]: ") or current_time.strftime("%m-%d %H:%M")

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

def show_data_pasien_menu():
    clear_screen()
    print("\n=== Data Pasien ===")
    print("1. Tambah Pasien")
    print("2. Hapus Pasien")
    print("3. Edit Pasien")
    print("4. Lihat Daftar Pasien")
    print("\nPress ESC to return to main menu")
    handle_data_pasien()

def show_remove_patient():
    global queue
    clear_screen()
    print("\n=== Hapus Pasien ===")
    print(queue)
    try:
        index_antrian = int(input("Enter index to remove: "))
        queue = queue.drop(index=index_antrian).reset_index(drop=True)
        queue.to_csv('queue.csv', index=False)
        print("Patient removed successfully")
        input("Press Enter to continue...")
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to continue...")

def show_edit_patient():
    global queue
    clear_screen()
    print("\n=== Edit Pasien ===")
    print(queue)
    try:
        index_x = int(input("Enter row index: "))
        index_y = int(input("Enter column index: "))
        new_value = input("Enter new value: ") or queue.iloc[index_x, index_y]
        queue.iat[index_x, index_y] = new_value
        queue.to_csv('queue.csv', index=False)
        print("Patient data updated successfully")
        input("Press Enter to continue...")
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to continue...")

def show_patient_list():
    clear_screen()
    print("\n=== Daftar Pasien ===")
    print(queue)
    input("\nPress Enter to continue...")

def show_doctor_schedule():
    try:
        with open('jadwal_dokter.csv', 'r') as f:
            print(f.read())
    except FileNotFoundError:
        print("Jadwal dokter tidak tersedia.")
    input("\nPress Enter to continue...")

def konsul_dan_diagnosa():
    global queue
    clear_screen()
    print("\n=== Konsul dan Diagnosa ===")
    print(queue[queue['diagnosa'].isna()])
    
    try:
        index = int(input("Pilih index pasien untuk diagnosa: "))
        diagnosa = input("Masukkan diagnosa: ")
        queue.loc[index, 'diagnosa'] = diagnosa
        queue.to_csv('queue.csv', index=False)
        print("Diagnosa berhasil ditambahkan")
        input("Press Enter to continue...")
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to continue...")

def tampilkan_kamar(df):
        print("\nStatus Kamar:")
        print(df.to_string(index=False))

def check_in(df, nama_pasien, nomor_kamar):
    indeks_kamar = df[df["Nomor Kamar"] == nomor_kamar].index
    if not indeks_kamar.empty:
        indeks = indeks_kamar[0]
        if df.at[indeks, "Status"] == "Kosong":
            df.at[indeks, "Status"] = "Terisi"
            df.at[indeks, "Nama Pasien"] = nama_pasien
            df.to_csv("data_kamar.csv", index=False)
            print(f"Pasien '{nama_pasien}' telah check-in ke kamar {nomor_kamar}.")
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
    while True:
        print("\nMenu:")
        print("1. Tampilkan Status Kamar")
        print("2. Check-In Pasien")
        print("3. Check-Out Kamar")
        print("4. Keluar")

        pilihan = input("Pilih opsi: ")

        if pilihan == "1":
            tampilkan_kamar(daftar_kamar)

        elif pilihan == "2":
            nama_pasien = input("Masukkan nama pasien: ")
            try:
                nomor_kamar = int(input("Masukkan nomor kamar yang diinginkan: "))
                check_in(daftar_kamar, nama_pasien, nomor_kamar)
            except ValueError:
                print("Input tidak valid. Masukkan nomor kamar yang benar.")

        elif pilihan == "3":
            try:
                nomor_kamar = int(input("Masukkan nomor kamar untuk check-out: "))
                check_out(daftar_kamar, nomor_kamar)
            except ValueError:
                print("Input tidak valid. Masukkan nomor kamar yang benar.")

        elif pilihan == "4":
            print("Program selesai.")
            break

        else:
            print("Pilihan tidak valid. Silakan coba lagi.")


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

def pembayaran():
    print("Pembayaran menu - To be implemented")
    input("Press Enter to continue...")

# jaga jaga buat debug biar gk login melulu
#if __name__ == "__main__":
#    main_menu()
if __name__ == "__main__":
    login_menu
