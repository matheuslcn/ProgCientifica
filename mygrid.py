from __future__ import annotations
from math import inf as INFINITY
from typing import List, Tuple
from compgeom.compgeom import CompGeom, Point

##classe para geração de grid de conectividade
class MyGrid():
    def __init__(self):
        self.grid = []
        self.qtd_x = 0
        self.qtd_y = 0
        self.min_x = INFINITY
        self.min_y = INFINITY
        self.max_x = -INFINITY
        self.max_y = -INFINITY
        self.espacamento = 0

    ##pega o tamanho maximo da da imagem baseado na boudBox de cada face
    ##entrada: Lista de boundBoxes
    def pega_bordas(self, boundBoxes:List[Tuple[float, float, float, float]]):
        for posBB in boundBoxes:
            if posBB[0] < self.min_x:
                self.min_x = posBB[0]
            if posBB[1] > self.max_x:
                self.max_x = posBB[1]
            if posBB[2] < self.min_y:
                self.min_y = posBB[2]
            if posBB[3] > self.max_y:
                self.max_y = posBB[3]
        print(f"min_x: {self.min_x} max_x: {self.max_x} min_y: {self.min_y} max_y: {self.max_y}")

    ##cria o grid como uma matriz em que cada posição é uma tupla contendo o centro do ponto e um booleando dizendo se está dentro ou fora
    ##entrada: raio
    ##obs: chamar após ter chamado o pega_bordas
    ##obs: ToDo-> trocar no linha.append((i,j,True)) o i e j pelas posições dos pontos
    def preencheBB(self, espacamento):
        self.espacamento = espacamento
        qtd_x = int(self.max_x - self.min_x) + 1
        self.qtd_x = int(qtd_x/espacamento)
        qtd_y = int(self.max_y - self.min_y) + 1
        self.qtd_y = int(qtd_y/espacamento)
        for i in range(self.qtd_x):
            linha = []
            for j in range(self.qtd_y):
                point  = {
                    "x": self.min_x + i * espacamento,
                    "y": self.min_y + j * espacamento,
                    "isInside": False,
                    "pos": -1,
                    "isOutline": 0,
                    "condition": 0
                }
                linha.append(point)
            self.grid.append(linha)

    ##troca booleano que diz que está dentro para false (dizendo que está fora)
    ##entrada: posX-> posição da linha no grid
    ##entrada: posY-> posição da coluna no grid
    ##entrada: SouN-> booleando dizendo se está dentro ou fora
    def set_ponto_fora(self, posX, posY, SouN, pos): 
        self.grid[posX][posY]["isInside"] = SouN
        if(SouN):
            self.grid[posX][posY]["pos"] = pos
            return pos+1
        return pos

    ##gera a matriz conect sendo a primeira coluna a quantidade de vizinho do ponto relativo a linha
    ##obs: a numeração é feita relativo a posição [j,i] onde j é coluna e i a linha
    ##obs: conta continua dos pontos é feito de coluna em coluna [0,0] = 1, [1,0] = 2, [2,0] = 3 ...
    ##obs: se algum ponto for falso vai entrar na lista conect com todos valores iguais a 0: ToDo retirar essa possibilidade ps: talvez já tenha sido tirado
    ##return: matriz Nx5 de conexções
    def pega_matriz_connect(self):
        connect = []
        for j in range(self.qtd_y):
            for i in range(self.qtd_x):
                linha = [0]
                if(self.grid[i][j]["isInside"]):
                    if( j > 0 and self.grid[i][j-1]["isInside"]):
                        linha[0] += 1
                        linha.append(self.grid[i][j-1]["pos"])
                    if( i > 0 and self.grid[i-1][j]["isInside"]):
                        linha[0] += 1
                        linha.append(self.grid[i-1][j]["pos"])
                    if( j < (self.qtd_y - 1) and self.grid[i][j+1]["isInside"]):
                        linha[0] += 1
                        linha.append(self.grid[i][j+1]["pos"])
                    if( i < (self.qtd_x - 1) and self.grid[i+1][j]["isInside"]):
                        linha[0] += 1
                        linha.append(self.grid[i+1][j]["pos"])
                    for _ in range(5 - len(linha)):
                        linha.append(0)
                    connect.append(linha)    
        return connect

    
    def pega_matriz_connect_contorno(self):
        connect = []
        for j in range(self.qtd_y):
            for i in range(self.qtd_x):
                linha = []
                if(self.grid[i][j]["isInside"]):
                    if( j > 0 and self.grid[i][j-1]["isInside"]):
                        linha.append(self.grid[i][j-1]["pos"])
                    else:
                        linha.append(0)
                    if( i > 0 and self.grid[i-1][j]["isInside"]):
                        linha.append(self.grid[i-1][j]["pos"])
                    else:
                        linha.append(0)
                    if( j < (self.qtd_y - 1) and self.grid[i][j+1]["isInside"]):
                        linha.append(self.grid[i][j+1]["pos"])
                    else:
                        linha.append(0)
                    if( i < (self.qtd_x - 1) and self.grid[i+1][j]["isInside"]):
                        linha.append(self.grid[i+1][j]["pos"])  
                    else:
                        linha.append(0)
        return connect
    ##gera uma matriz N x 2 para indicar quais pontos não se movem
    ##obs: função restringindo a penas a 1ª coluna
    ##obs: ToDo-> necessario mudar a função para poder restringir de outras formas
    ##return: matriz Nx2 de restrições
    def gera_restricoes(self):
        restricoes = []
        for j in range(self.qtd_y):
            for i in range(self.qtd_x):
                if(self.grid[i][j]["isInside"]):
                    if(j == 0):
                        ponto = [1, 1]
                        restricoes.append(ponto)
                    else:
                        ponto = [0, 0]
                        restricoes.append(ponto)
        return restricoes

    ##gera uma matriz N x 2 com as posições de cada ponto de conexao dentro da imagem
    ##return: matriz Nx2 de posição dos pontos
    def gera_pontos(self):
        pontos = []
        for j in range(self.qtd_y):
            for i in range(self.qtd_x):
                if(self.grid[i][j]["isInside"]):
                    ponto = []
                    ponto.append(self.grid[i][j]["x"])
                    ponto.append(self.grid[i][j]["y"])
                    pontos.append(ponto)
        return pontos

    ##gera uma matriz N x 2 para indicar a força gerada em certos pontos
    ##obs: função aplica força apenas na ultima coluno
    ##obs: ToDo-> necessario mudar a função para poder aplicar força em diferentes pontos
    ##return: matriz Nx2 de restrições
    def gera_forca(self):
        forcas = []
        for j in range(self.qtd_y):
            for i in range(self.qtd_x):
                if(self.grid[i][j]["isInside"]):
                    if(j == self.qtd_y-1):
                        ponto = [-1000.0, 0.0]
                        forcas.append(ponto)
                    else:
                        ponto = [0.0, 0.0]
                        forcas.append(ponto)
        return forcas


    def atualiza_grid(self, patches):
        count = 1
        for linha in self.grid:
            for p in linha:
                point = Point(p["x"], p["y"])       
                for patch in patches:
                    if (patch.isPointInside(point)):
                        p["isInside"] = True
                        p["pos"] = count
                        count += 1

    def atualiza_outline(self, pt1, pt2, direction, condition):
        if direction == 0: # direira
            return self.atualiza_esquerda(pt1, pt2, condition)
        elif direction == 1: # esquerda
            return self.atualiza_direita(pt1, pt2, condition)
        elif direction == 2: # cima
            return self.atualiza_cima(pt1, pt2, condition)
        elif direction == 3: # baixo
            return self.atualiza_baixo(pt1, pt2, condition)

    def isInsideBox(self, pt, pt1, pt2):
        min_x = min(pt1.x(), pt2.x())
        max_x = max(pt1.x(), pt2.x())
        min_y = min(pt1.y(), pt2.y())
        max_y = max(pt1.y(), pt2.y())
        return (min_x <= pt['x'] and pt['x'] <= max_x and
            min_y <= pt['y'] and pt['y'] <= max_y)

    def atualiza_cima(self, pt1, pt2, condition):
        print("atualizando cima")
        pts = []
        pos = []
        print(self.qtd_x)
        for i, linha in enumerate(self.grid):
            for j, casa in enumerate(linha):
                if(not self.isInsideBox(casa, pt1, pt2)):
                    continue
                if(casa["isInside"]):
                    if(j < (len(linha)-1)):
                        if(not self.grid[i][j+1]["isInside"]):
                            casa["isOutline"] = 1
                            casa["condition"] = condition
                            pts.append(casa)
                            pos.append((i,j))
                    else:
                        casa["isOutline"] = 1
                        casa["condition"] = condition
                        pts.append(casa)
                        pos.append((i,j))
        for p in pos:
            print(f"x:{p[0]} y:{p[1]}")
        return pts

    def atualiza_baixo(self, pt1, pt2, condition):
        print("atualizando baixo")
        pts = []
        pos = []
        # print(self.qtd_x)
        for i, linha in enumerate(self.grid):
            for j, casa in enumerate(linha):
                if(not self.isInsideBox(casa, pt1, pt2)):
                    continue
                if(casa["isInside"]):
                    if(j > 0):
                        if(not self.grid[i][j-1]["isInside"]):
                            casa["isOutline"] = 1
                            casa["condition"] = condition
                            pts.append(casa)
                            pos.append((i,j))
                            print(f"{i}, {j}: {self.max_x-casa['x']}")
                    else:
                        casa["isOutline"] = 1
                        casa["condition"] = condition
                        pts.append(casa)
                        pos.append((i,j))
        for p in pos:
            print(f"x:{p[0]} y:{p[1]}")
        return pts
    
    def atualiza_esquerda(self, pt1, pt2, condition):
        print("atualizando esquerda")
        pts = []
        pos = []
        print(self.qtd_x)
        for i, linha in enumerate(self.grid):
            for j, casa in enumerate(linha):
                if(not self.isInsideBox(casa, pt1, pt2)):
                    continue
                if(casa["isInside"]):
                    if(i < (len(self.grid)-1)):
                        if(not self.grid[i+1][j]["isInside"]):
                            casa["isOutline"] = 1
                            casa["condition"] = condition
                            pts.append(casa)
                            pos.append((i,j))
                    else:
                        casa["isOutline"] = 1
                        casa["condition"] = condition
                        pts.append(casa)
                        pos.append((i,j))
        for p in pos:
            print(f"x:{p[0]} y:{p[1]}")
        return pts

    def atualiza_direita(self, pt1, pt2, condition):
        print("atualizando direita")
        pts = []
        pos = []
        print(self.qtd_x)
        for i, linha in enumerate(self.grid):
            for j, casa in enumerate(linha):
                if(not self.isInsideBox(casa, pt1, pt2)):
                    continue
                if(casa["isInside"]):
                    if(i > 0):
                        if(not self.grid[i-1][j]["isInside"]):
                            casa["isOutline"] = 1
                            casa["condition"] = condition
                            pts.append(casa)
                            pos.append((i,j))
                    else:
                        casa["isOutline"] = 1
                        casa["condition"] = condition
                        pts.append(casa)
                        pos.append((i,j))
        for p in pos:
            print(f"x:{p[0]} y:{p[1]}")
        return pts
        

