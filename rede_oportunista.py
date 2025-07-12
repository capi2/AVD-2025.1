import math
import numpy as np

class No:
    def __init__(self, id, data, hora, localizacao, bateria, memoria_interna):
        self.id = id
        self.data = data
        self.hora = hora
        self.localizacao = localizacao
        self.bateria = bateria
        self.memoria_interna = memoria_interna
    
    def leituras(self):
        return len(self.data)
    
def read_dataset(dataset):
    nos = []
    with open(dataset, "r") as file:
        print("Efetuando leitura de dados do dataset")
        line = file.readline()
        id = "1"
        data = []
        hora = []
        localizacao = []
        bateria = []
        mem_interna = []
        while line:
            line = line.split(";")
            if id == line[0]:
                data.append(line[1])
                hora.append(line[2])
                localizacao.append(line[3])
                bateria.append(line[4])
                mem_interna.append(line[5])
            else:
                no = No(id, data, hora, localizacao, bateria, mem_interna)
                nos.append(no)
                id = line[0]
                data = []
                hora = []
                localizacao = []
                bateria = []
                mem_interna = []
                data.append(line[1])
                hora.append(line[2])
                localizacao.append(line[3])
                bateria.append(line[4])
                mem_interna.append(line[5])
            line = file.readline()
    no = No(id, data, hora, localizacao, bateria, mem_interna)
    nos.append(no)
    print("Dataset lido com sucesso")
    file.close()
    return nos

