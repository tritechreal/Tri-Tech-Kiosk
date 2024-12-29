from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
import Camera as C





#kv code for ui
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
            on_press: raise Exception("User quit program")

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
    
   
    GridLayout:

        rows: 3
        cols: 2
        padding: 10
        spacing: 10
        Label:  
            text: "Username"
        TextInput:
            id: username
            on_focus: app.update_user(self.text, self.focus)
            
            
        Label:
            text: "Password"
        TextInput:
            id: password
            password: True
            on_focus: app.update_pass(self.text, self.focus)
        Button:
            text: 'Done'
            on_press:
                if app.authenticate_user(): print("Login successful!")   
                else: print("error, no account found")
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'
                    
                
        
<Sign_Up>:
    GridLayout:

        rows: 3
        cols: 2
        padding: 10
        spacing: 10
        Label:  
            text: "Username"
        TextInput:
            id: username
            on_focus: app.update_user(self.text, self.focus)
            
            
        Label:
           
            text: "Password"
        TextInput:
            id: password
            password: True
            on_focus: app.update_pass(self.text, self.focus)
        Button:
            text: 'Done'
            on_press:
                if app.authenticate_user(): print("Login successful!")   
                else: app.create_user()
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



class Kiosk(App):

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(Account(name='Account'))
        sm.add_widget(Sign_In(name='sign_in'))
        sm.add_widget(Sign_Up(name='sign_up'))
        return sm
    
    def update_user(self, text, focus):
        global user
        if not focus:  # When the TextInput loses focus
            user = str(text)
            print(user)
            print("Variable updated:", user)

    def update_pass(self, text, focus):
        global passw
        if not focus:  # When the TextInput loses focus
            passw = str(text)
            print(passw)
            print("Variable updated:", passw)
    
    def create_user(e):
        with open('users.json', 'r+') as file:
            try:
                data = json.load(file)
            except json.decoder.JSONDecodeError:
                data = {}
            data[user] = passw
            file.seek(0)
            json.dump(data, file, indent=4)
        pass

    def authenticate_user(e):
        print(user)
        print(passw)
        with open('users.json', 'r') as file:
            data = json.load(file)
            return data.get(user) == passw
        pass



if __name__ == '__main__':
    Kiosk().run()