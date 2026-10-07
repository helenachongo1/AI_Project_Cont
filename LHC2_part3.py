import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import hashlib

def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username, email, password):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, hash_password(password)))
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
    return True

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hash_password(password)))
    user = cursor.fetchone()
    conn.close()
    return user

def check_username_exists(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user is not None  


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.username_label = Label(text="Username:")
        layout.add_widget(self.username_label)
        self.username_input = TextInput(multiline=False)
        layout.add_widget(self.username_input)
        
        self.password_label = Label(text="Password:")
        layout.add_widget(self.password_label)
        self.password_input = TextInput(password=True, multiline=False)
        layout.add_widget(self.password_input)
        
        self.login_button = Button(text="Login")
        self.login_button.bind(on_press=self.check_credentials)
        layout.add_widget(self.login_button)
        
        self.status_label = Label(text="")
        layout.add_widget(self.status_label)
        
        self.add_widget(layout)

    def check_credentials(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        user = check_user(username, password)
        if user:
            self.status_label.text = "Login Successful"
            self.status_label.color = (0, 1, 0, 1)
        else:
            self.status_label.text = "Invalid Credentials"
            self.status_label.color = (1, 0, 0, 1)

class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super(SignUpScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text="Sign Up Screen"))

        self.username = TextInput(hint_text="Username", multiline=False)
        layout.add_widget(self.username)
        
        self.email = TextInput(hint_text="Email", multiline=False)
        layout.add_widget(self.email)
        
        self.password = TextInput(hint_text="Password", password=True, multiline=False)
        layout.add_widget(self.password)
        
        signup_button = Button(text="Sign Up")
        signup_button.bind(on_press=self.sign_up)
        layout.add_widget(signup_button)

        toggle_button = Button(text="Login")
        toggle_button.bind(on_press=self.go_to_login)
        layout.add_widget(toggle_button)

        self.status_label = Label(text="")
        layout.add_widget(self.status_label)
        
        self.add_widget(layout)

    def sign_up(self, instance):
        username = self.username.text
        email = self.email.text
        password = self.password.text

        if not username or not email or not password:
            self.status_label.text = "All fields are required"
            self.status_label.color = (1, 0, 0, 1)
        elif check_username_exists(username):
            self.status_label.text = "Username already exists"
            self.status_label.color = (1, 0, 0, 1)
        else:
            if add_user(username, email, password):
                self.status_label.text = "User signed up successfully!"
                self.status_label.color = (0, 1, 0, 1)
            else:
                self.status_label.text = "Sign-up failed"
                self.status_label.color = (1, 0, 0, 1)

    def go_to_login(self, instance):
        self.manager.current = 'login'

class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)
        self.add_widget(SignUpScreen(name='signup'))
        self.add_widget(LoginScreen(name='login'))

class MyApp(App):
    def build(self):
        create_database()
        sm = MyScreenManager()
        return sm

if __name__ == "__main__":
    MyApp().run()