def haversine(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371000
    return c * r

def encontrarLinha(nos, id_linha):
    i = 0
    ultima_pos = 0
    pos = nos[i].leituras()
    while True:
        if pos >= id_linha:
            posicao = id_linha - ultima_pos - 1
            return nos[i].id, nos[i].data[posicao], nos[i].hora[posicao], nos[i].localizacao[posicao], nos[i].bateria[posicao], nos[i].memoria_interna[posicao]
        else:
            i += 1
            ultima_pos = pos
            pos += nos[i].leituras()

def converter_hora(hora):
    h, m, s = hora.split(':')
    return int(h)*3600 + int(m)*60 + int(s)

def bateria_media(nos):
    bateria = 0
    for no in nos:
        for i in range(no.leituras()):
            bateria += int(no.bateria[i])
    return bateria/112554
    
def repassar_mensagem_n_egoista(nos, id1, id2, data1, hora1, lat1, lon1, bateria1, tolerancia_tempo, R, file):
    id_temp = id1
    data_temp = data1
    hora_temp = hora1
    lat_temp = lat1
    lon_temp = lon1
    bateria_temp = bateria1
    saltos = 0
    tempo = converter_hora(hora_temp)
    tempo_final_tolerancia = tempo + tolerancia_tempo
    tempo_inicio = tempo
    for j in range(len(nos)):
        for i in range(nos[j].leituras()):
            lat, lon = nos[j].localizacao[i].split(",")
            if nos[j].data[i] == data_temp and tempo_inicio <= converter_hora(nos[j].hora[i]) and converter_hora(nos[j].hora[i]) <= tempo_final_tolerancia and haversine(lat_temp, lon_temp, float(lat), float(lon)) <= R and id_temp != nos[j].id:
                file.write(f"Nó {nos[j].id} disponível! data: {nos[j].data[i]} hora: {nos[j].hora[i]} dist: {haversine(lat_temp, lon_temp, float(lat), float(lon))} | {id_temp} --> {nos[j].id}\n")
                id_temp = nos[j].id
                data_temp = nos[j].data[i]
                hora_temp = nos[j].hora[i]
                tempo_inicio = converter_hora(nos[j].hora[i])
                lat_temp = float(lat)
                lon_temp = float(lon)
                bateria_temp = nos[j].bateria[i]
                saltos += 1
                if id_temp == id2:
                    return True, saltos
                else:
                    j = 0
                    break
    return False, saltos

def repassar_mensagem_egoista_sem_prioridade(bat_media, nos, id1, id2, data1, hora1, lat1, lon1, bateria1, tolerancia_tempo, R, file):
    id_temp = id1
    data_temp = data1
    hora_temp = hora1
    lat_temp = lat1
    lon_temp = lon1
    bateria_temp = bateria1
    saltos = 0
    tempo = converter_hora(hora_temp)
    tempo_final_tolerancia = tempo + tolerancia_tempo
    tempo_inicio = tempo
    for j in range(len(nos)):
        for i in range(nos[j].leituras()):
            lat, lon = nos[j].localizacao[i].split(",")
            if nos[j].data[i] == data_temp and tempo_inicio <= converter_hora(nos[j].hora[i]) and converter_hora(nos[j].hora[i]) <= tempo_final_tolerancia and haversine(lat_temp, lon_temp, float(lat), float(lon)) <= R and id_temp != nos[j].id:
                if int(nos[j].bateria[i]) >= bat_media:
                    file.write(f"Nó {nos[j].id} disponível! data: {nos[j].data[i]} hora: {nos[j].hora[i]} bateria: {nos[j].bateria[i]} dist: {haversine(lat_temp, lon_temp, float(lat), float(lon))} | {id_temp} --> {nos[j].id}\n")
                    id_temp = nos[j].id
                    data_temp = nos[j].data[i]
                    hora_temp = nos[j].hora[i]
                    tempo_inicio = converter_hora(nos[j].hora[i])
                    lat_temp = float(lat)
                    lon_temp = float(lon)
                    bateria_temp = nos[j].bateria[i]
                    saltos += 1
                    if id_temp == id2:
                        return True, saltos
                    else:
                        j = 0
                        break
                else:
                    file.write(f"Nó {nos[j].id} recusou repassar a mensagem! Motivo: Bateria = {nos[j].bateria[i]}\n")
    return False, saltos

def repassar_mensagem_egoista_com_prioridade(bat_media, nos, id1, id2, data1, hora1, lat1, lon1, bateria1, tolerancia_tempo, R, file, prioridade):
    id_temp = id1
    data_temp = data1
    hora_temp = hora1
    lat_temp = lat1
    lon_temp = lon1
    bateria_temp = bateria1
    saltos = 0
    tempo = converter_hora(hora_temp)
    tempo_final_tolerancia = tempo + tolerancia_tempo
    tempo_inicio = tempo
    for j in range(len(nos)):
        for i in range(nos[j].leituras()):
            lat, lon = nos[j].localizacao[i].split(",")
            if nos[j].data[i] == data_temp and tempo_inicio <= converter_hora(nos[j].hora[i]) and converter_hora(nos[j].hora[i]) <= tempo_final_tolerancia and haversine(lat_temp, lon_temp, float(lat), float(lon)) <= R and id_temp != nos[j].id:
                if int(nos[j].bateria[i]) >= bat_media:
                    file.write(f"Nó {nos[j].id} disponível! data: {nos[j].data[i]} hora: {nos[j].hora[i]} bateria: {nos[j].bateria[i]} dist: {haversine(lat_temp, lon_temp, float(lat), float(lon))} Prioridade da mensagem: {prioridade} | {id_temp} --> {nos[j].id}\n")
                    id_temp = nos[j].id
                    data_temp = nos[j].data[i]
                    hora_temp = nos[j].hora[i]
                    tempo_inicio = converter_hora(nos[j].hora[i])
                    lat_temp = float(lat)
                    lon_temp = float(lon)
                    bateria_temp = nos[j].bateria[i]
                    saltos += 1
                    if id_temp == id2:
                        return True, saltos
                    else:
                        j = 0
                        break
                else:
                    if prioridade == "normal":
                        file.write(f"Nó {nos[j].id} recusou repassar a mensagem! Motivo: Bateria = {nos[j].bateria[i]} Prioridade da mensagem: {prioridade}\n")
                    else:
                        file.write(f"Nó {nos[j].id} forçadamente repassou a mensagem! Motivo: Bateria = {nos[j].bateria[i]} Prioridade da mensagem: {prioridade} data: {nos[j].data[i]} hora: {nos[j].hora[i]} dist: {haversine(lat_temp, lon_temp, float(lat), float(lon))} | {id_temp} --> {nos[j].id}\n")
                        id_temp = nos[j].id
                        data_temp = nos[j].data[i]
                        hora_temp = nos[j].hora[i]
                        tempo_inicio = converter_hora(nos[j].hora[i])
                        lat_temp = float(lat)
                        lon_temp = float(lon)
                        bateria_temp = nos[j].bateria[i]
                        saltos += 1
                        if id_temp == id2:
                            return True, saltos
                        else:
                            j = 0
                            break
    return False, saltos


def simular_100_n_egoista(nos, R, D, tolerancia_tempo, file):
    linha1 = np.random.randint(1,112555)
    linha2 = np.random.randint(1,112555)

    id1, data1, hora1, localizacao1, bateria1, mem_interna1 = encontrarLinha(nos, linha1)
    id2, data2, hora2, localizacao2, bateria2, mem_interna2 = encontrarLinha(nos, linha2)
    while id2 == id1:
        linha2 = np.random.randint(1,112555)
        id2, data2, hora2, localizacao2, bateria2, mem_interna2 = encontrarLinha(nos, linha2)
    lat1, lon1 = localizacao1.split(",")
    lat2, lon2 = localizacao2.split(",")
    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)

    file.write(f"Nó 1: {linha1} | {id1, data1, hora1, localizacao1, bateria1, mem_interna1}\n")
    file.write(f"Nó 2: {linha2} | {id2, data2, hora2, localizacao2, bateria2, mem_interna2}\n")
    dist = haversine(lat1, lon1, lat2, lon2)
    file.write(f"Distancia entre os nós: {dist} metros\n")
    if dist <= D:
        file.write(f"Os nós {id1} e {id2} estão dentro do range de {D} metros para tentar realizar a comunicação!\n")
        if dist <= R:
            file.write(f"Os nós estão dentro do raio de {R} metros e a comunicação foi instântanea!\n")
            return True, 0
        else:
            sucesso, saltos = repassar_mensagem_n_egoista(nos, id1, id2, data1, hora1, lat1, lon1, bateria1, tolerancia_tempo, R, file)
            if sucesso:
                file.write(f"Mensagem repassada pela rede com sucesso! Saltos = {saltos}\n")
                return True, saltos
            else:
                file.write("Simulação falhou! Nenhum nó disponível...\n")
                return False, saltos
    else:
        file.write(f"Os nós {id1} e {id2} estão longe demais...\n")
    return False, 0

