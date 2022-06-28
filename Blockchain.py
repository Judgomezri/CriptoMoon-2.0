import hashlib
import binascii
import datetime
import collections
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
#se define la clase cliente que nos servira para crear transacciones
def generateKey(string, key="Blockchain"):
    key = list(key)
    if len(string) == len(key):
        return(key)
    else:
        for i in range(len(string) -
                       len(key)):
            key.append(key[i % len(key)])
    return("" . join(key))
def cifrarvigenere(string, key="Blockchain"):
    generateKey(string,key)
    cipher_text = []
    for i in range(len(string)):
        x = (ord(string[i]) +
             ord(key[i])) % 26
        x += ord('A')
        cipher_text.append(chr(x))
    return("" . join(cipher_text))
def decifrarVigenere(cipher_text, key):
    orig_text = []
    for i in range(len(cipher_text)):
        x = (ord(cipher_text[i]) -
             ord(key[i]) + 26) % 26
        x += ord('A')
        orig_text.append(chr(x))
    return("" . join(orig_text))
def cifrartransacciones(transacciones):
    for i in transacciones:
        cifrarvigenere(i,key="Blockchain")
def decifrartransacciones(transacciones):
    for i in transacciones:
        decifrarVigenere(i,key="Blockchain")
class Cliente:
    def __init__(self):
        random= Crypto.Random.new().read #numero random para generar la clave
        self.private_key = RSA.generate(1024,random) # se genera clave privada
        self.public_key = self.private_key.public_key() # se genera la clave publica que será la identidad del cliente
        self.signer = PKCS115_SigScheme(self.private_key) #firma
        self.identidad = binascii.hexlify(self.public_key.exportKey(format='DER'))
#Ejemplo
Daniel= Cliente()
Juan = Cliente()
Carlos = Cliente()
Agustin = Cliente()
#print(Daniel.identidad)

#####################################################################################

#se define la clase transacción que anota el dinero que se intercambia entre clientes
class Transaccion:
    def __init__(self,remitente,destinatario,valor): #remitente y destintario se refiere a su identidad o clave pública
        self.remitente=remitente
        self.destinatario= destinatario
        self.valor=valor #En este caso seran las Moon Coins SIUUUUUUUUUU
        self.time= datetime.datetime.now()
    def diccionario(self): # simplemente es guardar todos los datos de la transaccion en una sola variable para que sea mas facil de leer y trabajar
        if self.remitente == "Genesis":
            identidad="Genesis"
        else:
            identidad=self.remitente.identidad
        return collections.OrderedDict({
            'Remitente': identidad,
            'Destinatario': self.destinatario,
            'Valor':self.valor,
            'Tiempo': self.time})
    def firmar_transaccion(self): #firmamos la transación con la clave privada del remitente
        private_key= self.remitente.private_key
        firmaRemitente= PKCS115_SigScheme(private_key) #libreria
        h = SHA.new(str(self.diccionario()).encode('utf8'))
        firma=firmaRemitente.sign(h)
        return firma

def mostrarTransaccion(transaccion):
    dict= transaccion.diccionario()
    Rem = "Remitente: " + str(dict['Remitente'])+"\n"
    #print("Remitente: " + str(dict['Remitente']))
    Dest = "Destinatario: " + str(dict['Destinatario'])+"\n"
    #print("Destinatario: " + str(dict['Destinatario']))
    Valor = "Valor: " + str(dict['Valor'])+"\n"
    #print("Valor: " + str(dict['Valor']))
    Tiempo = "Tiempo: " + str(dict['Tiempo'])+"\n"
    #print("Tiempo: " + str(dict['Tiempo']))
    Separador = "-----"+"\n"
    #print("-----")
    return ([Rem, Dest, Valor, Tiempo, Separador])

Transacciones=[]
firmas=[]
t0 = Transaccion("Genesis",Daniel.identidad,500)

def AñadirTransacción(Remitente,Destinatario,MC): #mc moon coins
    global Transacciones
    t=Transaccion(Remitente,Destinatario,MC)
    Transacciones.append(t)
    firmas.append(t.firmar_transaccion())
    return (t)
