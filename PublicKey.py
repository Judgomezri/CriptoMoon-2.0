from sympy import N, randprime
import random
import math

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
    ca=[]
    aux=len(message) #LEN ORIGINAL MENSAJE
    while(len(message)%3!=0):
      message=message+"X"
    for i in range(0,len(message),3):#CIFRAMOS EN BLOQUES DE 3           
          c=(ord(message[i])-64)*(27**2)+(ord(message[i+1])-64)*27+(ord(message[i+2])-64)
          ca.append(c)
          cipher_text = pow(c,pub_key,r)#(m**pub_key)%n
          encrypt_text.append(cipher_text)
    #print(ca)
    return(encrypt_text)

def descifrarRSA(message, r):
    file_in = open("priv_key_RSA.txt", "r")
    priv_key = int(file_in.read())
    file_in.close()
    decrypt_text = ""
    convert10=0
    decryptleter=[]
    for k in range(0,len(message)):
        c = message[k]
        decrypt_letter = pow(c,priv_key,r)
        decryptleter.append(decrypt_letter)
        convert27 = fromDeci("", 27, decrypt_letter)

        for i in range(0,len(convert27)):
                convert10= toDeci(convert27[i],27)
                convertascci=chr(convert10+64)
                decrypt_text = decrypt_text + convertascci
    #print(decryptleter,"d")
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
def cifrarElgamal(message,p,beta,alpha):
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
    file_out = open("ak.txt", "w")
    file_out.write(str(alpha_k))
    file_out.close()
    return(encrypt_text)

#For decryption
def descifrarElgamal(message):
    file_in = open("ak.txt", "r")
    alpha_k = int(file_in.read())
    file_in.close()
    file_in = open("pub_key_elgamal.txt", "r")
    p = int(file_in.readline().rstrip())
    file_in.close()
    file_in = open("priv_key_elgamal.txt", "r")
    a = int(file_in.read())
    file_in.close()
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

#Menezes Vanestone--------------------------------------------------------

