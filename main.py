from kivy.logger import Logger, LOG_LEVELS
Logger.setLevel(LOG_LEVELS["info"])
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
user = None
passw = None
from kivy.core.window import Window
from kivy.config import Config
import time
import threading
import os

os.environ['SDL_MOUSE_TOUCH_EVENTS'] = '1'
os.environ['KIVY_WINDOW'] = 'x11'
print(time.localtime())

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
#:import Factory kivy.factory.Factory
                
<MenuScreen>:
    BoxLayout:
        
        Button:
            text: 'Settings  ' + '⚙️'
            font_name: 'seguiemj'
            font_size: 40
            on_press: root.manager.current = 'settings'
        Button:
            text: 'Account  ' + '👤'
            font_name: 'seguiemj'
            font_size: 40
            on_press: root.manager.current = 'Account'
        Button:
            text: 'Fishing ' + '🐟🎣'
            font_name: 'seguiemj'
            font_size: 40
            on_press: root.manager.current = 'Fish_Stuff'
        Button:
            text: 'Quit ' + '❌'
            font_name: 'seguiemj'
            font_size: 40
            on_press: raise Exception("User quit program")
<MyPopup@Popup>:
    auto_dismiss: False
    on_dismiss: print("Popup dismissed")
    title: 'You are now signed in!'         
    Button:
        text: 'You have been signed in! ✅' + '   (Click popup to continue)'
        font_name: 'seguiemj'
        font_size: 60
        on_release: root.dismiss()
    
<SettingsScreen>:
    BoxLayout:
        Button:
            text: 'Debug' + '🛠️'
            font_name: 'seguiemj'
            font_size: 40
            on_press: root.manager.current = 'admin'
        Button:
            text: 'My settings button'
        Button:
            text: 'Back  ' + '↩️'
            font_name: 'seguiemj'
            font_size: 40
            on_press: root.manager.current = 'menu'
<Account>:
    BoxLayout:
        Button:
            text: 'Sign In ' + '👤'
            font_name: 'seguiemj'
            font_size: 40
            on_press: root.manager.current = 'sign_in'
        Button:
            text: 'Sign Up' + '➕👤'
            font_name: 'seguiemj'
            font_size: 40
            on_press: root.manager.current = 'sign_up'
        Button:
            text: 'My Stats ' + '👤📈'
            font_name: 'seguiemj'
            font_size: 40
            on_press: root.manager.current = 'My_Stats'
        Button:
            text: 'Back  ' + '↩️'
            font_name: 'seguiemj'
            font_size: 40
         
            on_press: root.manager.current = 'menu'
                    
<Sign_In>:
    GridLayout:

        rows: 3
        cols: 2
        padding: 10
        spacing: 10
        Label:  
            text: "Username 👤"
            font_name: 'seguiemj'
            font_size: 40
        TextInput:
            id: username
            use_bubble: True 
            on_text: app.update_user(self.text)
            font_name: 'seguiemj'
            font_size: 40
        Label:
            text: "Password 🔑"
            font_name: 'seguiemj'
            font_size: 40
        TextInput:
            id: password
            password: True
            on_text: app.update_pass(self.text)
            font_name: 'seguiemj'
            font_size: 40
        Button:
            text: 'Done ' + '✅'
            font_name: 'seguiemj'
            font_size: 40
            on_press:
                if app.authenticate_user(): Factory.MyPopup().open()
                   
            
                else: print("error, no account found")
        Button:
            text: 'Back  ' + '↩️'
            font_name: 'seguiemj'
            font_size: 40
         
            on_press: root.manager.current = 'menu'
                           
<Sign_Up>:
    GridLayout:

        rows: 3
        cols: 2
        padding: 10
        spacing: 10
        Label:  
            text: "Username 👤"
            font_name: 'seguiemj'
            font_size: 40
        TextInput:
            id: username
            on_text: app.update_user(self.text)
            font_name: 'seguiemj'
            font_size: 40
 
        Label:
           
            text: "Password 🔑"
            font_name: 'seguiemj'
            font_size: 40
        TextInput:
            id: password
            password: True
            on_text: app.update_pass(self.text)
            font_name: 'seguiemj'
            font_size: 40
        Button:
            text: 'Done' + '✅'
            font_name: 'seguiemj'
            font_size: 40
            on_press:
                if app.authenticate_user(): Factory.MyPopup().open()   
                else: app.create_user()
                app.authenticate_user()
                Factory.MyPopup().open()
        Button:
            text: 'Back  ' + '↩️'
            font_name: 'seguiemj'
            font_size: 40
         
            on_press: root.manager.current = 'menu'
