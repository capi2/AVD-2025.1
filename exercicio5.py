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
        if tempo_chegada_relogio < tempo_final_servico:
            tempos_espera[i] = tempo_final_servico - tempo_chegada_relogio
        tempo_inicio_servico = max(tempo_chegada_relogio, tempo_final_servico)
        tempo_servico = np.random.exponential(1/taxa_servico)
        tempo_final_servico = tempo_inicio_servico + tempo_servico
    return tempos_espera

def eliminar_transiente_conway(tempos):
    for i in range(2, len(tempos)):
        subserie = tempos[:i]
        atual = tempos[i]
        if not (atual == max(subserie) or atual == min(subserie)):
            return i 
    return len(tempos)

def eliminar_transiente_fishman(tempos, k=7):
    media = np.mean(tempos)
    cruzamentos = 0
    for i in range(1, len(tempos)):
        if (tempos[i-1] - media) * (tempos[i] - media) < 0:
            cruzamentos += 1
        if cruzamentos >= k:
            return i
    return len(tempos)

def simular():
    taxa_entrada = 9.5
    taxa_servico = 10
    n = 10**3
    repeticoes = 30
    ro = taxa_entrada / taxa_servico
    valor_esperado = ro * (1/taxa_servico) / (1 - ro)
    print(f"Valor esperado de tempo de espera: {valor_esperado:.5f}")

    resultados = []

    for metodo in ['Conway', 'Fishman']:
        tempos_medio = []
        bies = []
        for _ in range(repeticoes):
            tempos = calcular(2 * n, taxa_entrada, taxa_servico)
            
            if metodo == 'Conway':
                idx = eliminar_transiente_conway(tempos)
            else:
                idx = eliminar_transiente_fishman(tempos, k=7)

            if idx + n > len(tempos):
                tempos = np.concatenate([tempos, calcular(n, taxa_entrada, taxa_servico)])

            tempos_estacionario = tempos[idx:idx + n]
            tempo_medio = np.mean(tempos_estacionario)
            bias = tempo_medio - valor_esperado

            tempos_medio.append(tempo_medio)
            bies.append(bias)

        table = pd.DataFrame({
            "tempo_medio": tempos_medio,
            "bias": bies
        })

        print(f"\nResultados para {repeticoes} simulações com {n} clientes usando {metodo}:")
        print(table)
        print(f"Tempo médio global: {np.mean(tempos_medio):.5f}")
        print(f"Desvio-padrão dos tempos médios: {np.std(tempos_medio):.5f}")
        print(f"Viés global: {np.mean(bies):.5f}")

        resultados.append((metodo, table))

simular()
