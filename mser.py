import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def calcular(num_clientes, taxa_entrada, taxa_servico):
    tempo_chegada_relogio = 0
    tempos_espera = np.zeros(num_clientes)
    tempo_final_servico = 0
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

def eliminar_transiente_mser(tempos):
    lista_z = []
    lista_mser = []
    z = 0
    cont = 0
    k = int(len(tempos)/5)
    for i in range(len(tempos)):
        z += tempos[i]
        cont += 1
        if cont == 5:
            lista_z.append(z/5)
            z = 0
            cont = 0
    d = 0
    while d < k/2:
        j = d+1
        z_medio = np.mean(lista_z[j:])
        var_z = np.sum((lista_z[j:] - z_medio) ** 2)
        mser = np.sqrt(var_z/(k-d))
        lista_mser.append(mser)
        d += 1
    d_asterisco = np.argmin(lista_mser)
    return tempos[d_asterisco:]

def simular():
    taxa_entrada = 9.5
    taxa_servico = 10
    n = 1000
    repeticoes = 30
    confianca = 0.95
    precisao = 0.05

    ro = taxa_entrada / taxa_servico
    valor_esperado = ro * (1/taxa_servico) / (1 - ro)
    print(f"Valor esperado de tempo de espera: {valor_esperado:.5f}")

    metodos = ['Conway', 'Fishman', 'MSER-5Y']
    medias = []
    erros = []
    replicas_usadas = []

    for metodo in metodos:
        tempos_medio = []
        replicas = 0

        while True:
            tempos = calcular(n, taxa_entrada, taxa_servico)

            if metodo == 'Conway':
                idx = eliminar_transiente_conway(tempos)
                if idx + n > len(tempos):
                    tempos = np.concatenate([tempos, calcular(n, taxa_entrada, taxa_servico)])
                tempos_estacionario = tempos[idx:idx + n]
            elif metodo == 'Fishman':
                idx = eliminar_transiente_fishman(tempos, k=7)
                if idx + n > len(tempos):
                    tempos = np.concatenate([tempos, calcular(n, taxa_entrada, taxa_servico)])
                tempos_estacionario = tempos[idx:idx + n]
            elif metodo == 'MSER-5Y':
                tempos_estacionario = eliminar_transiente_mser(tempos)
                if len(tempos_estacionario) < n:
                    tempos_estacionario = np.concatenate([tempos_estacionario, calcular(n - len(tempos_estacionario), taxa_entrada, taxa_servico)])

            tempo_medio = np.mean(tempos_estacionario)
            tempos_medio.append(tempo_medio)
            replicas += 1

            if metodo != 'MSER-5Y' and replicas == repeticoes:
                break
            if metodo == 'MSER-5Y' and replicas >= 10:
                media = np.mean(tempos_medio)
                s = np.std(tempos_medio, ddof=1)
                z = stats.norm.ppf((1 + confianca) / 2)
                h = z * s / np.sqrt(replicas)
                if h / media <= precisao:
                    break

        media_global = np.mean(tempos_medio)
        desvio = np.std(tempos_medio, ddof=1)
        z = stats.norm.ppf((1 + confianca) / 2)
        erro = z * desvio / np.sqrt(replicas)

        medias.append(media_global)
        erros.append(erro)
        replicas_usadas.append(replicas)

        print(f"\n{metodo}: média = {media_global:.5f}, IC ± {erro:.5f}, réplicas = {replicas}")

    nomes_com_replicas = [f"{metodo}\n(n° clientes: {rep})" for metodo, rep in zip(metodos, replicas_usadas)]

    plt.figure(figsize=(10, 6))
    plt.bar(nomes_com_replicas, medias, yerr=erros, capsize=10, color=['skyblue', 'salmon', 'lightgreen'])
    plt.axhline(y=valor_esperado, color='gray', linestyle='--', label='Valor esperado teórico')
    plt.ylabel("Tempo médio de espera")
    plt.title("Comparação entre métodos de eliminação de transiente")
    plt.legend()
    plt.tight_layout()
    plt.show()

simular()
