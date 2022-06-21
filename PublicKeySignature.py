<<<<<<< HEAD
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import base64
import PublicKey as pk
import math
import random



####RSA--------------------------------------
def CrearClavesFirmaRSA():
    key = RSA.generate(2048)
    private_key = key.export_key()
    file_out = open("private_RSA.key", "wb")
    file_out.write(private_key)
    file_out.close()
    public_key = key.publickey().export_key()
    file_out = open("public_RSA.key", "wb")
    file_out.write(public_key)
    file_out.close()

###########################################

def firmarRSA(file):
    CrearClavesFirmaRSA()
    with open(file,"rb") as opened_file:
        f=base64.b64encode(opened_file.read())
    privatekey = RSA.import_key(open('private_RSA.key').read())
    h = SHA256.new(f)
    signer=pkcs1_15.new(privatekey)
    signature=signer.sign(h)
    file_out = open("firma_RSA.pem", "wb")
    file_out.write(signature)
    file_out.close()
    return True
    #print(signature.hex())

########################################################

def verificarRSA(file):
    publickey = RSA.import_key(open("public_RSA.key").read())
    file_in = open(file, "rb")
    with file_in as opened_file:
        message=base64.b64encode(opened_file.read())
    file_in.close()
    file_in = open("firma_RSA.pem", "rb")
    signature=file_in.read()
    file_in.close()
    h = SHA256.new(message)
    try:
        pkcs1_15.new(publickey).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False

######ElGamal---------------------

def primoRelativo(p):
    h= random.randint(0,p)
    while math. gcd(p,h)!=1:
        h=random.randint(0,p)
    return h

#############################################################################

def CrearClavesFirmaGamal(p):
    alpha=random.randint(2,p)
    a= pk.gen_key(p)
    beta=pow(alpha,a,p)
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

#############################################################################    
    
def firmarGamal(file):
    p= pk.generatePrime()
    CrearClavesFirmaGamal(p)
    with open(file,"rb") as opened_file:
        f=base64.b64encode(opened_file.read())    
    H = SHA256.new(f)
    H=H.hexdigest()
    H=int(H, 16)    
    h=primoRelativo(p-1)
    h_inv=pk.multiplicative_inverse(h,p-1)    
    
    
    with open("pub_key_elgamal.txt") as f:
        lines = f.readlines()        
        alpha = int(lines[1].rstrip())        
        f.close()
    with open("priv_key_elgamal.txt") as f:
        lines = f.readlines()
        a=int(lines[0].rstrip())
        f.close()
    
    r=pow(alpha,h,p)    
    s=((H-(a*r))*h_inv)%(p-1)
    file_out = open("firma_gamal.txt", "w")
    file_out.write(str(r))
    file_out.write("\n")
    file_out.write(str(s))
    file_out.close()
    
    
    return True


#############################################################################

def verificarGamal(file):
    with open("pub_key_elgamal.txt") as f:
        lines = f.readlines()
        p=int(lines[0].rstrip())
        alpha = int(lines[1].rstrip())
        beta = int(lines[2].rstrip())
        f.close()
    with open("firma_gamal.txt") as f:
        lines = f.readlines()
        r=int(lines[0].rstrip())
        s = int(lines[1].rstrip())       
        f.close()
    with open(file,"rb") as opened_file:
        f=base64.b64encode(opened_file.read())
    H = SHA256.new(f)
    H=H.hexdigest()
    H=int(H, 16)
    k1=pow(r,s,p)
    k2=pow(beta,r,p)
    k=(k1*k2)%p
    k_H=pow(alpha,H,p)
    return k==k_H


#####Meneses Vanestone-------------------------------------------
def CrearClavesFirmaMV():
    key = ECC.generate(curve='P-256')
    private_key = key.export_key(format='PEM')
    file_out = open("private.key", "wt")
    file_out.write(private_key)
    file_out.close()
    public_key = key.public_key().export_key(format='PEM')
    file_out = open("public.key", "wt")
    file_out.write(public_key)
    file_out.close()

###########################################

def firmarMV(file):
    CrearClavesFirmaMV()
    with open(file,"rb") as opened_file:
        f=base64.b64encode(opened_file.read())
    privatekey = ECC.import_key(open('private.key').read())
    h = SHA256.new(f)
    signer=DSS.new(privatekey,'fips-186-3')
    signature=signer.sign(h)
    file_out = open("firma_mv.pem", "wb")
    file_out.write(signature)
    file_out.close()
    return True
    #print(signature.hex())

########################################################

def verificarMV(file):
    publickey = ECC.import_key(open("public.key").read())
    file_in = open(file, "rb")
    with file_in as opened_file:
        message=base64.b64encode(opened_file.read())
    file_in.close()
    file_in = open("firma_mv.pem", "rb")
    signature=file_in.read()
    file_in.close()
    h = SHA256.new(message)
    try:
        DSS.new(publickey,'fips-186-3').verify(h, signature)
        return True
    except (ValueError, TypeError):
