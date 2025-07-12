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
        print("efetuando leitura de dados do dataset")
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
    print("dataset lido com sucesso")
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
    
def repassar_mensagem(nos, id1, id2, data1, hora1, lat1, lon1, bateria1, tolerancia_tempo, R):
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
                print(f"Nó {nos[j].id} disponível! data: {nos[j].data[i]} hora: {nos[j].hora[i]} dist: {haversine(lat_temp, lon_temp, float(lat), float(lon))} | {id_temp} --> {nos[j].id}")
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

def simular(nos, R, D, tolerancia_tempo):
    linha1 = np.random.randint(1,112555)
    linha2 = np.random.randint(1,112555)
    print(linha1, linha2)

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

    print(id1, data1, hora1, lat1, lon1, bateria1, mem_interna1)
    print(id2, data2, hora2, lat2, lon2, bateria2, mem_interna2)
    dist = haversine(lat1, lon1, lat2, lon2)
    print(f"Distancia entre os nos {dist}")
    if dist <= D:
        print(f"Os nós {id1} e {id2} estão dentro do range de {D} metros para tentar realizar a comunicação!")
        if dist <= R:
            print(f"Os nós estão dentro do raio de {R} metros e a comunicação foi instântanea!")
        else:
            sucesso, saltos = repassar_mensagem(nos, id1, id2, data1, hora1, lat1, lon1, bateria1, tolerancia_tempo, R)
            if sucesso:
                print(f"Mensagem repassada pela rede com sucesso! Saltos = {saltos}")
            else:
                print("Simulação falhou pois não encontrei nenhum nó disponível...")
    else:
        print(f"Os nós {id1} e {id2} estão longe demais...")

def main():
    R = 50
    D = 200
    tolerancia_tempo = 300
    dataset_path = "dataset_final_29.06.25.txt"
    nos = read_dataset(dataset_path)

    simular(nos, R, D, tolerancia_tempo)

main()