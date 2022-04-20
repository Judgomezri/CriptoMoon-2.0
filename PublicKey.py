from sympy import N, randprime
import random
#General functions
def generatePrime(a=0):
    if a!=0:
        return randprime(2**(a-2),2**(a-1))
    return randprime(2**(64),2**(128))

def gcd(p,q):
    while q != 0:
        p, q = q, p%q
    return p

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def val(c):
    if c >= '0' and c <= '9':
        return ord(c) - ord('0')
    else:
        return ord(c) - ord('A') + 10
 
# Function to convert a number
# from given base 'b' to decimal
def toDeci(str,base): #CONVIERTE BASE N A DECIMAL
    llen = len(str)
    power = 1 #Initialize power of base
    num = 0     #Initialize result
 
    # Decimal equivalent is str[len-1]*1 +
    # str[len-2]*base + str[len-3]*(base^2) + ...
    for i in range(llen - 1, -1, -1):
         
        # A digit in input number must
        # be less than number's base
        if val(str[i]) >= base:
            print('Invalid Number')
            return -1
        num += val(str[i]) * power
        power = power * base
    return num
    
def reVal(num):
    if (num >= 0 and num <= 9):
        return chr(num + ord('0'))
    else:
        return chr(num - 10 + ord('A'))

def strev(str):
    len = len(str)
    for i in range(int(len / 2)):
        temp = str[i]
        str[i] = str[len - i - 1]
        str[len - i - 1] = temp

def fromDeci(res, base, inputNum): #CONVIERTE DECIMAL A BASE N
    # Initialize index of result
    while (inputNum > 0):
        res+= reVal(inputNum % base)
        inputNum = int(inputNum / base)
    res = res[::-1]
    return res

def multiplicative_inverse(e, phi):
    d, x1, x2, y1 = 0, 0, 1, 1
    temp_phi = phi
    while e > 0:
        temp1 = temp_phi//e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        x = x2 - temp1 * x1
        y = d - temp1 * y1
        x2 = x1
        x1 = x
        d = y1
        y1 = y
    if temp_phi == 1:
        return d + phi

#RSA-----------------------------------------------------------------------
def generateRsaData(p,q):
    n=p*q
    phi = (p-1)*(q-1)
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    #for i in range(2,phi):
    #    if(gcd(i,phi)==1 and gcd(i,n)==1):
    pub_key=e
            #break
    file_out = open("pub_key_RSA.txt", "w")
    file_out.write(str(pub_key))
    file_out.close()
    # Private key generation
    d = 0
    d =multiplicative_inverse(pub_key,phi)
    #while d < 1:
    #    if (pub_key * d) % phi == 1:
    #        break
    #    d = d+1
    priv_key = d
    file_out = open("priv_key_RSA.txt", "w")
    file_out.write(str(priv_key))
    file_out.close()
    return (n, phi, pub_key)

def cifrarRSA(message, r, pub_key):
    message=message.upper()
    message=message.replace(" ", "")
    encrypt_text = []
    block=[[1,False]]
    while(len(message)%3!=0): #De ser necesario completamos el texto con "X" para que el tamaño sea múltiplo de 3 
        message=message+"X"
    for i in range(0,len(message),3):#CIFRAMOS EN BLOQUES DE 3 
        if ord(message[i])-64==26: #verifica y cambia el valor de z para que al hacer la conversion de valores den letras del alfabeto ingles
            block[0][0]=(ord(message[i])-65)*(26**2)+(ord(message[i+1])-65)*26+(ord(message[i+2])-65)
            block[0][1]=True
            cipher_text = [pow(block[0][0],pub_key,r),block[0][1]]
            encrypt_text.append(cipher_text)
        else:         
            block[0][0]=(ord(message[i])-64)*(26**2)+(ord(message[i+1])-65)*26+(ord(message[i+2])-65)
            block[0][1]=False
            print(block[0][0])
            cipher_text = [pow(block[0][0],pub_key,r),block[0][1]]
            encrypt_text.append(cipher_text)
    return(encrypt_text)

def descifrarRSA(message, r):
    file_in = open("private_key_RSA.txt", "r")
    priv_key = int(file_in.read())
    file_in.close()
    decrypt_text = ""
    convert10=0
    for k in range(0,len(message)):
        c = message[k][0]
        decrypt_letter = (c**priv_key)%r
        convert26 = fromDeci("", 26, decrypt_letter)

        for i in range(0,len(convert26)):
             if message[k][1]==True : #Basicamente verifica si el bloque empieza por z.
              convert10= toDeci(convert26[i],26)
              convertascci=chr(convert10+65)
              decrypt_text = decrypt_text + convertascci
             else:
               if(i==0):
                convert10= toDeci(convert26[i],26)
                convertascci=chr(convert10+64)
                decrypt_text = decrypt_text + convertascci
               else:
                convert10= toDeci(convert26[i],26)
                convertascci=chr(convert10+65)
                decrypt_text = decrypt_text + convertascci
    return(decrypt_text)

#Rabin -----------------------------------------------------------------
def generateRabinData(p,q):
    n=p*q
    file_out = open("pub_key_Rabin.txt", "w")
    file_out.write(str(n))
    file_out.close()
    file_out = open("priv_key_Rabin.txt", "w")
    file_out.write(str(p))
    file_out.write("\n")
    file_out.write(str(q))
    file_out.close()
    return n

