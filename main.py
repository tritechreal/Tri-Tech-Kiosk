import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
from kivy.uix.screenmanager import ScreenManager, Screen
#these are the imports

sm = ScreenManager()
screen = Screen(name='mainpage')

class TestApp(App):

    def build(self):
        grid = GridLayout(cols=4, rows=1)
        grid.add_widget(Button(text="Upload Fish"))
        grid.add_widget(Button(text="Leaderboard"))
        grid.add_widget(Button(text="Fish Stats"))
        grid.add_widget(Button(text="Sign in"))
        
        screen = Screen(name='sign in')
        sm.add_widget(screen)
        return grid
        
if __name__ == '__main__':
    TestApp().run()