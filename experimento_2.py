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

def calcula(tabela, numFatores, numReplicacoes):
    numTratamentos = 2 ** numFatores
    respostas = []

    print(f"\nInforme os dados experimentais:")
    for i in range(numTratamentos):
        linha = []
        print(f"Tratamento {i + 1}:")
        for j in range(numReplicacoes):
            while True:
                try:
                    valor = float(input(f"  Repetição {j + 1}: "))
                    linha.append(valor)
                    break
                except ValueError:
                    print("  Valor inválido. Tente novamente.")
        respostas.append(linha)

    df_respostas = pd.DataFrame(respostas, columns=[f"R{j+1}" for j in range(numReplicacoes)])
    df_respostas["Media"] = df_respostas.mean(axis=1)

    for i, row in df_respostas.iterrows():
        for j in range(numReplicacoes):
            tabela.loc[i, f"R{j+1}"] = row[f"R{j+1}"]

    tabela["Media"] = df_respostas["Media"]  

    todas_respostas = df_respostas.iloc[:, :-1].values.flatten()
    media_geral = todas_respostas.mean()
    SST = sum((y - media_geral) ** 2 for y in todas_respostas)

    ss_fatores = {}
    ss_interacao = {}

    for i in range(numFatores):
        fator = "ABCDE"[i]
        coluna = tabela[fator]
        soma = 0
        for nivel in [-1, 1]:
            indices = coluna[coluna == nivel].index
            media_nivel = df_respostas.loc[indices, "Media"].mean()
            soma += len(indices) * ((media_nivel - media_geral) ** 2)
        ss_fatores[f"SS{fator}"] = soma * numReplicacoes

    if numFatores == 2:
        ss_interacao["SSAB"] = 0
        for nivelA in [-1, 1]:
            for nivelB in [-1, 1]:
                indices = (tabela["A"] == nivelA) & (tabela["B"] == nivelB)
                media_interacao = df_respostas.loc[indices, "Media"].mean()
                ss_interacao["SSAB"] += len(indices) * ((media_interacao - media_geral) ** 2)
    
    print("\nResultados:")
    print(f"SST: {SST:.4f}")
    for fator, valor in ss_fatores.items():
        print(f"{fator}: {valor:.4f}")
    
    if ss_interacao:
        for interacao, valor in ss_interacao.items():
            print(f"{interacao}: {valor:.4f}")

    print("\nTabela com Respostas Experimentais e Médias:")
    print(tabela)

    return SST, ss_fatores, ss_interacao


numfat, numrepli = lerDadosEntrada()
tabela = createTable(numfat)
print(tabela)
SST, SS_fatores, SS_interacao = calcula(tabela, numfat, numrepli)
