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

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371000
    return c * r

def main():
    dataset_path = "dataset_final_29.06.25.txt"
    nos = read_dataset(dataset_path)
    print(nos[12].localizacao)

    lat1, lon1 = -3.08849338, -59.96486666
    lat2, lon2 = -3.0885493,-59.96457

    dist_meters = haversine(lat1, lon1, lat2, lon2)
    print(f"Distance: {dist_meters:.2f} meters")

    linha1 = np.random.randint(1,112554)
    linha2 = np.random.randint(1,112554)
    print(linha1, linha2)

    for j in range(37):
        print(f"leituras {nos[j].id,nos[j].leituras()}")

    i = 0
    pos = nos[i].leituras()
    while True:
        print(f"posicao {i} {pos}")
        if pos >= linha1:
            print(f"achei! é o no {i}")
            posicao = linha1 - ultima_pos - 1
            print(f"offset {posicao}")
            print(f"no {i} data: {len(nos[i].data)}")
            print(f"info da linha: no {i} data: {nos[i].data[posicao]} hora: {nos[i].hora[posicao]} localizacao: {nos[i].localizacao[posicao]} mem interna: {nos[i].memoria_interna[posicao]}")
            break
        else:
            i += 1
            ultima_pos = pos
            pos += nos[i].leituras()

main()