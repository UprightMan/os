import time, threading, signal

sem = threading.Semaphore ( value = 1 ) #mutex
sem1 = threading.Semaphore ( value = 0 ) #radi li barber na klijentu
sem2 = threading.Semaphore(value=1) #klijent odlazi
sleep_sem = threading.Semaphore(value=0) #barber spava
sem3 = threading.Semaphore(value=0) #klijent pozvan

red = []
sleeping = 0
otvoren = False
stolac = 0

def ispisi_stanje(opis):
    global stolac, otvoren
    if otvoren: print ( "OTVORENO  ", end="" )
    else: print ( "ZATVORENO ", end="" )
    print ( "stolac: " + str(stolac), end="" )
    cekaona = red + ["-"] * (3-len(red))
    cekaona = " ".join([str(i) for i in cekaona])
    print ( " red: " + cekaona, end="" )
    print ( " [ " + opis + " ]" )

def frizerka ():
    # uđi u kritični odsječak
    global otvoren
    global stolac
    global red, sleeping
    sem.acquire()
    otvoren = True # postavi oznaku OTVORENO
    print("frizerka: otvaram salon")
    # izađi iz kritičnog odsječka
    sem.release()
    while not prekini: # nije zahtjevan prekid izvođenja
        # uđi u kritični odsječak
        sem.acquire()
        if len(red) > 0: # ima klijenata
            ispisi_stanje("frizerka: krecem s radom na frizuri")
            # pozovi idućeg klijenta
            sem3.release()
            sem.release()
            # izađi iz kritičnog odsječka
            time.sleep(5)
            sem1.release()
            # kraj rada na frizuri
        elif otvoren:
            stolac = 0
            ispisi_stanje("frizerka: spavam")
            # izađi iz kritičnog odsječka
            sem.release()
            sleep_sem.acquire()
        else:
            stolac = 0
            ispisi_stanje("frizerka: zavrsavam s radom")
            # izađi iz kritičnog odsječka
            sem.release()
            break
    sem.release()

def klijent (id):
    global otvoren
    global stolac
    global red, sleeping
    sem.acquire() #krit
    if otvoren and len(red) < 3:
        red.append(id)
        ispisi_stanje("klijent " + str(id) + ": dosao")
        if stolac == 0:
            sleep_sem.release() #wakeupcall
        sem.release()
        # izađi iz kritičnog odsječka
        # čekaj da te frizerka pozove
        sem2.acquire()
        sem3.acquire()
        # čekaj da prethodni klijent ode
        if prekini: return
        # uđi u kritični odsječak
        sem.acquire()
        stolac = id
        red.remove(id)
        ispisi_stanje("klijent " + str(id) + ": radi mi frizuru")       # čekaj da frizura bude gotova
        sem.release()
        sem1.acquire()
        sem.acquire()# uđi u kritični odsječak
        ispisi_stanje("klijent " + str(id) + ": frizura gotova")
        sem2.release()
    elif not otvoren:
        ispisi_stanje("klijent " + str(id) + ": salon zatvoren")
    else:
        ispisi_stanje("klijent " + str(id) + ": nema mjesta")
    sem.release()
    # izađi iz kritičnog odsječka

def signal_kraj(sig_num, frame):
    global prekini
    ispisi_stanje("Kraj")
    prekini = True
    sleep_sem.release()
    sem1.release()
    sem2.release()

def main():
    global prekini, otvoren
    signal.signal(signal.SIGINT, signal_kraj)
    prekini= False
    frizerka_dretva = threading.Thread(target = frizerka)
    frizerka_dretva.start()
    for i in range(1, 21):
        klijent_dretva = threading.Thread(target=klijent, args=(i,))
        klijent_dretva.start()
        time.sleep(2)
    sem.acquire()
    otvoren = False
    sem.release()
    for i in range(21, 24):
        klijent_dretva = threading.Thread(target=klijent, args=(i,))
        klijent_dretva.start()
        time.sleep(2)
if __name__ == "__main__":
    main()