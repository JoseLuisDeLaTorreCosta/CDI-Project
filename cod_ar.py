import math 
from functools import *
from itertools import *
import sys

alfabeto = []
alfdict = dict([])

def do_alfabeto_and_dict():
    a = ['A', 'T', 'G', 'C']
    for first in enumerate(a):
        word = first[1]
        pos = first[0]
        alfabeto.append(word)
        alfdict[word] = pos

def obtener_frecuencias(mensaje):
    return [mensaje.count(x) for x in alfabeto]

def num2rice(num, k):
    m = pow(2, k)
    q = num//m 
    rest = bin(num%m)[2:]
    if len(rest) < k:
        rest = ('0' * (k - len(rest))) + rest 
    
    return ('1' * q) + '0' + rest

def listnum2rice(L, k):
    mensaje = ""
    for num in L:
        mensaje += num2rice(num, k)
    return mensaje

def rice2listnum(cod, k, let):
    m = pow(2, k)
    if cod == "" or let == 0:
        return ([], cod)
    else:
        x = list(takewhile(lambda x: x == '1', cod))
        y = cod[len(x):len(x)+1 + k]
        rest, cod = rice2listnum(cod[len(x)+1 + k:], k, let-1)
        return [len(x)*m + int(y, 2)] + rest, cod
    


def tabla_de_frec(frecuencias, len):
    return [(i, j/len) for i,j in zip(alfabeto, frecuencias)]

def Decimal_to_binary(num, k):
    c = bin(num)[2:]
    if len(c) < k:
        c = ('0' * (k - len(c))) + c
    return c

def IntegerArithmeticEncode(mensaje, frecuencias):
    code = ''
    T = sum(frecuencias)
    k = math.ceil(math.log2(4*T))
    R = pow(2, k)
    tabla = tabla_de_frec(frecuencias, len(mensaje))
    
    I = [0]
    for i in range(len(tabla)):
        I.append(I[i] + tabla[i][1])
    
    inferior_limit = 0
    superior_limit = R
    
    
    bits_acumulados = 0

    len_word = 1 
    for i in range(len(mensaje)//len_word):
        x = len_word*i 

        il = int(inferior_limit + I[alfdict[mensaje[x:x+len_word]]]*(superior_limit - inferior_limit))
        sl = int(inferior_limit + I[alfdict[mensaje[x:x+len_word]]+1]*(superior_limit - inferior_limit))
        inferior_limit = il 
        superior_limit = sl

            
        while (inferior_limit >= 0 and superior_limit <= R/2) or (inferior_limit >= R/2 and superior_limit <= R) or (inferior_limit >= R/4 and superior_limit <= 3*R/4):
            if superior_limit <= R/2:
                code+='0'
                if bits_acumulados != 0:
                    code+= ('1' * bits_acumulados)
                    bits_acumulados = 0
                inferior_limit = 2*inferior_limit
                superior_limit = 2*superior_limit
            elif superior_limit <= 3*R/4:
                bits_acumulados+=1
                inferior_limit = 2*inferior_limit - int(R/2)
                superior_limit = 2*superior_limit - int(R/2)
            else:
                code+='1'
                if bits_acumulados != 0:
                    code+= ('0' * bits_acumulados)
                    bits_acumulados = 0
                inferior_limit = 2*inferior_limit - R
                superior_limit = 2*superior_limit - R 
    
    if inferior_limit <= R/4:
        code += '01' + ('1' * bits_acumulados)
    else:
        code += '10' + ('0' * bits_acumulados)

    code += Decimal_to_binary(inferior_limit, k)
    
    return code



def findPos(I, num, inferior_limit, superior_limit):
    for j in range(len(I)-1):
        il = int(inferior_limit + I[j]*(superior_limit - inferior_limit))
        sl = int(inferior_limit + I[j+1]*(superior_limit - inferior_limit))
        if num >= il and num < sl:
            return il, sl, j

def IntegerArithmeticDecode(codigo, longitud_mensaje, alfabeto, frecuencias):
    mensaje = ""

    T = sum(frecuencias)
    k = int(math.log2(4*T)) + 1
    R = pow(2, k)
    tabla = tabla_de_frec(frecuencias, longitud_mensaje)


    I = [0]
    for i in range(len(tabla)):
        I.append(I[i] + tabla[i][1])
    
    inferior_limit = 0
    superior_limit = R
    num = int(codigo[0:k], 2)

    for i in range(len(codigo) - k):
        while not ((inferior_limit >= 0 and superior_limit <= R/2) or (inferior_limit >= R/2 and superior_limit <= R) or (inferior_limit >= R/4 and superior_limit <= 3*R/4)):
            (inferior_limit, superior_limit, pos) = findPos(I, num, inferior_limit, superior_limit)
            mensaje += alfabeto[pos]
            
            
            
        if inferior_limit >= 0 and superior_limit <= R/2:
            inferior_limit = 2*inferior_limit
            superior_limit = 2*superior_limit
            num = 2*num
        elif inferior_limit >= R/2 and superior_limit <= R:
            inferior_limit = 2*inferior_limit - R
            superior_limit = 2*superior_limit - R
            num = 2*num - R
        elif inferior_limit >= R/4 and superior_limit <= 3*R/4:
            inferior_limit = 2*inferior_limit - int(R/2)
            superior_limit = 2*superior_limit - int(R/2) 
            num = 2*num - int(R/2)

        num+=int(codigo[i+k])
        
    
    return mensaje[:longitud_mensaje]

def entradaEn(file):
    f = open(file, 'r')
    text = f.read()
    return text

def entradaDe(file):
    f = open(file, 'rb')
    text = int.from_bytes(f.read(), byteorder='big')
    f.close()
    text = bin(text)[2:]
    return text

def salidaEn(cod, file, flag1=0):
    if flag1 == "-h":
        x = (list(takewhile(lambda x: x != "/", file[::-1]))[::-1])
        file = "".join(str(element) for element in x)
    file = file + ".ch"
    codified = int(cod, 2).to_bytes((len(cod) + 7) // 8, byteorder='big')
    f = open(file, 'wb')
    f.write(codified)
    f.close()

def salidaDe(men, file, flag1=0):
    if flag1 == "-h":
        x = (list(takewhile(lambda x: x != "/", file[::-1]))[::-1])
        file = "".join(str(element) for element in x)
    file = file[:-3]
    f = open(file, 'w')
    f.write(men)
    f.close()

k = 10

do_alfabeto_and_dict()
if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("INVALID COMMAND LINE")
    print("The next command lines are accepted:")
    print("python3 cod_ar.py [-h] filepath")
    print("-h: The output will be saved at the same path as the compressor")
else: 
    if sys.argv[-1][-2:] == "ch":
        cod = entradaDe(sys.argv[-1])
        frecuencias, cod = rice2listnum(cod, k, 4)
        men = IntegerArithmeticDecode(cod, sum(frecuencias), alfabeto, frecuencias)
        salidaDe(men, sys.argv[-1], sys.argv[1])
    else:
        men = entradaEn(sys.argv[-1])
        frecuencias = obtener_frecuencias(men)
        cod = listnum2rice(frecuencias, k)
        cod = cod + IntegerArithmeticEncode(men, frecuencias)
        salidaEn(cod, sys.argv[-1], sys.argv[1])

