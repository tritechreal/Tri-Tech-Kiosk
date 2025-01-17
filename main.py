from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
user = None
passw = None


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

def sync_users_and_scores():  #Ensures that all users have an entry in the scores file, setting the score to 0 if they are not already present.
    try:
        users = load_data('users.json')
        scores = load_data('scores.json')
       #print("Users:", users)  # Debug: Print loaded users
       #print("Scores:", scores)  # Debug: Print loaded scores
        for user in users:
            if user not in scores: #if the user is not present, add them
                scores[user] = 0
                print(f"Added user {user} to scores with score 0.")
        save_data('scores.json', scores)
        print("Users and scores synchronized.")
    except Exception as e:
        print(f"An error occurred during synchronization: {e}")
sync_users_and_scores() #keeps new accounts on the scores list to keep original account system



#region kv code for ui 
Builder.load_string("""
                
<MenuScreen>:
    BoxLayout:
        Button:
            text: 'Settings'
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
            text: 'Debug'
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
            text: 'My Stats'
            on_press: root.manager.current = 'My_Stats'
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
            on_text: app.update_user(self.text)
        Label:
            text: "Password"
        TextInput:
            id: password
            password: True
            on_text: app.update_pass(self.text)
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
            on_text: app.update_user(self.text)
 
        Label:
           
            text: "Password"
        TextInput:
            id: password
            password: True
            on_text: app.update_pass(self.text)
        Button:
            text: 'Done'
            on_press:
                if app.authenticate_user(): print("Login successful!")   
                else: app.create_user()
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'
<My_Stats>:
    GridLayout:
        rows: 3
        cols: 2
        padding: 10
        spacing: 10
        Label:  
            text: "My Stats"
        
        Label:
            id: your_score
            text: str(app.get_score())
        
        Button:
            text: 'Refresh Stats'
            on_press:
                your_score.text = str(app.get_score())
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
#endregion
# Declare all screens... and yes you need it
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

class My_Stats(Screen):
    pass

class Fish_Stuff(Screen):
    pass

class Fish_Stats(Screen):
    pass

#Main thing, if you change the name it will change the name of the window, just be sure to change it at the bottom too
class Kiosk(App):

    def build(self):
        # Create the screen manager and sets up everything for navigation
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(Account(name='Account'))
        sm.add_widget(Sign_In(name='sign_in'))
        sm.add_widget(Sign_Up(name='sign_up'))
        sm.add_widget(My_Stats(name='My_Stats'))
        sm.add_widget(Fish_Stuff(name='Fish_Stuff'))
        sm.add_widget(Fish_Stats(name='Fish_Stats'))
        return sm
    
    def update_user(self, text): #for sign in and creaiting account
        global user
        user = str(text)
        print("Variable updated:", user) #can comment these out, primarily for debug

    def update_pass(self, text): #for sign in and creaiting account
        global passw
        passw = str(text)
        print("Variable updated:", passw) #can comment these out, primarily for debug

    def create_user(e): #creates new user
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
    def authenticate_user(e): #Login existing user
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
    def get_score(e):
        """Retrieves the score for a given user."""
        scores = load_data('scores.json')
        print(scores.get(user, 0))
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

    def find_highest_score(e):
        score_list = list() #preps to convert the json of scores to a list for sorting
        users = load_data('users.json')
        scores = load_data('scores.json')
        for user in users:
            score_list.append(scores[user])
            print(f"Added user {user} with score of {scores[user]}")
        score_list.sort() #this line sorts the list
        for user in users: #for each user in the user list (repeats for duration  of the user list)
            if scores[user] == score_list[-1]: #if the score matches the last item on the sorted list (highest)
                return user, score_list[-1]
               #print([user, score_list[-1]])  here for debug
                break
            else:
                print("trying again") #fail safe if there is some error with the first result
        


if __name__ == '__main__': #main python code goes here
    kiosk_app = Kiosk()
    print(kiosk_app.find_highest_score()) #this is here for testing
    kiosk_app.run()