def simular_egoista_sem_prioridade(bat_media, nos, R, D, tolerancia_tempo, file):
    linha1 = np.random.randint(1,112555)
    linha2 = np.random.randint(1,112555)

    id1, data1, hora1, localizacao1, bateria1, mem_interna1 = encontrarLinha(nos, linha1)
    id2, data2, hora2, localizacao2, bateria2, mem_interna2 = encontrarLinha(nos, linha2)
    while id2 == id1:
        linha2 = np.random.randint(1,112555)
        id2, data2, hora2, localizacao2, bateria2, mem_interna2 = encontrarLinha(nos, linha2)
    lat1, lon1 = localizacao1.split(",")
    lat2, lon2 = localizacao2.split(",")
    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)

    file.write(f"Bateria média: {bat_media}\n")
    file.write(f"Nó 1: {linha1} | {id1, data1, hora1, localizacao1, bateria1, mem_interna1}\n")
    file.write(f"Nó 2: {linha2} | {id2, data2, hora2, localizacao2, bateria2, mem_interna2}\n")
    dist = haversine(lat1, lon1, lat2, lon2)
    file.write(f"Distancia entre os nós: {dist} metros\n")
    if dist <= D:
        file.write(f"Os nós {id1} e {id2} estão dentro do range de {D} metros para tentar realizar a comunicação!\n")
        if dist <= R:
            file.write(f"Os nós estão dentro do raio de {R} metros e a comunicação foi instântanea!\n")
            return True, 0
        else:
            sucesso, saltos = repassar_mensagem_egoista_sem_prioridade(bat_media, nos, id1, id2, data1, hora1, lat1, lon1, bateria1, tolerancia_tempo, R, file)
            if sucesso:
                file.write(f"Mensagem repassada pela rede com sucesso! Saltos = {saltos}\n")
                return True, saltos
            else:
                file.write("Simulação falhou! Nenhum nó disponível...\n")
                return False, saltos
    else:
        file.write(f"Os nós {id1} e {id2} estão longe demais...\n")
    return False, 0

