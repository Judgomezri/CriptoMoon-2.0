from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

#Loading the interface properties
Builder.load_file('CriptoMoon.kv')

# Declare both screens
class MenuScreen(Screen):
    pass
class LlavePublica_Screen(Screen):

    def spinner_clicked(self, cifrador):
        pass

class CriptoMoon(App):

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(LlavePublica_Screen(name='LlavePublica'))

        return sm

if __name__ == '__main__':
    CriptoMoon().run()