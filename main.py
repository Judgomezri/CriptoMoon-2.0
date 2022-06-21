from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import PublicKey as pk
import PublicKeySignature as pks
from sympy import randprime
from kivy.uix.popup import Popup 
import Image as im

#Loading the interface properties
#Builder.load_file('CriptoMoon.kv')

auxtext=""
def list_to_str(list):
    s=[]
    for i in range(0,len(list)):
        s.append(str(list[i]))
    cstring="----".join(s)
    return cstring

def str_to_list(text):
  lista=text.split("----") #esto transforma de nuevo el texto de numeros a lista
  s=[]
  for i in range(0,len(lista)):
    s.append(int(lista[i]))
  return s

# Declare both screens
class MenuScreen(Screen):
    pass
class LlavePublica_Screen(Screen):
    def spinner_clicked(self, cifrador, grid, primo1, primo2, data1, data2, data3, data4, data5):
        primo1.select_all(); primo1.delete_selection()
        primo2.select_all(); primo2.delete_selection()
        data1.select_all(); data1.delete_selection()
        data2.select_all(); data2.delete_selection()
        data3.select_all(); data3.delete_selection()
        data4.select_all(); data4.delete_selection()
        data5.select_all(); data5.delete_selection()
        if cifrador == "RSA" or cifrador=="Rabin" or cifrador=="ElGamal" or cifrador=="Menezes Vanestone":
            grid.visible = True
        else:
            grid.visible = False

    def generarPrimos(self, cifrador, widget, widget2):
        if cifrador== "RSA":
            primo1=str(pk.generatePrime())
            primo2=str(pk.generatePrime())
            widget.select_all(); widget.delete_selection()    
            widget.insert_text(primo1)
            widget2.select_all(); widget2.delete_selection()    
            widget2.insert_text(primo2)
        elif cifrador== "Rabin":
            primo1=pk.generatePrime()
            while(primo1%4!=3):
                primo1=pk.generatePrime()
            primo2=pk.generatePrime()
            while(primo2%4!=3):
                primo2=pk.generatePrime()
            widget.select_all(); widget.delete_selection()    
            widget.insert_text(str(primo1))
            widget2.select_all(); widget.delete_selection()    
            widget2.insert_text(str(primo2))
        elif cifrador== "ElGamal":
            primo1=str(pk.generatePrime())
            widget.select_all(); widget.delete_selection()    
            widget.insert_text(primo1)
        elif cifrador== "Menezes Vanestone":
            primo1=str(pk.generatePrime(10))
            widget.select_all(); widget.delete_selection()    
            widget.insert_text(primo1)

    def generarDatos(self, cifrador, primo1, primo2, data1, data2, data3, data4, data5):
        if cifrador== "RSA":
            n, phi, pub_key = pk.generateRsaData(int(primo1.text), int(primo2.text))
            data1.select_all(); data1.delete_selection()    
            data1.insert_text(str(n))
            data2.select_all(); data2.delete_selection()    
            data2.insert_text(str(phi))
            data3.select_all(); data3.delete_selection()    
            data3.insert_text(str(pub_key))
        elif cifrador== "Rabin":
            n = pk.generateRabinData(int(primo1.text),int(primo2.text))
            data1.select_all(); data1.delete_selection()    
            data1.insert_text(str(n))
        elif cifrador== "ElGamal":
            alpha, beta = pk.generateElgamalData(int(primo1.text))
            data1.select_all(); data1.delete_selection()    
            data1.insert_text(str(alpha))
            data2.select_all(); data2.delete_selection()    
            data2.insert_text(str(beta))
        elif cifrador== "Menezes Vanestone":
            a,b,p,gx, gy, ca, cb = pk.generateMvData(int(primo1.text))
            data1.select_all(); data1.delete_selection()    
            data1.insert_text(str(a))
            data2.select_all(); data2.delete_selection()    
            data2.insert_text(str(b))
            data4.select_all(); data4.delete_selection()    
            data4.insert_text(str(gx))
            data5.select_all(); data5.delete_selection()    
            data5.insert_text(str(gy))
        else:
            pass
    def cifrar(self, cifrador, primo1, primo2, data1, data2, data3, data4, data5, Texto, Resultado):
        if cifrador== "RSA":
            text=pk.cifrarRSA(Texto.text, int(data1.text), int(data3.text))
            text=list_to_str(text)
            Resultado.select_all(); Resultado.delete_selection()   
            Resultado.insert_text(text)
        elif cifrador== "Rabin":
            text=pk.cifrarRabin(Texto.text, int(data1.text))
            text=list_to_str(text)
            Resultado.select_all(); Resultado.delete_selection()   
            Resultado.insert_text(text)
        elif cifrador== "ElGamal":
            text=pk.cifrarElgamal(Texto.text, int(primo1.text), int(data2.text), int(data1.text))
            text=list_to_str(text)
            Resultado.select_all(); Resultado.delete_selection()   
            Resultado.insert_text(text)
        elif cifrador== "Menezes Vanestone":
            text=pk.cifrarMenezesVanestone(Texto.text)
            Resultado.select_all(); Resultado.delete_selection()   
            Resultado.insert_text(str(pk.cifrarMenezesVanestone(Texto.text)))

    def descifrar(self, cifrador, primo1, primo2, data1, data2, data3, data4, data5, Texto, Resultado):
        if cifrador== "RSA":
            text=str_to_list(Texto.text)
            Resultado.select_all(); Resultado.delete_selection()
            Resultado.insert_text(pk.descifrarRSA(text, int(data1.text)))
        elif cifrador=="Rabin":
            text=str_to_list(Texto.text)
            text=pk.descifrarRabin(text)
            if int(primo1.text)>99999:
                posibleText = ""
                for i in text:
                    for j in i:
                        if len(j)==3:
                            posibleText=posibleText+j
                text=posibleText
            Resultado.select_all(); Resultado.delete_selection()
            Resultado.insert_text(str(text))
        elif cifrador=="ElGamal":
            text=str_to_list(Texto.text)
            Resultado.select_all(); Resultado.delete_selection()
            Resultado.insert_text(str(pk.descifrarElgamal(text)))
        elif cifrador=="Menezes Vanestone":
            text=list(Texto.text)
            text[0]='['
            text[-1]=']'
            text="".join(text).replace(" ","").replace("},{","],[").replace("{","(").replace("}",")")
            text="["+text+"]"
            text = list(text)
            text[1]=""
            text[-2]=""
            text="".join(text)
            print(text)
            text=eval(text)
            Resultado.select_all(); Resultado.delete_selection()
            Resultado.insert_text(str(pk.descifrarMenezesVanestone(text)))