def simular_egoista_com_prioridade(bat_media, nos, R, D, tolerancia_tempo, file):
    linha1 = np.random.randint(1,112555)
    linha2 = np.random.randint(1,112555)
    prioridade = np.random.choice(["urgente","normal"])

    id1, data1, hora1, localizacao1, bateria1, mem_interna1 = encontrarLinha(nos, linha1)
    id2, data2, hora2, localizacao2, bateria2, mem_interna2 = encontrarLinha(nos, linha2)
    while id2 == id1:
        linha2 = np.random.randint(1,112555)
        id2, data2, hora2, localizacao2, bateria2, mem_interna2 = encontrarLinha(nos, linha2)
    lat1, lon1 = localizacao1.split(",")
    lat2, lon2 = localizacao2.split(",")
    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)

    file.write(f"Bateria média: {bat_media}\n")
    file.write(f"Nó 1: {linha1} | {id1, data1, hora1, localizacao1, bateria1, mem_interna1}\n")
    file.write(f"Nó 2: {linha2} | {id2, data2, hora2, localizacao2, bateria2, mem_interna2}\n")
    dist = haversine(lat1, lon1, lat2, lon2)
    file.write(f"Distancia entre os nós: {dist} metros\n")
    if dist <= D:
        file.write(f"Os nós {id1} e {id2} estão dentro do range de {D} metros para tentar realizar a comunicação!\n")
        if dist <= R:
            file.write(f"Os nós estão dentro do raio de {R} metros e a comunicação foi instântanea!\n")
            return True, 0
        else:
            sucesso, saltos = repassar_mensagem_egoista_com_prioridade(bat_media, nos, id1, id2, data1, hora1, lat1, lon1, bateria1, tolerancia_tempo, R, file, prioridade)
            if sucesso:
                file.write(f"Mensagem repassada pela rede com sucesso! Saltos = {saltos}\n")
                return True, saltos
            else:
                file.write("Simulação falhou! Nenhum nó disponível...\n")
                return False, saltos
    else:
        file.write(f"Os nós {id1} e {id2} estão longe demais...\n")
    return False, 0

def simulacoes(num_simulacoes, nos, R, D, tolerancia_tempo, file):
    print("Gerando simulações, por favor aguarde")
    bat_media = int(bateria_media(nos))
    
    entregas1 = 0
    saltos_total1 = 0
    file.write(f"######### Simulação com nós não egoístas #########\n")
    for i in range(num_simulacoes):
        file.write(f"-------------- SIMULAÇÃO {i+1} ------------------\n")
        sucesso, saltos = simular_100_n_egoista(nos, R, D, tolerancia_tempo, file)
        if sucesso:
            entregas1 += 1
        saltos_total1 += saltos
        file.write(f"----------------------------------------------\n")
    file.write("#############################################################\n\n")

    entregas2 = 0
    saltos_total2 = 0
    file.write(f"######### Simulação com nós egoístas e mensagens sem prioridade #########\n")
    for i in range(num_simulacoes):
        file.write(f"-------------- SIMULAÇÃO {i+1} ------------------\n")
        sucesso, saltos = simular_egoista_sem_prioridade(bat_media, nos, R, D, tolerancia_tempo, file)
        if sucesso:
            entregas2 += 1
        saltos_total2 += saltos
        file.write(f"----------------------------------------------\n")
    file.write("#############################################################\n\n")

    entregas3 = 0
    saltos_total3 = 0
    file.write(f"######### Simulação com nós egoístas e mensagens com prioridade #########\n")
    for i in range(num_simulacoes):
        file.write(f"-------------- SIMULAÇÃO {i+1} ------------------\n")
        sucesso, saltos = simular_egoista_com_prioridade(bat_media, nos, R, D, tolerancia_tempo, file)
        if sucesso:
            entregas3 += 1
        saltos_total3 += saltos
        file.write(f"----------------------------------------------\n")
    file.write("#############################################################\n\n")
    
    file.write("---------- RESULTADOS SIMULAÇÃO  NÓS 100% NÃO EGOÍSTAS------------------------------------\n")
    file.write(f"num simulacoes:  {num_simulacoes} | entregas: {entregas1} | taxa entrega: {(entregas1/num_simulacoes)*100}% | saltos: {saltos_total1}\n")

    file.write("\n---------- RESULTADOS SIMULAÇÃO NÓS EGOÍSTAS COM MENSAGENS SEM PRIORIDADE ----------------\n")
    file.write(f"num simulacoes:  {num_simulacoes} | entregas: {entregas2} | taxa entrega: {(entregas2/num_simulacoes)*100}% | saltos: {saltos_total2}\n")

    file.write("\n---------- RESULTADOS SIMULAÇÃO NÓS EGOÍSTAS COM MENSAGENS COM PRIORIDADE ----------------\n")
    file.write(f"num simulacoes:  {num_simulacoes} | entregas: {entregas3} | taxa entrega: {(entregas3/num_simulacoes)*100}% | saltos: {saltos_total3}\n")

    file.write(f"\nNúmero médio de saltos: {(saltos_total1 + saltos_total2 + saltos_total3)/3}")

def main():
    R = 50
    D = 500
    tolerancia_tempo = 300
    num_simulacoes = 100
    logs = "logs.txt"
    dataset_path = "dataset_final_29.06.25.txt"

    nos = read_dataset(dataset_path)
    with open(logs, "w") as file:
        simulacoes(num_simulacoes, nos, R, D, tolerancia_tempo, file)
    file.close()
    print("Simulações encerradas. Consulte os logs para ver os resultados!")

main()