def legendre(a, p):
    return pow(a, (p - 1) // 2, p)

def tonelli(n, p):
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:
        return pow(n, (p + 1) // 4, p)
    for z in range(2, p):
        if p - 1 == legendre(z, p):
            break
    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    t2 = 0
    while (t - 1) % p != 0:
        t2 = (t * t) % p
        for i in range(1, m):
            if (t2 - 1) % p == 0:
                break
            t2 = (t2 * t2) % p
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r

def ec_gen_points_set(a, b, p):
    ec_points_on_curve = []
    for x in range(p):
        y2 = x ** 3 + a * x + b
        lengdre_val = legendre(y2, p)
        if lengdre_val != 0:
            if lengdre_val != 1:  # (y2 | p) must be ≡ 1 to have a square if not continue to next num
                continue
        elif lengdre_val == 0:
            y_root1 = 0
            gen1 = (x, y_root1)
            ec_points_on_curve.append(gen1)
            continue
        y_root1 = tonelli(y2, p)  # one possible root
        y_root2 = p - y_root1

        if y_root2 < y_root1:
            gen1 = (x, y_root2)
            gen2 = (x, y_root1)
        else:
            gen1 = (x, y_root1)
            gen2 = (x, y_root2)

        ec_points_on_curve.append(gen1)
        ec_points_on_curve.append(gen2)
    return ec_points_on_curve

def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient * x, x
        y, lasty = lasty - quotient * y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)


# calculate `modular inverse`
def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g == 1:
        return x % m
    else:
        return None

#OPERACIONES ECC
# double function
def ecc_double(x1, y1, p, a):
    if modinv(2 * y1, p) is None: return None

    s = ((3 * (x1 ** 2) + a) * modinv(2 * y1, p)) % p
    x3 = (s ** 2 - x1 - x1) % p
    y3 = (s * (x1 - x3) - y1) % p
    return (x3, y3)


# add function
def ecc_add(x1, y1, x2, y2, p, a):
    s = 0
    if (x1 == x2):
        if modinv(2 * y1, p) is None : return None
        s = ((3 * (x1 ** 2) + a) * modinv(2 * y1, p)) % p
    else:
        if modinv(x2 - x1, p) is None: return None
        s = ((y2 - y1) * modinv(x2 - x1, p)) % p
    x3 = (s ** 2 - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p
    return (x3, y3)


def double_and_add(multi, generator, p, a):
    (x3, y3) = (0, 0)
    (x1, y1) = generator
    (x_tmp, y_tmp) = generator
    init = 0
    for i in str(bin(multi)[2:]):
        if (i == '1') and (init == 0):
            init = 1
        elif (i == '1') and (init == 1):
            if ecc_double(x_tmp, y_tmp, p, a) is None: return None
            if ecc_add(x1, y1, x3, y3, p, a) is None: return None
            (x3, y3) = ecc_double(x_tmp, y_tmp, p, a)
            (x3, y3) = ecc_add(x1, y1, x3, y3, p, a)
            (x_tmp, y_tmp) = (x3, y3)
        else:
            if ecc_double(x_tmp, y_tmp, p, a) is None: return None
            (x3, y3) = ecc_double(x_tmp, y_tmp, p, a)
            (x_tmp, y_tmp) = (x3, y3)
    return (x3, y3)


def scale_point_set(a, b, p, generator):
    ec_curve_points = ec_gen_points_set(a, b, p)
    scaled_points_set = {}
    i = 1
    scaled_points_set[str(i) + "P"] = generator

    while True:
        i += 1
        scaled_point = double_and_add(i, generator, p, a)

        if scaled_point is None or scaled_point not in ec_curve_points:
            scaled_points_set[str(i) + "P"] = "O"
            break

        elif scaled_point in ec_curve_points:
            scaled_points_set[str(i) + "P"] = scaled_point
            if str(i) + "P" != "2P" and scaled_points_set["2P"] == scaled_points_set[str(i) + "P"]:  # the current index is not 2P and no other duplicate point exists
                scaled_points_set[str(i) + "P"] = "O"
                break    #if duplicate P exists then stop

    return scaled_points_set

def KeyGen(key, pointSet):
    order = len(pointSet)
    if key > order:
        key = key % order

        if key == 0: return pointSet[str(order) + "P"]  # if the modulo is zero return the last element in list

        key = pointSet[str(key) + "P"]  # User Public Key
    else:
        key = pointSet[str(key) + "P"]  # User Public Key

    return key

# agoritmo extendido de euclides que toma 2 primos relativos y les encuentra inverso modular
def Inverse_Mod(e, m):
    m0 = m
    y = 0
    x = 1
    if (m == 1):
        return 0
    while (e > 1):
        q = int(e / m)  # q is quotient
        temp = m
        m = e % m
        e = temp
        temp = y
        # Update x and y
        y = x - q * y
        x = temp
    # Make x positive
    if (x < 0): x = x + m0
    return x
def primitivo(a,b,p):
	for x in range(1,p):
		val=((x*x*x)+a*x+b) % p
		res = math.sqrt(val)
		if (abs(res-int(res))<0.0001):
			return(x,int(res))

def cifrarMenezesVanestone(text):
    file_in = open("pub_key_MV.txt", "r")
    a = int(file_in.readline().rstrip())
    b = int(file_in.readline().rstrip())
    p = int(file_in.readline().rstrip())
    gx = int(file_in.readline().rstrip())
    gy = int(file_in.readline().rstrip())
    Nb = int(file_in.readline().rstrip())
    file_in.close()
    file_in = open("priv_key_MV.txt", "r")
    Ka = int(file_in.read())
    file_in.close()
    cifrado=[]
    generator=(gx,gy)
    y0 = KeyGen(Ka, scale_point_set(a, b, p, generator))
    publicKeyB = KeyGen(Nb, scale_point_set(a, b, p, generator))
    mask = KeyGen(Ka, scale_point_set(a, b, p, publicKeyB))
    for i in range(len(text)):
        m=str(ord(text[i]))
        if((len(m)%2)!=0):
            m1 = int(m[:(len(m)//2)+1])
            m2 = int(m[len(m)//2+1:])
        else:
            m1 = int(m[:(len(m)//2)])
            m2 = int(m[len(m)//2:])
        y1 = (mask[0]*m1)%p
        y2 = (mask[1]*m2)%p
        cifrado.append((y0,y1,y2))
    #print("(C1,C2)):", mask)
    return(cifrado)
  
def descifrarMenezesVanestone(tcifrado):
    file_in = open("pub_key_MV.txt", "r")
    a = int(file_in.readline().rstrip())
    b = int(file_in.readline().rstrip())
    p = int(file_in.readline().rstrip())
    gx = int(file_in.readline().rstrip())
    gy = int(file_in.readline().rstrip())
    Nb = int(file_in.readline().rstrip())
    file_in.close()
    TextoDecifrado=""
    for i in range(len(tcifrado)):
        Nb_hint= KeyGen(Nb, scale_point_set(a, b, p, tcifrado[i][0]))
        inv_c1 = Inverse_Mod(Nb_hint[0],p)
        decrypt_m1 = (inv_c1*tcifrado[i][1])%p
        inv_c2 = Inverse_Mod(Nb_hint[1],p)
        decrypt_m2 = (inv_c2*tcifrado[i][2])%p
        TextoDecifrado = TextoDecifrado + chr(int(str(decrypt_m1) + str(decrypt_m2)))
    return TextoDecifrado

def generateMvData(p):
    if p=="":
        p=randprime(100,1000)
    else:
        p=int(p)
    a=random.randint(0,100)
    b=random.randint(0,100)
    gx,gy=primitivo(a,b,p)
    ca=random.randint(10**2,10**3)
    while(ca>p):
        ca=random.randint(10**2,10**3)
    cb=random.randint(10**2,10**3)
    while(cb>p):
        cb=random.randint(10**2,10**3)
    file_out = open("pub_key_MV.txt", "w")
    file_out.write(str(a))
    file_out.write("\n")
    file_out.write(str(b))
    file_out.write("\n")
    file_out.write(str(p))
    file_out.write("\n")
    file_out.write(str(gx))
    file_out.write("\n")
    file_out.write(str(gy))
    file_out.write("\n")
    file_out.write(str(cb))
    file_out.close()
    file_out = open("priv_key_MV.txt", "w")
    file_out.write(str(ca))
    file_out.close()
    return a,b,p,gx, gy, ca, cb