#AñadirTransacción(Daniel,Juan.identidad,5.0)
#AñadirTransacción(Carlos,Agustin.identidad,7.0)
#AñadirTransacción(Agustin,Bob.identidad,6.0)
#AñadirTransacción(Bob,Daniel.identidad,10.0)
#AñadirTransacción(Juan,Daniel.identidad,50.0)
#AñadirTransacción(Agustin,Carlos.identidad,40.0)
'''
#para ver todas las transacciones
for transaccion in Transacciones:
    mostrarTransaccion(transaccion)
    print("--------")
'''

#print(t.diccionario())
#print(firma)

#####################################################################################
class Bloque:
    def __init__(self):
        self.transacciones_verificadas = []
        self.anterior_hash = ""
        self.Nonce = ""  #guardamos el nonce generado por el minero siuuuuuuu

def Full_blockchain(Bloques):
    Final = []
    Final.append("el número de bloques en la cadena es de: " + str(len(Bloques))+"\n")
    #print("el número de bloques en la cadena es de: " + str(len(Bloques)))
    for x in range(len(MoonCoins)):
        block_temp= MoonCoins[x]
        Final.append("block #" + str(x)+"\n")
        #print("block #" + str(x))
        Final.append("el hash del bloque encontrado por el minero es: " + str(block_temp.Nonce)+"\n")
        #print("el hash del bloque encontrado por el minero es: " + str(block_temp.Nonce))
        for Transaccion in block_temp.transacciones_verificadas:
            trans = mostrarTransaccion(Transaccion)
            for i in trans:
                Final.append(i)
        Final.append("===================================")
        #print("=====================================")
    return Final
ultimo_hash=""
bloque0=Bloque() #para genesis
bloque0.anterior_hash=None
bloque0.Nonce=None
bloque0.transacciones_verificadas.append(t0)
bloque_hash=hash(bloque0)
ultimo_hash=bloque_hash
MoonCoins=[]
MoonCoins.append(bloque0)
indice_ultima_transaccion= 0
def sha256(message):
 return hashlib.sha256(message.encode('ascii')).hexdigest()
def minar(mensaje,dificultad):
    assert dificultad>=1
    prefix='0'*dificultad
    i=0
    bool = True
    while bool:
        hashi= sha256(str(hash(mensaje)) + str(i))
        if hashi.startswith(prefix):
            bool=False
            #print("despues de " + str(i)+" intentos se encontró el nonce: "+ hashi)
            return hashi
        i=i+1
def agregarbloque():
    global indice_ultima_transaccion
    global ultimo_hash
    block = Bloque()
    j = 0
    try:
        for i in range(3):
            Transaccion_Actual=Transacciones[indice_ultima_transaccion]
            public_key = Transaccion_Actual.remitente.public_key
            h = SHA.new(str(Transaccion_Actual.diccionario()).encode('utf8'))
            verificador = PKCS115_SigScheme(public_key)
            try:
              verificador.verify(h,firmas[indice_ultima_transaccion])
              block.transacciones_verificadas.append(Transaccion_Actual)
              indice_ultima_transaccion+=1
              j+=1
              #print("transaccion valida")
            except:
                print("hubo un error añadiendo las transacciones parece que la firma no coincide")
        block.anterior_hash = ultimo_hash
        block.Nonce = minar(block, 4) #note que tenemos que hashear el bloque para agregarlo
        MoonCoins.append(block)
        ultimo_hash = hash((block))
    except:
        print("parece que no hay suficientes transacciones para generar un bloque")
        indice_ultima_transaccion = indice_ultima_transaccion-j
        return 0
    return 1
    

#minero 1 agrega un bloque
#agregarbloque()
#minero 2 agrega un bloque
#agregarbloque()
#AñadirTransacción(Juan,Agustin.identidad,30.0)
#AñadirTransacción(Juan,Agustin.identidad,30.0)
#agregarbloque()
#print(Full_blockchain(MoonCoins))
#####################################################################################

a = "prueba"