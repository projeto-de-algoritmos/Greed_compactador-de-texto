from tkinter import *
import ctypes


class Node(object):
    def __init__(self):
        self.raiz = False
        self.pai = None
        self.letra = None
        self.bit = None
        self.peso = None
        self.esquerda = None
        self.direita = None


def compactar():
    global canvas
    canvas.delete("all")

    texto = entrada.get()
    probabilidades = {}
    acesso = {}
    tabelaDeCodigos = {}
    pilha = []
    codigoFinal = []

    for i in texto:
        if i in probabilidades:
            probabilidades[i] += 1
        else:
            probabilidades[i] = 1

    probabilidades = {k: v for k, v in sorted(
        probabilidades.items(), key=lambda item: item[1])}

    for i in probabilidades.items():
        no = Node()
        no.peso = i[1]
        noEsquerda = Node()

        noEsquerda.letra = i[0]

        noEsquerda.pai = no

        no.esquerda = noEsquerda
        no.direita = -1
        pilha.append(no)

    while len(pilha) > 1:
        x = pilha.pop(0)
        y = pilha.pop(0)

        arvore = Node()
        arvore.peso = x.peso+y.peso

        if x.direita == -1:
            tempNo = Node()
            tempNo.letra = x.esquerda.letra
            tempNo.bit = 0
            tempNo.primeira = False
            tempNo.pai = arvore
            acesso[tempNo.letra] = id(tempNo)
            arvore.esquerda = tempNo
        else:
            x.bit = 0
            x.pai = arvore
            arvore.esquerda = x

        if y.direita == -1:
            tempNo = Node()
            tempNo.letra = y.esquerda.letra
            tempNo.bit = 1
            tempNo.primeira = False
            tempNo.pai = arvore
            acesso[tempNo.letra] = id(tempNo)
            arvore.direita = tempNo

        else:
            y.bit = 1
            y.pai = arvore
            arvore.direita = y

        j = 0
        for i in pilha:
            if i.peso <= arvore.peso:
                j += 1
            else:
                pilha.insert(j, arvore)
                s = 1
                break
        if j == len(pilha):
            pilha.append(arvore)

    pilha[0].raiz = True

    for i in acesso.items():
        codigo = []
        letra = i[0]
        ponteiro = i[1]
        no = ctypes.cast(ponteiro, ctypes.py_object).value

        while no.raiz == False:
            codigo.append(no.bit)
            no = no.pai
        codigo.reverse()

        if letra not in tabelaDeCodigos:
            tabelaDeCodigos[letra] = ''.join(str(x) for x in codigo)

    for i in texto:
        codigoFinal.append(tabelaDeCodigos[i])

    textoDecodificado = []
    print(''.join(codigoFinal))
    temp = arvore
    for i in ''.join(codigoFinal):

        if i == '0':
            temp = temp.esquerda
        elif i == '1':
            temp = temp.direita

        if temp.letra:
            textoDecodificado.append(temp.letra)
            temp = arvore

    imprimirInformacoes('   '.join(codigoFinal), texto,
                        ''.join(textoDecodificado))


def imprimirInformacoes(codigoFinal, texto, textoDecodificado):
    bits = 0
    bitsASCI = len(texto)*8
    for i in codigoFinal:
        if i == '0' or i == '1':
            bits += 1

    canvas.create_text(
        500, 300, text='Sua string compactada ocupa o espaco de '+str(bits) + ' bits')

    canvas.create_text(
        500, 320, text='Sua string em ASCII ocupa o espaco de '+str(bitsASCI)+' bits')

    canvas.create_text(500, 500, text='Código gerado:')
    canvas.create_text(
        500, 520, text=codigoFinal)

    canvas.create_text(500, 700, text='Sua string decodificada:')
    canvas.create_text(
        500, 720, text=textoDecodificado)


root = Tk()
root.title('Projeto Greedy')


canvas = Canvas(width=1000, height=800, bg='white')
canvas.focus_set()

canvas.pack(expand=YES, fill=BOTH)

Label(root, text='Entre sua string a ser compactada:').place(x=400, y=50)
entrada = Entry(root)
entrada.place(x=400, y=80)
Button(root, text="COMPACTAR", command=compactar,
       height=1, width=13).place(x=400, y=120)
root.mainloop()
