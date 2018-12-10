# -*- coding: utf-8 -*-

def abreCodigo():
    
    #Carrega a variável arquivo original com o código .asm 
    global arquivo_original
    arquivo_original = open('SimpleAdd.vm')
    
    #Carrega as linhas do arquivo dentro da variável código 
    global codigo_original
    codigo_original = arquivo_original.readlines()
    arquivo_original.close()

    #Cria uma lista global com as linhas do código sem espaços
    global codigo_sem_comentario
    codigo_sem_comentario = []

    """
    #Cria uma lista global com as linhas do código sem labels
    global codigo_sem_labels
    codigo_sem_labels = []

    #Cria uma lista global com as linhas do código sem label jumps
    global codigo_sem_label_jump
    codigo_sem_label_jump = []

    #Cria uma lista global com as linhas do código sem variáveis
    global codigo_sem_variavel
    codigo_sem_variavel = []
    """
    
    #Cria uma lista global com as linhas do código com as instruções em binário
    global codigo_asm
    codigo_asm = []

def removeComentario():

    #Identifica as linhas com comentários e as remove, sem deixar espaços vazios no lugar
    for linha in codigo_original:
        if linha.find('//') == 0:
            codigo_sem_comentario.append(linha[0:linha.find('//')])
        elif linha.find('//') != -1:
            codigo_sem_comentario.append(linha[linha.find('//'):] + '\n')
        elif linha.find('\n') == 0:
            pass
        else:
            codigo_sem_comentario.append(linha)
                
"""def removeLabel():

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
"""

def converteInstrucoesAsm():

    K = 0

    # Dicionário associando as intruções comp a = 0

    for linha in codigo_sem_comentario:
        instrucoes_aritmetico = {'add':['@SP','A=M-1','D=M','M=0','@SP','M=M-1','A=M-1','M=D+M'],
                             'sub':['@SP','A=M-1','D=M','M=0','@SP','M=M-1','A=M-1','M=D-M'],
                             'and':['@SP','A=M-1','D=M','M=0','@SP','M=M-1','A=M-1','M=D&M'],
                             'or':['@SP','A=M-1','D=M','M=0','@SP','M=M-1','A=M-1','M=D|M'],
                             'not':['@SP','A=M-1','M=!M'],
                             'neg':['@SP','A=M-1','M=-M'],
                             'eq':['@SP','A=M-1','D=M','A=A-1','D=D-M','@ISEQ.'+str(K),'D;JEQ',
                                    '@NOTEQ.'+str(K),'D;JNE','(ISEQ.'+str(K)+')','D=-1','@EQ.'+str(K),'0;JMP','(NOTEQ.'+str(K)+')',
                                    'D=0','@EQ.'+str(K),'0;JMP','(EQ.'+str(K)+')','@SP','A=M-1','M=0','A=A-1','M=D','@SP','M=M-1'],
                             'lt':['@SP','A=M-1','D=M','A=A-1','D=M-D','@ISLT.'+str(K),'D;JLT','@NOTLT.'+str(K),'0;JMP',
                                   '(ISLT.'+str(K)+')','D=-1','@LT.'+str(K),'0;JMP','(NOTLT.'+str(K)+')','D=0','@LT.'+str(K),'0;JMP','(LT.'+str(K)+')',
                                   '@SP','A=M-1','M=0','A=A-1','M=D','@SP','M=M-1'],
                             'gt':['@SP','A=M-1','D=M','A=A-1','D=M-D','@ISGT.'+str(K),'D;JGT','@NOTGT.'+str(K),'0;JMP',
                                   '(ISGT.'+str(K)+')','D=-1','@GT.'+str(K),'0;JMP','(NOTGT.'+str(K)+')','D=0','@GT.'+str(K),'0;JMP','(GT.'+str(K)+')',
                                   '@SP','A=M-1','M=0','A=A-1','M=D','@SP','M=M-1']}
        if linha.find('add') != -1:
            for key in instrucoes_aritmetico['add']:
                codigo_asm.append(key + '\n')
        elif linha.find('sub') != -1:
            for key in instrucoes_aritmetico['sub']:
                codigo_asm.append(key + '\n')
        elif linha.find('and') != -1:
            for key in instrucoes_aritmetico['and']:
                codigo_asm.append(key + '\n')
        elif linha.find('or') != -1:
            for key in instrucoes_aritmetico['or']:
                codigo_asm.append(key + '\n')
        elif linha.find('not') != -1:
            for key in instrucoes_aritmetico['not']:
                codigo_asm.append(key + '\n')
        elif linha.find('neg') != -1:
            for key in instrucoes_aritmetico['neg']:
                codigo_asm.append(key + '\n')
        elif linha.find('eq') != -1:
            K += 1
            for key in instrucoes_aritmetico['eq']:
                codigo_asm.append(key + '\n')
        elif linha.find('lt') != -1:
            K += 1
            for key in instrucoes_aritmetico['lt']:
                codigo_asm.append(key + '\n')
        elif linha.find('gt') != -1:
            K += 1
            for key in instrucoes_aritmetico['gt']:
                codigo_asm.append(key + '\n')
        else:
            codigo_asm.append(linha)

abreCodigo()
removeComentario()
#removeLabel()
#removeVariavel()
converteInstrucoesAsm()
arquivo = open('SimpleAdd.asm','w')
arquivo.writelines(codigo_asm)
arquivo.close()
