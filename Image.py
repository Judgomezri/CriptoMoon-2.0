from PIL import Image
import random
import itertools

#Espacio de color RGB
#siglas en español
N=(0,0,0)
R=(255,0,0)
Az=(0,0,255)
V=(0,255,0)
Aq=(0,255,255)
F=(255,0,255)
Am=(255,255,0)
Bl=(255,255,255)

#NEGRO
Y_N=[[N,N,N,N],[N,N,N,N],[N,N,N,N],[N,N,N,N]]
C_N=[[[N,R,N,N],[V,N,N,N],[N,N,Az,N],[Bl,N,N,N]],[[N,N,V,N],[N,N,R,N],[N,N,N,Bl],[N,N,Az,N]]]

#ROJO
Y_R=[[N,N,N,R],[N,N,N,N],[N,N,N,N],[N,N,N,N]]
C_R=[[[N,N,N,R],[N,V,N,N],[N,Az,N,N],[N,N,N,Bl]],[[N,N,N,Bl],[V,N,N,N],[N,N,R,N],[N,N,Az,N]]]

#AZUL
Y_Az=[[N,N,N,Az],[N,N,N,N],[N,N,N,N],[N,N,N,N]]
C_Az=[[[N,N,N,Az],[N,N,N,R],[N,N,N,V],[N,N,N,Bl]],[[N,N,N,Bl],[N,N,R,N],[Az,N,N,N],[V,N,N,N]]]

#VERDE
Y_V=[[N,N,N,V],[N,N,N,N],[N,N,N,N],[N,N,N,N]]
C_V=[[[N,N,N,V],[N,N,N,R],[N,Az,N,N],[N,N,N,Bl]],[[N,N,N,Bl],[N,N,R,N],[Az,N,N,N],[V,N,N,N]]]

#CYAN
Y_Aq=[[N,N,N,Aq],[N,N,N,N],[N,N,N,N],[N,N,N,N]]
C_Aq=[[[N,N,N,V],[N,R,N,N],[N,Az,N,N],[N,N,N,Bl]],[[N,N,N,Az],[N,N,R,N],[Bl,N,N,N],[V,N,N,N]]]

#FUCSIA
Y_F=[[N,N,N,F],[N,N,N,N],[N,N,N,N],[N,N,N,N]]
C_F=[[[N,N,N,Az],[N,N,N,R],[N,N,N,V],[N,N,N,Bl]],[[N,N,N,R],[V,N,N,N],[Bl,N,N,N],[N,N,Az,N]]]

#AMARILLO
Y_Am=[[N,N,N,Am],[N,N,N,N],[N,N,N,N],[N,N,N,N]]
C_Am=[[[N,N,N,R],[N,V,N,N],[N,N,N,Bl],[N,N,N,Az]],[[N,N,N,V],[N,N,R,N],[Az,N,N,N],[N,N,Bl,N]]]

#BLANCO
Y_Bl=[[N,N,N,Bl],[N,N,N,N],[N,N,N,N],[N,N,N,N]]
C_Bl=[[[N,N,N,Bl],[N,N,N,R],[N,N,N,V],[N,Az,N,N]],[[N,N,N,Bl],[N,N,R,N],[Az,N,N,N],[V,N,N,N]]]

###############################################################################################################

def NormalizarImg(imagen):
    img = Image.open(imagen)
    img = img.convert("RGB")
    d = img.getdata()
    
    imagen_8color = []
    #cambia la imagen al espacio de color
    for item in d:        
        #cambiar a rojo
        if ((item[0]>(255/2)) and (item[1]<(255/2)) and (item[2]<(255/2))):
            imagen_8color.append(R)
            
               
        #cambiar a negro
        if ((item[0]<=(255/2)) and (item[1]<(255/2)) and (item[2]<(255/2))):
            imagen_8color.append(N)
            
         #cambiar a azul
        if ((item[0]<=(255/2)) and (item[1]<(255/2)) and (item[2]>=(255/2))):
            imagen_8color.append(Az)
            
         #cambiar a fucsia
        if ((item[0]>(255/2)) and (item[1]<(255/2)) and (item[2]>=(255/2))):
            imagen_8color.append(F)
            
         #cambiar a amarillo
        if ((item[0]>(255/2)) and (item[1]>=(255/2)) and (item[2]<(255/2))):
            imagen_8color.append(Am)
            
        #cambiar a verde
        if ((item[0]<=(255/2)) and (item[1]>=(255/2)) and (item[2]<(255/2))):
            imagen_8color.append(V)
            
         #cambiar a aqua
        if ((item[0]<=(255/2)) and (item[1]>=(255/2)) and (item[2]>=(255/2))):
            imagen_8color.append(Aq)
            
         #cambiar a blanco
        if ((item[0]>(255/2)) and (item[1]>=(255/2)) and (item[2]>=(255/2))):
            imagen_8color.append(Bl)
            
        
    ancho, alto=img.size
    img = Image.new('RGB', (ancho, alto), color=(0, 0, 0))
       
    # Actualiza los datos de la imgen
    img.putdata(imagen_8color)
    
    # guarda nueva imagen
    img.save("imagen_normalizada.jpg")
    return img, imagen_8color

###############################################################################################################

