def lerDadosEntrada():
    numFatoresValido = 0
    while(not numFatoresValido):
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
                numFatoresValido = 1

    numReplicacoesValido = 0
    while(not numReplicacoesValido):
        print("Digite o número de replicacoes")
        print("O número de fatores precisa estar entre 1 e 3")
        try:
            numReplicacoes = int(input())
        except ValueError:
            print("Valor inválido!")
        else:
            if(numReplicacoes < 1 or numReplicacoes > 3):
                print("Valores fora do range especificado!")
            else:
                print("Valor válido!")
                numReplicacoesValido = 1
    return numFatores, numReplicacoes
