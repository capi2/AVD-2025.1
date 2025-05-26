import numpy as np
from scipy import stats

def simular(num_clientes, taxa_entrada, taxa_servico):
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

def analisar(num_clientes, tempos_espera, taxa_entrada, taxa_servico, confianca):
    print(f"\tResultado para {num_clientes} clientes!")
    
    tempo_medio_espera = np.mean(tempos_espera)
    print(f"Tempo Medio de Espera: {tempo_medio_espera}")
    
    ro = taxa_entrada/taxa_servico
    valor_esperado = ro*(1/taxa_servico)/(1-ro)
    print(f"Valor esperado: {valor_esperado}")

    z = stats.norm.ppf(confianca)
    s = np.std(tempos_espera, ddof=1)

    limite_superior = float(tempo_medio_espera + z * s/num_clientes)
    limite_inferior = float(tempo_medio_espera - z * s/num_clientes)

    print(f"Intervalo de Confiança: {limite_inferior, limite_superior}")

def resultados():
    taxa_entrada = 9
    taxa_servico = 10
    clientes = [10**3, 10**5, 10**7]
    confianca = 0.95

    for i in clientes:
        tempos = simular(i, taxa_entrada, taxa_servico)
        analisar(i, tempos, taxa_entrada, taxa_servico, confianca)

resultados()