def permutar_matrices(Y,C):
    Aux_Y=[]
    Aux_C=[[],[]]
    Aux_Y0=[]
    Aux_C0=[[],[]]
    
    permutaciones_Y=list(itertools.permutations(Y))
    permutaciones_C0=list(itertools.permutations(C[0]))   
    permutaciones_C1=list(itertools.permutations(C[1]))
    num=random.randint(12, 24-1)
    
    Aux_Y0.append(list(permutaciones_Y[num]))
    Aux_C0[0].append(list(permutaciones_C0[num]))
    Aux_C0[1].append(list(permutaciones_C1[num]))
    
    Aux_Y0=list(itertools.chain(*Aux_Y0))
    Aux_C0[0]=list(itertools.chain(*Aux_C0[0]))
    Aux_C0[1]=list(itertools.chain(*Aux_C0[1]))
    
    for i in range(4):
        permutaciones_Y=list(itertools.permutations(Aux_Y0[i]))
        permutaciones_C0=list(itertools.permutations(Aux_C0[0][i]))   
        permutaciones_C1=list(itertools.permutations(Aux_C0[1][i]))
        num=random.randint(12, 24-1)
        Aux_Y.append(list(permutaciones_Y[num]))
        Aux_C[0].append(list(permutaciones_C0[num]))
        Aux_C[1].append(list(permutaciones_C1[num]))
    return Aux_Y, Aux_C

###############################################################################################################

def encriptarImage(imagen, muestra, A, B):
    datos_norml=NormalizarImg(imagen)
    muestra.source = "imagen_normalizada.jpg"
    imagen_T1T2=[]
    imagen_T1=[]
    imagen_T2=[]
    datos_imagen=datos_norml[0]
    datos_imagen_T1=datos_imagen
    datos_imagen_T2=datos_imagen

    datos_list=datos_norml[1]

    for item in datos_list:
             #ampliar rojo
            if (item==R):
                aux_permuto=permutar_matrices(Y_R,C_R)
                imagen_T1T2.append(aux_permuto[0])
                imagen_T1.append(aux_permuto[1][0])
                imagen_T2.append(aux_permuto[1][1])
            #ampliar negro
            if (item==N):
                aux_permuto=permutar_matrices(Y_N,C_N)
                imagen_T1T2.append(aux_permuto[0])
                imagen_T1.append(aux_permuto[1][0])
                imagen_T2.append(aux_permuto[1][1])

             #ampliar azul
            if (item==Az):
                aux_permuto=permutar_matrices(Y_Az,C_Az)
                imagen_T1T2.append(aux_permuto[0])
                imagen_T1.append(aux_permuto[1][0])
                imagen_T2.append(aux_permuto[1][1])

             #ampliar fucsia
            if (item==F):
                aux_permuto=permutar_matrices(Y_F,C_F)
                imagen_T1T2.append(aux_permuto[0])
                imagen_T1.append(aux_permuto[1][0])
                imagen_T2.append(aux_permuto[1][1])
             #ampliar amarillo
            if (item==Am):
                aux_permuto=permutar_matrices(Y_Am,C_Am)
                imagen_T1T2.append(aux_permuto[0])
                imagen_T1.append(aux_permuto[1][0])
                imagen_T2.append(aux_permuto[1][1])

            #ampliar verde
            if (item==V):
                aux_permuto=permutar_matrices(Y_V,C_V)
                imagen_T1T2.append(aux_permuto[0])
                imagen_T1.append(aux_permuto[1][0])
                imagen_T2.append(aux_permuto[1][1])

             #ampliar aqua
            if (item==Aq):
                aux_permuto=permutar_matrices(Y_Aq,C_Aq)
                imagen_T1T2.append(aux_permuto[0])
                imagen_T1.append(aux_permuto[1][0])
                imagen_T2.append(aux_permuto[1][1])

             #ampliar blanco
            if (item==Bl):
                aux_permuto=permutar_matrices(Y_Bl,C_Bl)
                imagen_T1T2.append(aux_permuto[0])
                imagen_T1.append(aux_permuto[1][0])
                imagen_T2.append(aux_permuto[1][1])

    #se acomodan los datos de las imagenes
    imagenes=[imagen_T1,imagen_T2,imagen_T1T2]
    ancho, alto=datos_imagen.size
    datos_imagenes=[]
    for i in range(3):            
        L0=[]
        L1=[]
        L2=[]
        L3=[]
        L=[]
        for item in imagenes[i]:
            L0.append(item[0])
            L1.append(item[1])
            L2.append(item[2])
            L3.append(item[3])

        L0=list(itertools.chain(*L0))
        L1=list(itertools.chain(*L1))
        L2=list(itertools.chain(*L2))
        L3=list(itertools.chain(*L3))

        j=len(L0)
        for i in range((j//(ancho*4))):
            L.append(L0[:ancho*4])
            L.append(L1[:ancho*4])
            L.append(L2[:ancho*4])
            L.append(L3[:ancho*4])
            L0=L0[ancho*4:]
            L1=L1[ancho*4:]
            L2=L2[ancho*4:]
            L3=L3[ancho*4:]
        L=list(itertools.chain(*L))
        datos_imagenes.append(L)
    
    #se crean imagenes de color negro del tamaño adecuado
    datos_imagen_T1 = Image.new('RGB', (ancho*4, alto*4), color=(0, 0, 0))
    datos_imagen_T2 = Image.new('RGB', (ancho*4, alto*4), color=(0, 0, 0))
    datos_imagen = Image.new('RGB', (ancho*4, alto*4), color=(0, 0, 0))
    
    
    #se cargan los datos a las imagenes 
    datos_imagen_T1.putdata(datos_imagenes[0])
    datos_imagen_T2.putdata(datos_imagenes[1])
    datos_imagen.putdata(datos_imagenes[2])
    #guardar imagenes
    datos_imagen_T1.save("T1.jpg")
    datos_imagen_T2.save("T2.jpg")
    datos_imagen.save("T1T2.jpg")
    A.source="T1.jpg"
    A.opacity= 1
    B.source="T2.jpg"
    B.opacity= 1
    return datos_imagen_T1, datos_imagen_T2, datos_imagen