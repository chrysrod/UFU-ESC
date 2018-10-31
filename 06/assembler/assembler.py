# -*- coding: utf-8 -*-

def abreCodigo():
    
    #Carrega a variável arquivo original com o código .asm 
    global arquivo_original
    arquivo_original = open('Pong.asm')
    
    #Carrega as linhas do arquivo dentro da variável código 
    global codigo_original
    codigo_original = arquivo_original.readlines()

    #Fecha o arquivo com o código original
    arquivo_original.close()

    #Cria uma lista global com as linhas do código sem espaços
    global codigo_sem_comentario
    codigo_sem_comentario = []

    #Cria uma lista global com as linhas do código sem labels
    global codigo_sem_labels
    codigo_sem_labels = []

    #Cria uma lista global com as linhas do código sem label jumps
    global codigo_sem_label_jump
    codigo_sem_label_jump = []

    #Cria uma lista global com as linhas do código sem variáveis
    global codigo_sem_variavel
    codigo_sem_variavel = []

    #Cria uma lista global com as linhas do código com as instruções em binário
    global codigo_instrucoes_bin
    codigo_instrucoes_bin = []

def removeComentario():

    #Listas sem espaço entre as palavras
    linha_sem_espaco = []
    codigo_sem_espaco = codigo_original

    #Índices
    index_1 = 0
    index_2 = 0
    
    """for linha in codigo_original:
        if linha.find(' '):
            for elemento in linha.split():
                linha_sem_espaco.append(linha.split()[index_1])
                index_1 += 1
            codigo_sem_espaco.append(linha_sem_espaco[index_2])
            index_2 += 1
            index_1 = 0
            index_2 = 0
        else:
            pass
    """
    
    #Identifica as linhas com comentários e as remove, sem deixar espaços vazios no lugar
    for linha in codigo_sem_espaco:
            if linha.find('//') == 0:
                codigo_sem_comentario.append(linha[0:linha.find('//')])
            elif linha.find('//') != -1:
                codigo_sem_comentario.append(linha[0:linha.find('//')] + '\n')
            else:
                codigo_sem_comentario.append(linha)        
                
def removeLabel():

    #Dicionário para associar linha dos labels com seus respectivos nomes
    labels = {}

    #Índice da linha atual
    index = 0

    #Auxiliar para atualizar o valor das linhas dos labels
    aux = 0
    
    #Associa os valores da linha aos seus repectivos labels e exclui a label
    for linha in codigo_sem_comentario:
        if linha.find('(') != -1:
            labels[linha[1:len(linha)-2]] = index - aux
            aux += 1
        else:
            codigo_sem_labels.append(linha)
        index += 1

    for linha in codigo_sem_labels:
        for palavra in linha.split():
            if palavra[1:len(palavra)] in labels.keys():
                codigo_sem_label_jump.append('@'+str(labels[palavra[1:]])+'\n')
            else:
                codigo_sem_label_jump.append(linha)

def removeVariavel():

    #Dicionário associando cada variável a seu respectivo endereço na memória
    variaveis = {"R0":0,
                 "R1":1,
                 "R2":2,
                 "R3":3,
                 "R4":4,
                 "R5":5,
                 "R6":6,
                 "R7":7,
                 "R8":8,
                 "R9":9,
                 "R10":10,
                 "R11":11,
                 "R12":12,
                 "R13":13,
                 "R14":14,
                 "R15":15,
                 "SP":0,
                 "LCL":1,
                 "ARG":2,
                 "THIS":3,
                 "THAT":4,
                 "SCREEN":16384,
                 "KBD":24576}

    #Índice da memória/dicionário, começa em 16 pois R0 até R15 está reservado
    index = 16

    for linha in codigo_sem_label_jump:
        if linha[0:1] == '@':
            if linha[1:len(linha)-1] not in variaveis.keys() and not str(linha[1:len(linha)-1]).isdigit():
                variaveis[linha[1:len(linha)-1]] = index
                index += 1
    for linha in codigo_sem_label_jump:
        if linha[:1] == '@':
            if linha[1:len(linha)-1] in variaveis.keys():
                codigo_sem_variavel.append('@'+str(variaveis[linha[1:len(linha)-1]])+'\n')
                #codigo_sem_variavel.append(bin(variaveis[linha[1:len(linha)-1]])[2:].zfill(16)+'\n')
            else:
                codigo_sem_variavel.append(linha)
                #codigo_sem_variavel.append(bin(int(linha[1:len(linha)-1]))[2:].zfill(16)+'\n')
        else:
            codigo_sem_variavel.append(linha)