=======
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import base64
import PublicKey as pk
import math
import random



####RSA--------------------------------------
def CrearClavesFirmaRSA():
    key = RSA.generate(2048)
    private_key = key.export_key()
    file_out = open("private_RSA.key", "wb")
    file_out.write(private_key)
    file_out.close()
    public_key = key.publickey().export_key()
    file_out = open("public_RSA.key", "wb")
    file_out.write(public_key)
    file_out.close()

###########################################

def firmarRSA(file):
    CrearClavesFirmaRSA()
    with open(file,"rb") as opened_file:
        f=base64.b64encode(opened_file.read())
    privatekey = RSA.import_key(open('private_RSA.key').read())
    h = SHA256.new(f)
    signer=pkcs1_15.new(privatekey)
    signature=signer.sign(h)
    file_out = open("firma_RSA.pem", "wb")
    file_out.write(signature)
    file_out.close()
    return True
    #print(signature.hex())

########################################################

def verificarRSA(file):
    publickey = RSA.import_key(open("public_RSA.key").read())
    file_in = open(file, "rb")
    with file_in as opened_file:
        message=base64.b64encode(opened_file.read())
    file_in.close()
    file_in = open("firma_RSA.pem", "rb")
    signature=file_in.read()
    file_in.close()
    h = SHA256.new(message)
    try:
        pkcs1_15.new(publickey).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False

######ElGamal---------------------

def primoRelativo(p):
    h= random.randint(0,p)
    while math. gcd(p,h)!=1:
        h=random.randint(0,p)
    return h

#############################################################################

def CrearClavesFirmaGamal(p):
    alpha=random.randint(2,p)
    a= pk.gen_key(p)
    beta=pow(alpha,a,p)
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

#############################################################################    
    
def firmarGamal(file):
    p= pk.generatePrime()
    CrearClavesFirmaGamal(p)
    with open(file,"rb") as opened_file:
        f=base64.b64encode(opened_file.read())    
    H = SHA256.new(f)
    H=H.hexdigest()
    H=int(H, 16)    
    h=primoRelativo(p-1)
    h_inv=pk.multiplicative_inverse(h,p-1)    
    
    
    with open("pub_key_elgamal.txt") as f:
        lines = f.readlines()        
        alpha = int(lines[1].rstrip())        
        f.close()
    with open("priv_key_elgamal.txt") as f:
        lines = f.readlines()
        a=int(lines[0].rstrip())
        f.close()
    
    r=pow(alpha,h,p)    
    s=((H-(a*r))*h_inv)%(p-1)
    file_out = open("firma_gamal.txt", "w")
    file_out.write(str(r))
    file_out.write("\n")
    file_out.write(str(s))
    file_out.close()
    
    
    return True


#############################################################################

def verificarGamal(file):
    with open("pub_key_elgamal.txt") as f:
        lines = f.readlines()
        p=int(lines[0].rstrip())
        alpha = int(lines[1].rstrip())
        beta = int(lines[2].rstrip())
        f.close()
    with open("firma_gamal.txt") as f:
        lines = f.readlines()
        r=int(lines[0].rstrip())
        s = int(lines[1].rstrip())       
        f.close()
    with open(file,"rb") as opened_file:
        f=base64.b64encode(opened_file.read())
    H = SHA256.new(f)
    H=H.hexdigest()
    H=int(H, 16)
    k1=pow(r,s,p)
    k2=pow(beta,r,p)
    k=(k1*k2)%p
    k_H=pow(alpha,H,p)
    return k==k_H


#####Meneses Vanestone-------------------------------------------
def CrearClavesFirmaMV():
    key = ECC.generate(curve='P-256')
    private_key = key.export_key(format='PEM')
    file_out = open("private.key", "wt")
    file_out.write(private_key)
    file_out.close()
    public_key = key.public_key().export_key(format='PEM')
    file_out = open("public.key", "wt")
    file_out.write(public_key)
    file_out.close()

###########################################

def firmarMV(file):
    CrearClavesFirmaMV()
    with open(file,"rb") as opened_file:
        f=base64.b64encode(opened_file.read())
    privatekey = ECC.import_key(open('private.key').read())
    h = SHA256.new(f)
    signer=DSS.new(privatekey,'fips-186-3')
    signature=signer.sign(h)
    file_out = open("firma_mv.pem", "wb")
    file_out.write(signature)
    file_out.close()
    return True
    #print(signature.hex())

########################################################

def verificarMV(file):
    publickey = ECC.import_key(open("public.key").read())
    file_in = open(file, "rb")
    with file_in as opened_file:
        message=base64.b64encode(opened_file.read())
    file_in.close()
    file_in = open("firma_mv.pem", "rb")
    signature=file_in.read()
    file_in.close()
    h = SHA256.new(message)
    try:
        DSS.new(publickey,'fips-186-3').verify(h, signature)
        return True
    except (ValueError, TypeError):
>>>>>>> 20662e3aa2063c99a35bc59cc83beb0452acf3e6
        return False