<My_Stats>:
    GridLayout:
        rows: 3
        cols: 2
        padding: 10
        spacing: 10
        Label:  
            text: "My Score 📈"
            font_name: 'seguiemj'
            font_size: 80
        
        Label:
            id: your_score
            
            font_name: 'seguiemj'
            font_size: 80
        
        Button:
            text: 'Refresh Stats  ' + '🔃'
            font_name: 'seguiemj'
            font_size: 60
            on_press:
                your_score.text = str(app.get_score())
        Button:
            text: 'Back  ' + '↩️'
            font_name: 'seguiemj'
            font_size: 60
         
            on_press: root.manager.current = 'menu'

<Fish_Stuff>:
    BoxLayout:
        Button:
            text: 'Fish Stats  ' + '📊'
            font_name: 'seguiemj'
            font_size: 40
            on_press: root.manager.current = 'Fish_Stats'
        Button:
            text: 'Upload Fish (Coming Soon)' + '🐟📸'
            font_name: 'seguiemj'
            font_size: 40
        
        Button:
            text: 'Leader Board  ' + '🥇🥈🥉'
            font_name: 'seguiemj'
            font_size: 40
            on_press: root.manager.current = 'Leader_Board'
        
        Button:
            text: 'Back  ' + '↩️'
            font_name: 'seguiemj'
            font_size: 40
         
            on_press: root.manager.current = 'menu'
<Leader_Board>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Leaderboard ' + '🏆'
            font_name: 'seguiemj'
            font_size: 80
        
        Label:
            size_hint_y: None
            size_hint_x: 0.6
            text_size: self.width, None
            height: self.texture_size[1]
            id: highest_score
            font_name: 'seguiemj'
            font_size: 80
        Button:
            text: 'Refresh  ' + '🔃'
            font_name: 'seguiemj'
            font_size: 80
            size_hint_y: None
            size_hint_x: 0.5
            text_size: self.width, None
            height: self.texture_size[1]
            on_press: highest_score.text = str(app.leaderboard())
        Button:
            text: 'Back  ' + '↩️'
            font_name: 'seguiemj'

            font_size: 80
            size_hint_y: None
            size_hint_x: 0.5
            text_size: self.width, None
            height: self.texture_size[1]
            on_press: root.manager.current = 'menu'
<Fish_Stats>:
    BoxLayout:
        Button:
            text: 'Leader Board  ' + '🥇🥈🥉'
            font_name: 'seguiemj'
            font_size: 40
            on_press: root.manager.current = 'Leader_Board'
        Button:
            text: 'Daily Catches ' + '📅🐟'
            font_name: 'seguiemj'
            font_size: 40
            on_press: root.manager.current = 'Daily_Catches'
        Button:
            text: 'Back  ' + '↩️'
            font_name: 'seguiemj'
            font_size: 40
         
            on_press: root.manager.current = 'menu'
<Daily_Catches>:
    BoxLayout:
        Label:
            id: daily_catches
            font_name: 'seguiemj'
            font_size: 40
        Button:
            text: 'Refresh  ' + '🔃'
            font_name: 'seguiemj'
            font_size: 40
            on_press: daily_catches.text = str(app.daily_stats())
        Button:
            text: 'Back  ' + '↩️'
            font_name: 'seguiemj'
            font_size: 40
            on_press: root.manager.current = 'Fish_Stats'                    
<admin>:
    BoxLayout:
        Button:
            text: 'Reset  ' + '🔃'
            font_name: 'seguiemj'
            font_size: 40
            on_press: root.manager.current = 'reset'
        Button:
            text: 'computer vision initialize' + '🤖'
            font_name: 'seguiemj'           
            font_size: 40
            on_press: app.computer_vision()
        Button:
            text: 'List Users  ' + '👤'
            font_name: 'seguiemj'
            font_size: 40
            on_press: app.leaderboard()
        Button:
            text: 'Back  ' + '↩️'
            font_name: 'seguiemj'
            font_size: 40
         
            on_press: root.manager.current = 'menu'
<reset>:
    BoxLayout:
        Button:
            text: 'Reset Score' + '♻️'
            font_name: 'seguiemj'
            font_size: 40
            on_press: app.reset_score(user)
        Button:
            text: 'Reset All Scores' + '♻️'
            font_name: 'seguiemj'
            font_size: 40
            on_press: app.reset_all_scores()
        Button:
            text: 'Back  ' + '↩️'
            font_name: 'seguiemj'
            font_size: 40
         
            on_press: root.manager.current = 'admin'
      
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
    def on_focus(self, instance, value):
        if value: 
            keyboard = Window.request_keyboard(self._keyboard_closed, self)
    pass

class Sign_Up(Screen):
    pass

class My_Stats(Screen):
    pass

class Fish_Stuff(Screen):
    pass

class Fish_Stats(Screen):
    pass

class Leader_Board(Screen):
    pass
class admin(Screen):
    pass
class reset(Screen):
    pass
class Daily_Catches(Screen):
    pass
