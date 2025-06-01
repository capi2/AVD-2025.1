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

    return tempo_medio_espera, largura_intervalo_confianca, limite_inferior, limite_superior

def calcular(taxa_entrada, taxa_servico, confianca, precisao_relativa):
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
            tempo_medio_espera, largura, lim_inf, lim_sup = analisar(clientes, tempos_espera, confianca)
            if largura/tempo_medio_espera <= precisao_relativa:
                parar_simulacao = True
    return tempo_medio_espera, clientes, lim_inf, lim_sup

def simular():
    taxa_entrada = 9
    taxa_servico = 10
    confianca = 0.95
    precisao_relativa = 0.05
    
    tempo_medio, clientes, lim_inf, lim_sup = calcular(taxa_entrada, taxa_servico, confianca, precisao_relativa)
    largura = lim_sup-lim_inf

    print(f"\tResultado para {clientes} clientes!")
    print(f"Tempo medio de espera: {tempo_medio}")
    print(f"Intervalo de Confiança: {lim_inf, lim_sup}")
    print(f"Largura intervalo de confiança {largura}")

simular()