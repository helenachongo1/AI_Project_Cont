from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import sqlite3


conn = sqlite3.connect("HAC.db")
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS HAC (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')
conn.commit()

current_username = None

class LoginScreen(Screen):
    def init(self, **kwargs):
        super().init(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.username_input = TextInput(hint_text="Username", multiline=False, font_size='20sp')
        self.password_input = TextInput(hint_text="Password", multiline=False, password=True, font_size='20sp')

        login_button = Button(text="Login", background_color=(1, 0.4, 0.7, 1), font_size='20sp')
        login_button.bind(on_press=self.login_user)

        sign_up_button = Button(text="Sign Up", background_color=(1, 0.4, 0.7, 1), font_size='20sp')
        sign_up_button.bind(on_press=self.switch_to_signup)

        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_button)
        layout.add_widget(sign_up_button)

        self.add_widget(layout)

    def login_user(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if username == current_username:
            Popup(title='Error', content=Label(text='Username not available for login!'), size_hint=(0.6, 0.6)).open()
            return
        
        c.execute("SELECT * FROM HAC WHERE username=? AND password=?", (username, password))
        user = c.fetchone()

        if user:
            Popup(title='Success', content=Label(text='Login Successful!', font_size='20sp'), size_hint=(0.6, 0.6)).open()
        else:
            Popup(title='Error', content=Label(text='Invalid username or password!', font_size='20sp'), size_hint=(0.6, 0.6)).open()

    def switch_to_signup(self, instance):
        self.manager.current = "signup"

class SignUpScreen(Screen):
    def init(self, **kwargs):
        super().init(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.username_input = TextInput(hint_text="Username:", multiline=False, font_size='20sp')
        self.email_input = TextInput(hint_text="Email:", multiline=False, font_size='20sp')
        self.password_input = TextInput(hint_text="Password:", multiline=False, password=True, font_size='20sp')

        signup_button = Button(text="Sign Up", background_color=(1, 0.4, 0.7, 1), font_size='20sp')
        signup_button.bind(on_press=self.sign_up_user)

        back_button = Button(text="Back to Login", background_color=(1, 0.4, 0.7, 1), font_size='20sp')
        back_button.bind(on_press=self.switch_to_login)

        layout.add_widget(self.username_input)
        layout.add_widget(self.email_input)
        layout.add_widget(self.password_input)
        layout.add_widget(signup_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def sign_up_user(self, instance):
        global current_username 
        username = self.username_input.text
        email = self.email_input.text
        password = self.password_input.text

        try:
            c.execute("INSERT INTO HAC (username, email, password) VALUES (?, ?, ?)", (username, email, password))
            conn.commit()
            current_username = username  
            Popup(title='Success', content=Label(text='Sign Up Successful!', font_size='20sp'), size_hint=(0.6, 0.6)).open()
            self.manager.current = "login"
        except sqlite3.IntegrityError:
            Popup(title='Error', content=Label(text='Username already exists!', font_size='20sp'), size_hint=(0.6, 0.6)).open()

    def switch_to_login(self, instance):
        self.manager.current = "login"

class MyScreenManager(ScreenManager):
    def _init_(self, **kwargs):
        super(MyScreenManager, self)._init_(**kwargs)
        self.add_widget(LoginScreen(name="Login"))
        self.add_widget(SignUpScreen(name="Signup"))
    pass

class MyApp(App):
    def build(self):
        sm = MyScreenManager()
        return sm

# Run the Kivy App
if __name__ == '__main__':
    MyApp().run()