def converteInstrucoesBinario():

    # Dicionário associando as intruções comp a = 0
    instrucoes_comp_0 = {'0':'101010',
                         '1':'111111',
                         '-1':'111010',
                         'D':'001100',
                         'A':'110000',
                         '!D':'001101',
                         '!A':'110001',
                         '-D':'001111',
                         '-A':'110011',
                         'D+1':'011111',
                         'A+1':'110111',
                         'D-1':'001110',
                         'A-1':'110010',
                         'D+A':'000010',
                         'D-A':'010011',
                         'A-D':'000111',
                         'D&A':'000000',
                         'D|A':'010101'}

    #Dicionário associando as intruções comp a = 1
    instrucoes_comp_1 = {'M':'110000',
                         '!M':'110001',
                         '-M':'110011',
                         'M+1':'110111',
                         'M-1':'110010',
                         'D+M':'000010',
                         'D-M':'010011',
                         'M-D':'000111',
                         'D&M':'000000',
                         'D|M':'010101'}

    #Dicionário associando as instruções dest
    instrucoes_dest = {'null':'000',
                       'M':'001',
                       'D':'010',
                       'MD':'011',
                       'A':'100',
                       'AM':'101',
                       'AD':'110',
                       'AMD':'111'}

    #Dicionário associando as instruções jmp
    instrucoes_jmp = {'null':'000',
                      'JGT':'001',
                      'JEQ':'010',
                      'JGE':'011',
                      'JLT':'100',
                      'JNE':'101',
                      'JLE':'110',
                      'JMP':'111'}

    for linha in codigo_sem_variavel:
        if linha.find('=') != -1:
            if linha[linha.find("=")+1:len(linha)-1] in instrucoes_comp_0:
                a = 0
                codigo_instrucoes_bin.append('111' + str(a) +
                                             instrucoes_comp_0[linha[linha.find("=")+1:len(linha)-1]] +
                                             instrucoes_dest[linha[:linha.find("=")]] +
                                             '000' + '\n'
                                             )
            else:
                a = 1
                codigo_instrucoes_bin.append('111' + str(a) +
                                             instrucoes_comp_1[linha[linha.find("=")+1:len(linha)-1]] +
                                             instrucoes_dest[linha[:linha.find("=")]] +
                                             '000' + '\n'
                                             )
        elif linha.find(';') != -1:
            if linha[:linha.find(";")] in instrucoes_comp_0:
                a = 0
                codigo_instrucoes_bin.append('111' + str(a) +
                                             instrucoes_comp_0[linha[:linha.find(";")]] +
                                             '000' +
                                             instrucoes_jmp[linha[linha.find(";")+1:len(linha)-1]] + '\n'
                                             )
            else:
                a = 1
                codigo_instrucoes_bin.append('111' + str(a) +
                                             instrucoes_comp_1[linha[:linha.find(";")]] +
                                             '000' +
                                             instrucoes_jmp[linha[linha.find(";") + 1:len(linha) - 1]] + '\n'
                                             )
        elif linha[0] == '@':
            codigo_instrucoes_bin.append(bin(int(linha[1:]))[2:].zfill(16) + '\n')
        else:
            codigo_instrucoes_bin.append(linha)

abreCodigo()
removeComentario()
removeLabel()
removeVariavel()
converteInstrucoesBinario()
arquivo = open('Pong.hack','w')
arquivo.writelines(codigo_instrucoes_bin)
arquivo.close()
