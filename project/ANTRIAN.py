import pandas as pd
import csv
from datetime import datetime
import numpy as np
queue = pd.DataFrame()
def antrian():
    while True:
        Nama = str(input("nama"))
        for huruf in Nama:
            if huruf.isdigit():
                print ("nama anda berisi nomor")
                break
        if len(Nama) > 3:
            print ("terlalu pendek")
        else:
            break
    while True:  #TODO :value exception for non int input
        NIK = str(input("nik"))
        if len(NIK) > 16:
            print ("waw")
        else:
            break
    while True:
        gender = str(input("gender"))
        for huruf in gender:
            if huruf.isdigit():
                print ("isi dengan F / M kapital")
        if len(gender) > 1:
            print("inputan terlau panjang")
        elif not gender:
            print("inputan kosong")
        else:
            break
    while True:
        current_time = datetime.now()
        waktu = input(": ") or current_time.strftime("%m-%d %H:%M")
        break
    temp = pd.DataFrame ({
    'Nama'    : [Nama],
    'Nik'     : [NIK],
    'gender'  : [gender],
    'date'    : [waktu],
    'diagnosa': [np.nan],
    'obat'    : [np.nan],
    'ruangan' : [np.nan]
    })
    pd.concat([queue,temp], ignore_index=0)
    queue = pd.read_csv('queue.csv')
    

#remove
def rm(d,e):
    d.drop(index=e, inplace=True)
    d.to_csv(f"{d}.csv")
#edit
def edit(a,b,c,d):
    a.iat[b,c] = d
    a.to_csv(f"{a}.csv")
 
while True:
    print(queue)
    x = int(input(""))
    if x == 1:
        antrian()
    elif x == 2:
        index_antrian = int(input)
        rm(queue, index_antrian)
    elif x ==3:
        index_X = int(input)
        index_y = int(input)
        user_input = input("Enter something: ") or queue.iloc(index_X,index_y)