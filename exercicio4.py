import numpy as np
import pandas as pd

def calcular(num_clientes, taxa_entrada, taxa_servico):
    tempo_chegada_relogio = 0
    tempos_espera = np.zeros(num_clientes)
    tempo_final_servico = 0
    tempo_inicio_servico = 0
    for i in range(num_clientes):
        tc = np.random.exponential(1/taxa_entrada)
        tempo_chegada_relogio += tc
        if(tempo_chegada_relogio < tempo_final_servico):
            tempos_espera[i] = tempo_final_servico - tempo_chegada_relogio
        tempo_inicio_servico = np.max([tempo_chegada_relogio, tempo_final_servico])
        tempo_servico = np.random.exponential(1/taxa_servico)
        tempo_final_servico = tempo_inicio_servico + tempo_servico
    return tempos_espera

def simular():
    taxa_entrada = 9.5
    taxa_servico = 10
    clientes = 10**3
    repeticoes = 30

    ro = taxa_entrada/taxa_servico
    valor_esperado = ro*(1/taxa_servico)/(1-ro)
    print(f"Valor esperado de tempo de espera: {valor_esperado}")

    tempos_medio = []
    bies = []
    for i in range(repeticoes):
        tempos = calcular(clientes, taxa_entrada, taxa_servico)
        tempo_medio = np.mean(tempos)
        tempos_medio.append(tempo_medio)
        bies.append(tempo_medio-valor_esperado)

    table = pd.DataFrame({
        "tempo_medio":tempos_medio,
        "bies":bies
    })

    print(f"Resultados para {repeticoes} simulações com {clientes} clientes!")
    print(table)
    print(f"Tempo medio global: {sum(table['tempo_medio'])/repeticoes}")
    print(f"Desvio-padrão dos tempos médios: {np.std(tempos_medio)}")
    print(f"Bies global: {sum(table['bies'])/repeticoes}")

simular()