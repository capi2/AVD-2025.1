import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t

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
    return tempos_espera, tempo_chegada_relogio, tempo_final_servico

def adicionar_observacoes(tempos_espera, clientes_adicionais, taxa_entrada, taxa_servico, tempo_chegada_relogio, tempo_final_servico):
    novos_tempos_espera = np.zeros(clientes_adicionais)
    for i in range(clientes_adicionais):
        tc = np.random.exponential(1/taxa_entrada)
        tempo_chegada_relogio += tc
        if tempo_chegada_relogio < tempo_final_servico:
            novos_tempos_espera[i] = tempo_final_servico - tempo_chegada_relogio
        tempo_inicio_servico = max(tempo_chegada_relogio, tempo_final_servico)
        tempo_servico = np.random.exponential(1/taxa_servico)
        tempo_final_servico = tempo_inicio_servico + tempo_servico
    print(f"{clientes_adicionais} Clientes adicionados para {taxa_entrada} clientes por segundo!")
    return np.concatenate([tempos_espera, novos_tempos_espera]), tempo_chegada_relogio, tempo_final_servico

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
    taxa_entrada = [7, 8, 9, 9.5]
    taxa_servico = 10
    n_clientes = 1000
    confianca = 0.95
    precisao = 0.05
    B = 20
    beta = 1.44
    lista_valor_esperado = []

    for clientes_por_segundo in taxa_entrada:
        ro = clientes_por_segundo / taxa_servico
        valor_esperado = ro * (1/taxa_servico) / (1 - ro)
        lista_valor_esperado.append(valor_esperado)
        print(f"Taxa de entrada = {clientes_por_segundo} e valor esperado de tempo de espera: {valor_esperado:.5f}")
    
    lista_tempo_medio = []
    lista_intervalo_confianca = []
    for clientes_por_segundo in taxa_entrada:
        tempos_espera, tempo_chegada_relogio, tempo_final_servico = calcular(n_clientes, clientes_por_segundo, taxa_servico)
        tempos_espera = eliminar_transiente_mser(tempos_espera)
        teste_passou = False
        M = 5
        while not teste_passou:
            lista_y = []
            bloco = []
            inicio = 0
            fim = M
            N = B*M
            if N <= len(tempos_espera):
                for i in range(len(tempos_espera)-M+1):
                    for j in range(inicio,fim):
                        bloco.append(tempos_espera[j])
                        if(len(bloco) == M):
                            lista_y.append(np.mean(bloco))
                            bloco = []
                            inicio += 1
                            fim += 1
                lista_ri = []
                for i in range(len(lista_y)):
                    ri = lista_y[i]
                    qtde_ri = 0
                    for j in range(len(lista_y)):
                        if(lista_y[j] <= ri and i != j):
                            qtde_ri += 1
                    lista_ri.append(qtde_ri)
                r_medio = np.sum(lista_ri)/B
                var_r = [(r-r_medio)**2 for r in lista_ri]
                acum = 0
                for k in range(len(lista_ri)-1):
                    acum += (lista_ri[k]-lista_ri[k+1])**2
                soma_var_r = np.sum(var_r)
                if soma_var_r == 0:
                    M += 1
                    continue
                RVN = acum/soma_var_r
                if RVN < beta:
                    media_global = np.mean(lista_y)
                    var = np.var(lista_y)
                    b = len(lista_y)
                    df = b - 1
                    alpha = 1 - confianca
                    t_value = t.ppf(1 - alpha/2, df)
                    limite_superior = float(media_global + t_value * np.sqrt(var/len(lista_y)))
                    limite_inferior = float(media_global - t_value * np.sqrt(var/len(lista_y)))
                    largura_intervalo_confianca = limite_superior - limite_inferior
                    h = largura_intervalo_confianca/2
                    if h/media_global <= precisao:
                        lista_tempo_medio.append(media_global)
                        lista_intervalo_confianca.append((limite_inferior,limite_superior))
                        M = 5
                        teste_passou = True
                    else:
                        M += 1
                        tempos_espera, tempo_chegada_relogio, tempo_final_servico = adicionar_observacoes(tempos_espera, len(lista_y)*M, clientes_por_segundo, taxa_servico, tempo_chegada_relogio, tempo_final_servico)
                else:
                    M += 1
            else:
                print("Simulacao falhou, nao ha observacoes o suficiente! gerando novos dados...")
                tempos_espera, tempo_chegada_relogio, tempo_final_servico = adicionar_observacoes(tempos_espera, len(lista_y)*M, clientes_por_segundo, taxa_servico, tempo_chegada_relogio, tempo_final_servico)
                M = 5
    print(lista_tempo_medio)
    print(lista_intervalo_confianca)

    inferiores = [media - ic[0] for media, ic in zip(lista_tempo_medio, lista_intervalo_confianca)]
    superiores = [ic[1] - media for media, ic in zip(lista_tempo_medio, lista_intervalo_confianca)]
    yerr = np.array([inferiores, superiores])

    plt.figure(figsize=(8, 5))
    plt.bar(taxa_entrada, lista_tempo_medio, yerr=yerr, width=0.4, capsize=10,
            color=['blue', 'green', 'red', 'yellow'])

    cores = ['blue', 'green', 'red', 'yellow']

    for i, (val_esp, cor) in enumerate(zip(lista_valor_esperado, cores)):
        plt.axhline(y=val_esp, linestyle='--', color=cor)

    plt.ylabel("Tempo médio de espera")
    plt.xlabel("Taxa de chegada (λ)")
    plt.title("Resultados para o método OBM")
    plt.tight_layout()
    plt.show()

simular()

