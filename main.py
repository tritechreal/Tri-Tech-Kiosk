from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# Create  screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        Button:
            text: 'Goto settings'
            on_press: root.manager.current = 'settings'
        Button:
            text: 'Account'
            on_press: root.manager.current = 'Account'
        Button:
            text: 'Quit'

<SettingsScreen>:
    BoxLayout:
        Button:
            text: 'My settings button'
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'
<Account>:
    BoxLayout:
        Button:
            text: 'Sign In'
            on_press: root.manager.current = 'sign_in'
        Button:
            text: 'Sign Up'
            on_press: root.manager.current = 'sign_up'
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'
                    
<Sign_In>:
    BoxLayout:
        Button:
            text: 'Email'
            
        Button:
            text: 'Password'
    
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'

<Sign_Up>:
    BoxLayout:
        Button:
            text: 'Email'
            
        Button:
            text: 'Password'
    
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'
""")

# Declare all screens
class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class Account(Screen):
    pass

class Sign_In(Screen):
    pass

class Sign_Up(Screen):
    pass

class TestApp(App):

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(Account(name='Account'))
        sm.add_widget(Sign_In(name='sign_in'))
        sm.add_widget(Sign_Up(name='sign_up'))

        return sm

if __name__ == '__main__':
    TestApp().run()