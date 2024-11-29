import pandas as pd
import numpy as np
from datetime import datetime
import msvcrt
import os

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

def show_main_menu():
    clear_screen()
    print("\n=== Sistem Informasi Kesehatan ===")
    print("1. Data Pasien")
    print("2. Jadwal Dokter")
    print("3. Konsul dan Diagnosa")
    print("4. Ruang Rawat Inap")
    print("5. Resep Obat")
    print("6. Pembayaran")
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

if __name__ == "__main__":
    show_main_menu()
    main_menu()