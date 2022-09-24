from PIL import Image

def in_tuple(val:int, t:tuple):
    if val >= t[0] and val <= t[1]:
        return True
    return False

def limiar_f(imagem, pixels, limiar:tuple):
    xsize, ysize = imagem.size

    for i in range(xsize):
        for j in range(ysize):
            if pixels[i,j] >= limiar[0] and pixels[i,j] <= limiar[1]:
                pixels[i,j] = 0
            else:
                pixels[i,j] = 255
    
    return pixels

def BFS(imagem, pixels, start):
    xsize, ysize = imagem.size
    moves = [(0,1),(0,2),(1,0),(2,0),(0,-1),(0,-2),(-1,0),(-2,0), (1,1), (1,-1),(-1,-1),(-1,1)]          # movimento de um BFS em Norte/Sul/Leste/Oeste em 2 níveis
    pretos = []                                                                                         # lista contendo todos os pixels pretps
    visitar = [start]
    visitados = []

    ignorePixel = lambda x,y: x <= 0 or y <= 0 or x >= xsize or y >= ysize or (x,y) in visitados or (x,y) in pretos

    while len(visitar) > 0:
        prox = visitar.pop(0)
        visitados.append(prox)
        
        vizinhos = []
        for move in moves:
            x,y = move[0]+prox[0], move[1]+prox[1]
            if ignorePixel(x,y):
                continue
            vizinhos.append((x,y))
        for vizinho in vizinhos:
            vx, vy = vizinho
            if pixels[vx,vy] == 0:
                pretos.append(vizinho)
                visitar.append(vizinho)
    return pretos

def ignore_sublist(outerList, item):
    for sublist in outerList:
        if item in sublist:
            return True
    return False

def localizar(imagem, pixels):
    xsize, ysize = imagem.size

    dinheiros = []

    print("achando dinheiros hehe")
    for i in range(xsize):
        for j in range(ysize):
            if pixels[i,j] == 0 and not ignore_sublist(dinheiros, (i,j)):
                print("\tBFS")
                objeto = BFS(imagem, pixels, (i,j))
                dinheiros.append(objeto)
                print(f"\t{len(objeto)}")
    dinheiros = [din for din in dinheiros if len(din) >= 500]
    return dinheiros


def main():
    
    moedas = Image.open("imagem.jpeg").convert("L")
    pixels = moedas.load() 

    limiar = (0,150)
    limiar_f(moedas, pixels, limiar)
    moedas.show()
    todasM = localizar(moedas, pixels)

    contagemP = [len(moeda) for moeda in todasM]
    contagemP.sort() 
    maiorMoeda = max(contagemP)
    

    moeda1r = []
    moeda10c = []
    for tamanho in contagemP:
        if in_tuple(tamanho, (maiorMoeda-((1/10)*tamanho), maiorMoeda+((1/10)*tamanho))):
            moeda1r.append(tamanho)
        else:
            moeda10c.append(tamanho)
    
    valor = len(moeda1r) + (0.1*len(moeda10c))

    print("Dinheiros: R${:.2f}".format(valor))


if __name__ == "__main__":
    main()