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
                print("[ERRO] Valor fora do range especificado! Tente de novo!")
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
                print("[ERRO] Valor fora do range especificado! Tente de novo!")
            else:
                print("Valor válido!")
                numReplicacoesValido = 1
    return numFatores, numReplicacoes

def criarCombinacoes(numFatores):
    base = "ABCDE"
    s = base[:numFatores]
    result = []
    for r in range(1, numFatores + 1):
        result.extend([''.join(c) for c in combinations(s, r)])
    return ["I"] + result

def criarColunas(numFatores):
    columns = []
    numColumns = 2**numFatores
    columns.append([1 for x in range(numColumns)])
    metade = 1
    for i in range(numFatores):
        c= []
        um = -1
        atingiu_metade = 0
        for j in range(numColumns):
            c.append(um)
            atingiu_metade += 1
            if(atingiu_metade == metade):
                um = um*-1
                atingiu_metade = 0
        columns.append(c)
        metade = metade*2
    return columns

def criarTabela(numFatores):
    print(f"Criando tabela de sinais com {numFatores} fatores")
    d = {}
    comb = criarCombinacoes(numFatores)
    cols = criarColunas(numFatores)
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

def lerMedicoes(tabela, numFatores, numReplicacoes):
    numTratamentos = 2 ** numFatores
    respostas = []

    print(f"\nInforme os dados experimentais:")
    for i in range(numTratamentos):
        linha = []
        print(f"Experimento {i + 1}:")
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

    erros = {}
    for k in range(numReplicacoes):
        col = tabela[f"R{k+1}"]
        res = col - tabela["Media"]
        erros[f"e{k+1}"] = res
    
    df = pd.DataFrame(erros)
    tabela = pd.concat([tabela, df], axis=1)
    print("\nTabela atualizada com medições!\n")
    return tabela

def calcularResultados(tabela, numFatores, numReplicacoes):
    polinomio = []
    numCols = 2**numFatores
    for i in range(numCols):
        total = 0
        total += sum(tabela.iloc[:,i]*tabela["Media"])
        polinomio.append(total)
    polinomio = [x/numCols for x in polinomio]

    SSE = 0
    for i in range(numReplicacoes):
        col = tabela[f"e{i+1}"]
        SSE += sum([e**2 for e in col])
    
    efeitos = [x**2 for x in polinomio[1:]]
    SST = numCols*numReplicacoes*sum(efeitos) + SSE
    
    nomeColunas = [x for x in tabela.columns[1:numCols]]
    resultados = {}
    for i in range(len(nomeColunas)):
        res = 0
        res = numCols*numReplicacoes*efeitos[i]/SST
        resultados[nomeColunas[i]] = res*100
    
    return resultados, SST, SSE
  
def main():
    numfat, numrepli = lerDadosEntrada()

    tabela = criarTabela(numfat)
    print(tabela)

    tabela = lerMedicoes(tabela, numfat, numrepli)
    print(tabela)

    resultados, sst, sse = calcularResultados(tabela, numfat, numrepli)
    print("\nResultados dos Experimentos")
    print(f"\nSST dos experimentos = {sst}")
    print(f"SSE = {sse}\n")
    maior = 0
    col = "nada"
    for key, value in resultados.items():
        if(value > maior):
            maior = value
            col = key
        print(f"Contribuição de {key} = {value:.3f} %")
    print(f"Erro = {(sse/sst)*100:.3f} %")
    print(f"\nMaior contribuição: {col} com {maior:.3f} %")

if __name__ == "__main__":
    main()
