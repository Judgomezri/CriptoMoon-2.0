from sympy import randprime
import random

# RSA
def generatePrime(a=0):
    if a!=0:
        return randprime(2**(a-2),2**(a-1))
    return randprime(2**(256),2**(512))

def gcd(p,q):
    while q != 0:
        p, q = q, p%q
    return p

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
    index = 0; # Initialize index of result
    while (inputNum > 0):
        res+= reVal(inputNum % base)
        inputNum = int(inputNum / base)
    res = res[::-1]
    return res
#RSA

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
    file_out = open("pub_key_RSA.txt", "w")
    file_out.write(str(pub_key))
    file_out.close()
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
            cipher_text = [(block[0][0]**pub_key)%r,block[0][1]]
            encrypt_text.append(cipher_text)
        else:         
            block[0][0]=(ord(message[i])-64)*(26**2)+(ord(message[i+1])-65)*26+(ord(message[i+2])-65)
            block[0][1]=False
            print(pub_key)
            cipher_text = [(block[0][0]**pub_key)%r,block[0][1]]
            encrypt_text.append(cipher_text)
    return(encrypt_text)

def decifrarRSA(message,priv_key):
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