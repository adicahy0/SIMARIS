# antrian
import datetime
def input():
    while True:
        Nama = str(input())
        for huruf in Nama:
            if huruf.isdigit():
                print ("nama anda berisi nomor")
                break
        if len(huruf) > 3:
            print ("terlalu pendek")
        else:
            break
    while True:  #TODO :value exception for non int input
        NIK = int(input())
        if len(NIK) >= 16:
            print ("waw")
            break
    while True:
        gender = str(input)
        for huruf in gender:
            if huruf.isdigit():
                print ("isi dengan F / M kapital")
                break
        if len(gender) >= 1:
            print("inputan terlau panjang")
        elif not gender:
            print("inputan kosong")
        else:
            break
    while True:
        current_time = datetime.now()
        waktu = input(": ") or current_time.strftime("%m-%d %H:%M")