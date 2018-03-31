import cv2


# tranforma a imagem em escala de cinza em preto e branco
def binariza(img, threshold):
    # faz uma cópia da imagem
    src = img.copy()
    # pega o numero de linhas e colunas
    rows, cols = src.shape
    # faz um loop de 0 até o numero de linhas
    for y in range(rows):
        # faz um loop de 0 até o numero de colunas
        for x in range(cols):
            # se o valor do pixel for maior que o treshold tranforma em branco
            if src[y, x] > threshold:
                src[y, x] = 255
            # se não transforma em preto
            else:
                src[y, x] = 0
    # retorna a imagem binarizada
    return src


# marca cada componente na imagem
def componentes_conexos(src):
    # pega o numero de linhas e colunas
    rows, cols = src.shape
    # faz uma cópia da imagem
    img = src.copy()
    # inicializa a label
    label = 1
    # faz um loop de 0 até o numero de linhas
    for y in range(rows):
        # faz um loop de 0 até o numero de colunas
        for x in range(cols):
            # se esse pixe for branco marca ele
            if img[y, x] == 255:
                # chama a função que vai marcar todos os pixel colados a este
                flood(label, img, x, y)
                # incrementa a label pois todos os pixels do blob ja foram marcados
                label += 1
    # retorna uma copia da imagem com os pixels com uma marcação e a quantidade de marcações
    return img, label


# marca o pixel passado e marca os pixels colados a este
def flood(label, imagem, x, y):
    # pega o numero de linhas e colunas
    rows, cols = imagem.shape
    # pixel recebe a marcação passada pela função que chamou essa
    imagem[y, x] = label
    # se o pixel acima for branco e exitir um pixel acima, chama esta função no pixel acima
    if imagem[y-1, x] == 255 and y > 0:
        flood(label, imagem, x, y-1)
    # se o pixel abaixo for branco e exitir um pixel abaixo, chama esta função no pixel abaixo
    if imagem[y+1, x] == 255 and y < rows:
        flood(label, imagem, x, y+1)
    # se o pixel a esquerda for branco e exitir um pixel a esquerda, chama esta função no pixel a esquerda
    if imagem[y, x+1] == 255 and x < cols:
        flood(label, imagem, x+1, y)
    # se o pixel a direita for branco e exitir um pixel a direita, chama esta função no pixel a direita
    if imagem[y, x-1] == 255 and x > 0:
        flood(label, imagem, x-1, y)


# desenha um retangulo no blob
def draw_rectangle(src, label):
    # pega o numero de linhas e colunas
    rows, cols = src.shape
    # cria um set para n olhar um pixel de um blob ja olhado
    labels_looked = set()
    # contador de arroz
    count = 0
    # faz um loop de 0 até o numero de linhas
    for y in range(rows):
        # faz um loop de 0 até o numero de colunas
        for x in range(cols):
            # se o label não é 0 nem 255 e o label não esta no set
            if label[y, x] != 0 and label[y, x] != 255 and label[y, x] not in labels_looked:
                # adiciona no set o label
                labels_looked.add((label[y, x]))
                # acha o ponto superior esquerdo e inferior direito do blob
                pt1, pt2 = acha_pontos(label, label[y, x], y)
                # se o ponto existir desenha o retangulo e aumenta o numero de arroz
                if pt1 != -1:
                    cv2.rectangle(src, pt1, pt2, (0, 255, 255), 0)
                    count += 1
    # retorna a quantidade de arroz
    return count


# acha o ponto superior esquerdo e inferior direito, recebe uma imagem como parametro, o valor da label do blob e o começo do blob
def acha_pontos(photo, valor, y):
    # pega o numero de linhas e colunas
    rows, cols = photo.shape

    # o menor y é o primeiro encontrado pela imagem
    menor_y = y

    # seta uma valor bem alto para diminuir depois
    menor_x = 10000000
    # seta um valor bem baixo para aumentar depois
    maior_y = 0
    maior_x = 0
    # local dos pontos iniciais
    pt1 = (menor_y, menor_x)
    pt2 = (maior_y, maior_x)
    # conta quantos pixels tem no blob
    count = 0
    # faz um loop do menor y até o numero de linhas
    for y in range(menor_y, rows):
        # faz um loop de 0 até o numero de colunas
        for x in range(cols):
            # se a label do pixel for igual a label do pixel passado para a função
            if photo[y, x] == valor:
                # aumenta o count
                count += 1
                # se o menor_x(valor mais a esquerda do blob) for maior que o x atual
                if menor_x > x:
                    # menor_x vira x atual
                    menor_x = x
                    # pt1 recebe esse novo valor
                    pt1 = (menor_x, menor_y)
                # se o maior_x(vamor mais a direita do blob) for menor que o x atual
                if maior_x < x:
                    # maior_x vira o x atual
                    maior_x = x
                    # pt2 recebe esse novo valor
                    pt2 = (maior_x, maior_y)
                # se o maior_y(vamor mais inferior do blob) for menor que o y atual
                if maior_y <= y:
                    # maior_y vira o y atual
                    maior_y = y
                    # pt2 recebe esse novo valor
                    pt2 = (maior_x, maior_y)
        # se o maior_y for diferente de 0 e o y atual for maior que o maior_y do blob
        if maior_y != 0 and y > maior_y:
            # se a quantidade de pixels forem menores que 50, é um ruido
            if count < 50:
                return -1, -1
            # retorna pt1 e pt2
            else:
                return pt1, pt2


# le a imagem
img = cv2.imread('arroz.bmp', 0)

# chama a função binariza
dst = binariza(img, 209)
# salva a foto binarizada
cv2.imwrite('binarizdo.bmp', dst)

# chama a função para marcar os blobs
labels, number_of_labels = componentes_conexos(dst)

# chama a função que desenha os retangulos
number_of_rectangles = draw_rectangle(img, labels)
# prina o numero de arroz no console
print("Quantidade de arroz =", number_of_rectangles)

# mostra a imagem desenhada
cv2.imshow('img', img)
cv2.waitKey()
cv2.destroyAllWindows()

#salva a imagem desenhada
cv2.imwrite('desenhado.bmp', img)
