import time, signal, sys

TEKUCI_PRIORITET = 0
PRIORITET = [0,0,0,0,0,0]
OZNAKA_CEKANJA = [0,0,0,0,0,0]

def ispisi_pojavu_signala ( prioritet ): # prioritet u rangu 1-5
	print ( '\t' + '- ' * prioritet + 'X ' + '- ' * (5-prioritet) )
def ispisi_pocetak_obrade_signala ( prioritet ):
	print ( '\t' + '- ' * prioritet + 'P ' + '- ' * (5-prioritet) )
def ispisi_kraj_obrade_signala ( prioritet ):
	print ( '\t' + '- ' * prioritet + 'K ' + '- ' * (5-prioritet) )
def ispisi_korak_obrade_signala ( prioritet, korak ):
	print ( '\t' + '- ' * prioritet + str(korak) + ' ' + '- ' * (5-prioritet) )
def ispisi_korak_obrade_glavnog_programa ( korak ):
	print ( '\t' + str(korak%10) + ' -' * 5 )

def simulacija_obrade_prekida ( prioritet ):
	ispisi_pocetak_obrade_signala ( prioritet )
	for korak in range(1,6):
		ispisi_korak_obrade_signala ( prioritet, korak )
		time.sleep(1)
	ispisi_kraj_obrade_signala ( prioritet )

def prekidna_rutina ( signal, frame ):
	global TEKUCI_PRIORITET
	prioritet = int(input("Unesi prioritet prekida: "))
	if prioritet == 10:
		print ( "\nZavršavam rad" )
		sys.exit(1)

	ispisi_pojavu_signala ( prioritet )
	OZNAKA_CEKANJA[prioritet] = 1

	while prioritet > TEKUCI_PRIORITET:
		OZNAKA_CEKANJA[prioritet] = 0
		PRIORITET[prioritet] = TEKUCI_PRIORITET
		TEKUCI_PRIORITET = prioritet
		simulacija_obrade_prekida ( prioritet )
		j = TEKUCI_PRIORITET
		prioritet = 0
		TEKUCI_PRIORITET = 0
		for j in range (0, j):
			if OZNAKA_CEKANJA[j]!=0:
				prioritet = j
	# ...

def main():
	print("\tG 1 2 3 4 5")

	signal.signal ( signal.SIGINT, prekidna_rutina )

	for korak in range(100):
		ispisi_korak_obrade_glavnog_programa ( korak )
		time.sleep(1)

if __name__ == "__main__":
	main()