def cifrarRabin(message, n):
    message=message.upper()
    message=message.replace(" ", "")
    encrypt_text = []
    while(len(message)%3!=0):
      message=message+"X"
    for i in range(0,len(message),3):#CIFRAMOS EN BLOQUES DE 3 
          c=(ord(message[i])-64)*(27**2)+(ord(message[i+1])-64)*27+(ord(message[i+2])-64)
          cipher_text = pow(c,2,n)
          encrypt_text.append(cipher_text)
    return(encrypt_text)

def descifrarRabin(message):
    file_in = open("priv_key_Rabin.txt", "r")
    p = int(file_in.readline().rstrip())
    q = int(file_in.readline().rstrip())
    file_in.close()
    decrypt_list=[] #guarda los decifrados en números
    decrypt_text = ""   #se guarda el decifrado letra por letra
    decrypt_textlist=[] # guarda el decifrado de los 4 residuos
    decrypt_end=[] #guarda todos los decifrados por cada resiudos segun el número de bloques
   # convert10=0
    for k in range(0,len(message)):
        c = message[k]
        # Use Extended Euclid's Algorithm to find x and y such that px+qy=1
        (g, x, y)=egcd(p,q)
        n=p*q
        # Calculate square roots in Zp and Zq
        r=(pow(c,((p+1)//4),p))
        s=(pow(c,((q+1)//4),q))
        ###3
        #decrypt_letter = (c**priv_key)%r
         # Use the Chinese Remainder Theorem to find 4 square roots in Zn
        r1=((x*p*s)+(y*q*r))%n
        r2=((x*p*s)-(y*q*r))%n
        r3=(-r1)%n
        r4=(-r2)%n

        decrypt_list.append([r1,r2,r3,r4]) ###Lista con los números decifrados sin convertir en letras
        #convertimos cada reisudo a base 26 
        convert27_1 = fromDeci("", 27, r1)
        convert27_2 = fromDeci("", 27, r2)
        convert27_3 = fromDeci("", 27, r3)
        convert27_4 = fromDeci("", 27, r4)
        residuos27=[convert27_1,convert27_2,convert27_3,convert27_4] #construimos una lista de esos residuos base26 que será modificada por cada 3 letras
        #recorremos cada residuo 
        for j in range(0,4):
          #recorremos cada letra de cada uno de los residuos
          for i in range(0,len(residuos27[j])):
               #convertimos cada letra base 27 a ascci
               convert10= toDeci((residuos27[j][i]),27)
               convertascci=chr(convert10+64)
               decrypt_text=decrypt_text+convertascci
          decrypt_textlist.append(decrypt_text) #agregamos todos los descifrados por bloque a una lista
          decrypt_text="" #vaciamos para que no se concatenen los próximos
        decrypt_end.append(decrypt_textlist) #agregamos cada lista de 4 decifrados para que nos quede una lista según el #de bloques del texto
        decrypt_textlist=[] #vaciamos la lista para que no se concatene
    return(decrypt_end)


#ElGamal-----------------------------------------------------------
def gen_key(p):
    key= random.randint(pow(10,20),p)
    while gcd(p,key)!=1:
        key=random.randint(0,p)
    return key
def exp_modular(a,b,c):
    x=1
    y=a
    while b>0:
        if b%2==0:
            x=(x*y)%c
        y=(y*y)%c
        b=int(b/2)
    return x%c

def generateElgamalData(p, alpha=0):
    if alpha==0:
        alpha=random.randint(2,p) #generador
    a=gen_key(p) # clave privada
    beta=exp_modular(alpha,a,p) #alpha^a
    file_out = open("pub_key_elgamal.txt", "w")
    file_out.write(str(p))
    file_out.write("\n")
    file_out.write(str(alpha))
    file_out.write("\n")
    file_out.write(str(beta))
    file_out.close()
    file_out = open("priv_key_elgamal.txt", "w")
    file_out.write(str(a))
    file_out.close()
    return alpha, beta
    
#For asymetric encryption
def cifrargamal(message,p,beta,alpha):
    message=message.upper()
    message=message.replace(" ", "")
    k=gen_key(p)
    alpha_k=exp_modular(alpha,k,p)
    alpha_a_k=exp_modular(beta,k,p)
    encrypt_text = []
    while(len(message)%3!=0):
      message=message+"X"
    for i in range(0,len(message),3):#CIFRAMOS EN BLOQUES DE 3 
          c=(ord(message[i])-64)*(27**2)+(ord(message[i+1])-64)*27+(ord(message[i+2])-64)
          cipher_text = c*alpha_a_k
          encrypt_text.append(cipher_text)
    return(encrypt_text,alpha_k)

#For decryption
def decifrargamal(message,alpha_k,a,p):
    decrypt_text = ""
    convert10=0
    for k in range(0,len(message)):
        c = message[k]
        h=exp_modular(alpha_k,a,p)
        decrypt_letter = int(c/h)
        convert27 = fromDeci("", 27, decrypt_letter)
        for i in range(0,len(convert27)):
              convert10= toDeci(convert27[i],27)
              convertascci=chr(convert10+64)
              decrypt_text = decrypt_text + convertascci
    return(decrypt_text)