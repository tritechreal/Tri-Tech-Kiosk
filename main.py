import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.base import runTouchApp
from kivy.uix.screenmanager import ScreenManager, Screen
#these are the imports                                                  imports for moduals 

sm = ScreenManager()
screen = Screen(name='mainpage')

class TestApp(App):

    def build(self):
        grid = GridLayout(cols=5, rows=1) #defigns the rows and coloms for the grid of this screen

        def callback(instance, value):
            print('My button <%s> state is <%s>' % (instance, value)) #figure this out pls
            if instance == "0x0000017ABF501710": #This line dosent work
                if value == "down":
                    print("Goto Signing Screen")
        btn1 = Button(text='Hello world 1')
        btn1.bind(state=callback)


        sign_in = Button(text='Sign In')
        sign_in.bind(state=callback)
        #These are not needed so they can be gone
        
        #grid.add_widget(Button(text="Upload Fish"))
        #grid.add_widget(Button(text="Leaderboard"))
        #grid.add_widget(Button(text="Fish Stats"))
        #grid.add_widget(Button(text="Sign in"))
        
        grid.add_widget(btn1)
        grid.add_widget(sign_in)
        
        screen = Screen(name='sign in')
        sm.add_widget(screen)
        return grid
        
if __name__ == '__main__':
    TestApp().run() #runs main code