#Main thing, if you change the name it will change the name of the window, just be sure to change it at the bottom too
#region main code
class FishFlex(App):

    def build(self):
        # Configure graphics settings
        Config.set('kivy', 'input_provider', 'sdl2')
        Config.set('graphics', 'fullscreen', 1)
        Config.set('graphics', 'resizable', 0)
        Config.set('graphics', 'borderless', 1)  # Example: Set borderless to 1
      

        
        # Configure input settings
        Config.set('input', 'mouse', 'multitouch_sim')  # Combine with mouse provider
        #Config.set('kivy', 'input_provider', 'sdl2')  # Example: Set input provider
        Config.set('input', 'keyboard_mode', 'dock')
        # Apply the configuration
        Config.write()
        
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(Account(name='Account'))
        sm.add_widget(Sign_In(name='sign_in'))
        sm.add_widget(Sign_Up(name='sign_up'))
        sm.add_widget(My_Stats(name='My_Stats'))
        sm.add_widget(Fish_Stuff(name='Fish_Stuff'))
        sm.add_widget(Fish_Stats(name='Fish_Stats'))
        sm.add_widget(Leader_Board(name='Leader_Board'))
        sm.add_widget(admin(name='admin'))
        sm.add_widget(reset(name='reset'))
        sm.add_widget(Daily_Catches(name='Daily_Catches'))
         # Set the initial screen to 'menu'
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

    def reset_all_scores(e):
        """Resets all stored scores."""
        save_data('scores.json', {})  # Save an empty dictionary to reset all scores
        sync_users_and_scores() #resets the scores and ensures that all users have an entry in the scores file, setting the score to 0 if they are not already present.

    def find_highest_score(e):
        score_list = list() #preps to convert the json of scores to a list for sorting
        users = load_data('users.json')
        scores = load_data('scores.json')
        for user1 in users:
            score_list.append(scores[user1])
            print(f"Added user {user1} with score of {scores[user1]}")
        score_list.sort() #this line sorts the list
        for user1 in users: #for each user in the user list (repeats for duration  of the user list)
            if scores[user1] == score_list[-1]: #if the score matches the last item on the sorted list (highest)
                return user1, score_list[-1]
               #print([user, score_list[-1]])  here for debug
                break
            else:
                print("trying again") #fail safe if there is some error with the first result
        


    def leaderboard(e):
        score_list = list() #preps to convert the json of scores to a list for sorting
        users = load_data('users.json')
        scores = load_data('scores.json')
        output = list()
        for user in users:
            score_list.append(scores[user])
            print(f"Added user {user} with score of {scores[user]}")
        score_list.sort() #this line sorts the list
        sorted_users = sorted(users.keys(), key=lambda x: scores[x], reverse=True)
        for user in sorted_users:
            print(f"{user}: {scores[user]}")
        for i in range(0,3):
            print(f"{i+1}: {sorted_users[i]} with a score of {scores[sorted_users[i]]}")
            output.append(f"{i+1}: {sorted_users[i]} with a score of {scores[sorted_users[i]]}")
            print(output)
        return output
    
    
    
    
    
    def log_data(fish_type, length):
        """Logs data for a given fish type and length."""
        data = load_data('fish_data.json')
        if fish_type not in data:
            data[fish_type] = []
        data[fish_type].extend([[length, user, time.time()]])
        save_data('fish_data.json', data)
    
    def register_catch(e):
        """Registers a catch for the given user."""
        scores = load_data('scores.json')
        if user in scores:
            scores[user] += 1
        else:
            scores[user] = 1
        save_data('scores.json', scores)
        
    def daily_stats(e):
        """Calculates daily statistics for all users."""
        data = load_data('fish_data.json')
        daily_stats = {}
        for fish_type, catches in data.items():
            for catch in catches:
                current_time = catch[2]  # Get timestamp from catch data
                today = time.strftime("%Y-%m-%d")  # Get today's date
                catch_date = time.strftime("%Y-%m-%d", time.localtime(current_time))
                
                if catch_date == today:  # Only process catches from today
                    if catch_date not in daily_stats:
                        daily_stats[catch_date] = {}
                    if fish_type not in daily_stats[catch_date]:
                        daily_stats[catch_date][fish_type] = 0
                    daily_stats[catch_date][fish_type] += 1
        return daily_stats
    def camera_proc():
        from kivy.logger import Logger, LOG_LEVELS
        Logger.setLevel(LOG_LEVELS["info"])
        import camera as cam
        
        print(cam.find_box())

    cam_thread = threading.Thread(target=camera_proc)
    cam_thread.daemon = True

    def computer_vision(e):
        """Handles the computer vision aspect of the application."""
        # Placeholder for computer vision code
        FishFlex.cam_thread.start()
        
        #print("with a width of", cam.find_box()[1])
        FishFlex.log_data("fish", 10)  # Example: Log a fish catch with length 10
        FishFlex.register_catch(None)  # Example: Register a catch for the user
        pass

    
#endregion

print(FishFlex.daily_stats("e"))
if __name__ == '__main__': #main python code goes here
    kiosk_app = FishFlex() #easteregg
    kiosk_app.run()
    