from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
user = str("")
passw = str("")
def create_user(username, password):
        with open('users.json', 'r+') as file:
            try:
                data = json.load(file)
            except json.decoder.JSONDecodeError:
                data = {}

            data[username] = password
            file.seek(0)
            json.dump(data, file, indent=4)
        pass

def authenticate_user(username, password):
    with open('users.json', 'r') as file:
        data = json.load(file)
        return data.get(username) == password
    pass

# Create a new user

create_user('test', 'pass')
'''
create_user('john', 'password123')

# Authenticate a user
if authenticate_user('john', 'password123'):
    print("Login successful!")
else:
    print("Invalid username or password.")
'''












# Create  screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
#:import auth main.authenticate_user
                    
                  
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
    
    f_username: username
    f_password: password
    GridLayout:

        rows: 2
        cols: 2
        padding: 10
        spacing: 10
        Label:  
            text: "Username"
        TextInput:
            id: username
            
        Label:
           
            text: "Password"
        TextInput:
            id: password
            password: True
        Button:
            text: 'Done'
            on_press:
                if auth(username, password):  print("Login successful!")   
                else: print("bad")
                    
                
        
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