from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
global user
global passw

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
            text: 'Fishing Menu'
            on_press: root.manager.current = 'Fish_Stuff'
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

<Fish_Stuff>:
    BoxLayout:
        Button:
            text: 'Fish Stats'
            on_press: root.manager.current = 'Fish_Stats'
        Button:
            text: 'Upload Fish'
        
        Button:
            text: 'Leader Board'
        
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'

<Fish_Stats>:
    BoxLayout:
        

        Button:
            text: 'Back'
            on_press: root.manager.current = 'Fish_Stuff'
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

class Fish_Stuff(Screen):
    pass

class Fish_Stats(Screen):
    pass

#Main thing, if you change the name it will change the name of the window, just be sure to change it at the bottom too
class Kiosk(App):

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(Account(name='Account'))
        sm.add_widget(Sign_In(name='sign_in'))
        sm.add_widget(Sign_Up(name='sign_up'))
        sm.add_widget(Fish_Stuff(name='Fish_Stuff'))
        sm.add_widget(Fish_Stats(name='Fish_Stats'))
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
    


    def load_data(filename):
        """Loads data from a JSON file."""
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}  # Return an empty dictionary if the file doesn't exist

    def save_data(filename, data):
        """Saves data to a JSON file."""
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def create_user(e):
        """Creates a new user with the given username and password."""
        if not user or not passw:
            print("Cannot create a blank user.")
            return

        users = load_data('users.json')
        if user in users:
            print("Username already exists.")
        else:
            users[user] = passw
            save_data('users.json', users)
            print(f"User {user} created successfully.")

    def authenticate_user(e):
        """Authenticates a user based on the given username and password."""
        if not user or not passw:
            print("Please provide both username and password.")
            return False

        users = load_data('users.json')
        if user in users and users[user] == passw:
            print(f"User {user} authenticated successfully.")
            return True
        else:
            print("Invalid username or password.")
            return False

    def get_score(user):
        """Retrieves the score for a given user."""
        scores = load_data('scores.json')
        return scores.get(user, 0)  # Return 0 if the user doesn't exist

    def update_score(user, new_score):
        """Updates the score for a given user."""
        scores = load_data('scores.json')
        scores[user] = new_score
        save_data('scores.json', scores)

    def reset_score(user):
        """Resets the score for a given user."""
        scores = load_data('scores.json')
        if user in scores:
            del scores[user]
            save_data('scores.json', scores)

    def reset_all_scores():
        """Resets all stored scores."""
        save_data('scores.json', {})  # Save an empty dictionary to reset all scores

    '''# Example usage
    create_user("Alice", "password123")
    if authenticate_user("Alice", "password123"):
        update_score("Alice", 150)
        print(f"Alice's score: {get_score('Alice')}")
        reset_score("Alice")
        print(f"Alice's score after reset: {get_score('Alice')}")
'''

if __name__ == '__main__':
    Kiosk().run()