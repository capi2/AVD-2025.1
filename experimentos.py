entradaValida = 0
while(not entradaValida):
    print("Digite o número de fatores")
    print("O número de fatores precisa estar entre 2 e 5")
    try:
        numFatores = int(input())
    except ValueError:
        print("Valor inválido!")
    else:
        if(numFatores < 2 or numFatores > 5):
            print("Valores fora do range especificado!")
        else:
            print("Valor válido!")
            entradaValida = 1