from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import PublicKey as pk
from sympy import randprime

#Loading the interface properties
Builder.load_file('CriptoMoon.kv')

# Declare both screens
class MenuScreen(Screen):
    pass
class LlavePublica_Screen(Screen):
    def spinner_clicked(self, cifrador, grid):
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
            widget2.select_all(); widget.delete_selection()    
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

    def generarDatos(self, cifrador, primo1, primo2, data1, data2, data3, data4, data5):
        if cifrador== "RSA":
            n, phi, pub_key = pk.generateRsaData(int(primo1.text), int(primo2.text))
            data1.select_all(); data1.delete_selection()    
            data1.insert_text(str(n))
            data2.select_all(); data1.delete_selection()    
            data2.insert_text(str(phi))
            data3.select_all(); data1.delete_selection()    
            data3.insert_text(str(pub_key))
        elif cifrador== "Rabin":
            n = pk.generateRabinData(int(primo1.text),int(primo2.text))
            data1.select_all(); data1.delete_selection()    
            data1.insert_text(str(n))
        elif cifrador== "ElGamal":
            alpha, beta = pk.generateElgamalData(int(primo1.text))
            data1.select_all(); data1.delete_selection()    
            data1.insert_text(str(alpha))
            data2.select_all(); data1.delete_selection()    
            data2.insert_text(str(beta))
        else:
            pass
    def cifrar(self, cifrador, primo1, primo2, data1, data2, data3, data4, data5, Texto, Resultado):
        if cifrador== "RSA":
            Resultado.select_all(); Resultado.delete_selection()   
            Resultado.insert_text(str(pk.cifrarRSA(Texto.text, int(data1.text), int(data3.text))))
        elif cifrador== "Rabin":
            Resultado.select_all(); Resultado.delete_selection()   
            Resultado.insert_text(str(pk.cifrarRabin(Texto.text, int(data1.text))))

    def descifrar(self, cifrador, primo1, primo2, data1, data2, data3, data4, data5, Texto, Resultado):
        if cifrador== "RSA":
            Resultado.select_all(); Resultado.delete_selection()
            Resultado.insert_text(str(pk.descifrarRSA(Texto.text, int(data1.text))))
        elif cifrador=="Rabin":
            Resultado.select_all(); Resultado.delete_selection()
            Resultado.insert_text(str(pk.descifrarRabin(Texto.text, int(data1.text))))

class CriptoMoon(App):
    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(LlavePublica_Screen(name='LlavePublica'))
        return sm

if __name__ == '__main__':
    CriptoMoon().run()