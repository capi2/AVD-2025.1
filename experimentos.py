import pandas as pd
from itertools import combinations

def lerDadosEntrada():
    numFatoresValido = 0
    while(not numFatoresValido):
        print("Digite o número de fatores")
        print("O número de fatores precisa estar entre 2 e 5")
        try:
            numFatores = int(input())
        except ValueError:
            print("[ERRO] Valor inválido! Tente de novo!")
        else:
            if(numFatores < 2 or numFatores > 5):
                print("[ERRO] Valores fora do range especificado! Tente de novo!")
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
            print("[ERRO] Valor inválido! Tente de novo!")
        else:
            if(numReplicacoes < 1 or numReplicacoes > 3):
                print("[ERRO] Valores fora do range especificado! Tente de novo!")
            else:
                print("Valor válido!")
                numReplicacoesValido = 1
    return numFatores, numReplicacoes

def createCombinations(numFatores):
    base = "ABCDE"
    s = base[:numFatores]
    result = []
    for r in range(1, numFatores + 1):
        result.extend([''.join(c) for c in combinations(s, r)])
    return ["I"] + result

def createColumns(numFatores):
    columns = []
    numColumns = 2**numFatores
    columns.append([1 for x in range(numColumns)])
    metade = numColumns//2
    for i in range(numFatores):
        c= []
        um = 1
        atingiu_metade = 0
        for j in range(numColumns):
            c.append(um)
            atingiu_metade += 1
            if(atingiu_metade == metade):
                um = um*-1
                atingiu_metade = 0
        columns.append(c)
        metade = metade//2
    return columns

def createTable(numFatores):
    print(f"Criando tabela com {numFatores} fatores")
    d = {}
    comb = createCombinations(numFatores)
    cols = createColumns(numFatores)
    for i in range(numFatores+1):
        d[comb[i]] = cols[i]
    table = pd.DataFrame(d)
    for j in range(numFatores+1,len(comb)):
        letters = [x for x in comb[j]]
        res_table = [1 for x in range(len(comb))]
        for i in range(len(letters)):
            res_table *= table[letters[i]]
        table[comb[j]] = res_table
    return table

numfat, numrepli = lerDadosEntrada()
table = createTable(numfat)
print(table)