class FirmaDigital_Screen(Screen):
    def changeStyle(self,text):
        if text== "Icon":
            return "List", 'icon'
        else: return "Icon", 'list'
    def aplicarRuta(self, ruta, files):
        files.path=ruta.text
        if files.path!=ruta.text:
            ruta.text=files.path
            files.path=ruta.text
    def firmar(self, file, cifrador):
        bool=False
        try:
            if cifrador=="RSA":
                file=str(file[0])
                bool=pks.firmarRSA(file)
            elif cifrador=="ElGamal":
                file=str(file[0])
                bool=pks.firmarGamal(file)
            elif cifrador=="Menezes Vanestone":
                file=str(file[0])
                bool=pks.firmarMV(file)
        except:
            pass
        if (bool):
            Popup_Screen().setText("La firma ha sido generada.")
            Popup_Screen().open()
        else:
            Popup_Screen().setText("No se ha realizado la firma, revise que el archivo sea válido.")
            Popup_Screen().open()
    def verificar(self, file, cifrador):
        
        bool=False
        
        try:
            if cifrador=="RSA":
                file=str(file[0])
                bool=pks.verificarRSA(file)
            elif cifrador=="ElGamal":
                file=str(file[0])
                bool=pks.verificarGamal(file)
            elif cifrador=="Menezes Vanestone":
                file=str(file[0])
                bool=pks.verificarMV(file)
        except:
            pass
        if (bool):
            Popup_Screen().setText("El archivo ha sido verificado.")
            Popup_Screen().open()
        else:
            Popup_Screen().setText("El archivo o la clave han sido modificados.")
            Popup_Screen().open()

class Imagenes_Screen(Screen):
    def changeStyle(self,text):
        if text== "Icon":
            return "List", 'icon'
        else: return "Icon", 'list'
    def cifrar(self, image, A, B):
        im.encriptarImage(image.source, image, A, B)

class Popup_Screen(Popup):
    def setText(self, texto):
        global auxtext
        auxtext= texto
    def getText(self):
        return auxtext

class CriptoMoon(App):
    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(LlavePublica_Screen(name='LlavePublica'))
        sm.add_widget(FirmaDigital_Screen(name='FirmaDigital'))
        sm.add_widget(Imagenes_Screen(name='Imagenes'))
        return sm

if __name__ == '__main__':
    CriptoMoon().run()