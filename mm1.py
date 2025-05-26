import numpy as np
from scipy import stats

def simular_streaming(num_clientes, taxa_entrada, taxa_servico):
    tempo_chegada_relogio = 0
    tempo_final_servico = 0

    soma = 0
    soma_quadrados = 0

    for i in range(1, num_clientes + 1):
        tc = np.random.exponential(1 / taxa_entrada)
        tempo_chegada_relogio += tc

        if tempo_chegada_relogio < tempo_final_servico:
            espera = tempo_final_servico - tempo_chegada_relogio
        else:
            espera = 0

        tempo_inicio_servico = max(tempo_chegada_relogio, tempo_final_servico)
        tempo_servico = np.random.exponential(1 / taxa_servico)
        tempo_final_servico = tempo_inicio_servico + tempo_servico

        soma += espera
        soma_quadrados += espera**2

        if i % 10_000_000 == 0:
            print(f"{i:,} clientes processados...")

    media = soma / num_clientes
    variancia = (soma_quadrados - num_clientes * media**2) / (num_clientes - 1)
    return media, np.sqrt(variancia)

def analisar_streaming(num_clientes, media, desvio, taxa_entrada, taxa_servico, confianca):
    print(f"\nResultado para {num_clientes} clientes:")

    print(f"Tempo Médio de Espera: {media:.4f}")
    
    ro = taxa_entrada / taxa_servico
    valor_esperado = ro * (1 / taxa_servico) / (1 - ro)
    print(f"Valor Teórico Esperado: {valor_esperado:.4f}")

    z = stats.norm.ppf(confianca)
    erro = z * desvio / np.sqrt(num_clientes)

    print(f"Intervalo de Confiança ({int(confianca*100)}%): ({media - erro:.4f}, {media + erro:.4f})")

def resultados():
    taxa_entrada = 9
    taxa_servico = 10
    num_clientes = 10**7
    confianca = 0.95

    media, desvio = simular_streaming(num_clientes, taxa_entrada, taxa_servico)
    analisar_streaming(num_clientes, media, desvio, taxa_entrada, taxa_servico, confianca)

if __name__ == "__main__":
    resultados()

