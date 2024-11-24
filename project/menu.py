def main():
    while True:
        print ("menu 1")
        print ("menu 2")
        print ("menu 3")
        print ("menu 4")
        print ("menu 5")
    pilihan = int(input())
    if pilihan in [0,1,2,3,4,5]:
        function(pilihan)
    else:
        print("pilihan tidak ditemukan")
    