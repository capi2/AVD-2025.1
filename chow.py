import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

def analisar(num_clientes, tempos_espera, confianca):
    tempo_medio_espera = np.mean(tempos_espera)

    z = stats.norm.ppf((1 + confianca) / 2)
    s = np.std(tempos_espera, ddof=1)

    limite_superior = float(tempo_medio_espera + z * s/np.sqrt(num_clientes))
    limite_inferior = float(tempo_medio_espera - z * s/np.sqrt(num_clientes))
    largura_intervalo_confianca = limite_superior - limite_inferior

    return tempo_medio_espera, largura_intervalo_confianca

def calcular(taxa_entrada, taxa_servico, d, confianca):
    tempo_chegada_relogio = 0
    tempos_espera = []
    tempo_final_servico = 0
    tempo_inicio_servico = 0
    parar_simulacao = False
    clientes = 0
    while not parar_simulacao:
        tc = np.random.exponential(1/taxa_entrada)
        tempo_chegada_relogio += tc
        clientes += 1

        if(tempo_chegada_relogio < tempo_final_servico):
            tempos_espera.append(tempo_final_servico - tempo_chegada_relogio)
        else:
            tempos_espera.append(0)

        tempo_inicio_servico = np.max([tempo_chegada_relogio, tempo_final_servico])
        tempo_servico = np.random.exponential(1/taxa_servico)
        tempo_final_servico = tempo_inicio_servico + tempo_servico

        if clientes >= 30:
            tempo_medio_espera, largura = analisar(clientes, tempos_espera, confianca)
            if largura <= 2*d:
                parar_simulacao = True
    print(f"\tResultado para {clientes} clientes!")
    print(f"Tempo medio de espera: {tempo_medio_espera}")
    return tempo_medio_espera, clientes

def simular():
    taxa_entrada = 9
    taxa_servico = 10
    d = [1, 0.5, 0.1, 0.05]
    confianca = 0.95

    tempos_medio = []
    labels = []
    for i in d:
        tempo_medio, clientes = calcular(taxa_entrada, taxa_servico, i, confianca)
        tempos_medio.append(tempo_medio)
        labels.append(f"d={i}(n={clientes})")
    plt.bar(labels, tempos_medio)
    plt.xlabel('d e Número de clientes (n)')
    plt.ylabel('Tempo Médio de Espera')
    plt.title('Resultados')
    plt.show()

simular()