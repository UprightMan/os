def is_in_list(broj, lista):
  for i in range(len(lista)):
    if lista[i] == broj:
      return 1
  return 0

brojevi = []
dupli_brojevi = []
a = input()
while a != "kraj":
  if is_in_list(a, brojevi) == 1: 
      brojevi.append(a)
      dupli_brojevi.append(a)
  else:
      brojevi.append(a)
  a = input()
print(brojevi, dupli_brojevi)
for x in range(len(brojevi)):
  if is_in_list(brojevi[x], dupli_brojevi) == 0:
    print(brojevi[x])
y = 0
for x in range(len(brojevi)):
  y = y + int(brojevi[x])
for x in range(len(dupli_brojevi)):
  y = y + int(dupli_brojevi[x])
print(y)