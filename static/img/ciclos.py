

comidas=["pollo","pizza","carne","hamburguesa"]
print("quieres? ")
for comida in comidas:
    if comida== "pollo":
        continue
    print(f" *{comida}")




print("tienes? ")
for comida in comidas:
    if comida== "pollo":
        print(f" *{comida}")
        break 



count=0
print("\n\ncomidas \n")
while count < 4:
    print(comidas[count])
    count=count+1




    