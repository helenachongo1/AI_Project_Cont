from kivy.app import App 
from kivy.uix.button import Button 
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager,Screen 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout

class SimpleApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.loginscreen()  
        return self.layout
    
    def loginscreen(self):
        self.layout.clear_widgets()
        self.username_label = Label(text="Username:")
        self.layout.add_widget(self.username_label)
        
        self.username_input = TextInput(hint_text='Enter your username', multiline=False)
        self.layout.add_widget(self.username_input)
        
       
        self.password_label = Label(text="Password:")
        self.layout.add_widget(self.password_label)
        
        self.password_input = TextInput(hint_text='Enter your password', password=True, multiline=False)
        self.layout.add_widget(self.password_input)
        
    
        self.login_button = Button(text="Login")
        self.login_button.bind(on_press=self.check_credentials)
        self.layout.add_widget(self.login_button)
        
        self.sign_button = Button(text="Go to Sign Up")
        self.sign_button.bind(on_press=self.Sign_UpApp)
        self.layout.add_widget(self.sign_button)
        
        self.status_label=Label(text="")
        self.layout.add_widget(self.status_label)
        
    def check_credentials(self,instance):
        username=self.username_input.text
        password=self.password_input.text
        
        
        if username=="admin" and password=="password":
            self.status_label.text="Login successful"
            self.status_label.color=(0,1,0,1)
        else:
            self.status_label.text="Invalid Credentials"
            self.status_label.color=(1,0,0,1)
            
    def Sign_UpApp(self):
        self.layout.clear_widgets()
        self.signup_username_label = Label(text="Username:")
        self.layout.add_widget(self.signup_username_label)
        
        self.signup_username_input = TextInput(hint_text='Enter your username', multiline=False)
        self.layout.add_widget(self.signup_username_input)
        
        
        self.email_label = Label(text="Email:")
        self.layout.add_widget(self.email_label)
        
        self.email_input = TextInput(hint_text='Enter your email', multiline=False)
        self.layout.add_widget(self.email_input)
        
     
        self.signup_password_label = Label(text="Password:")
        self.layout.add_widget(self.signup_password_label)
        
        self.signup_password_input = TextInput(hint_text='Enter your password', password=True, multiline=False)
        self.layout.add_widget(self.signup_password_input)
        
        
        self.sign_button=Button(text="Sign_Up")
        self.sign_button.bind(on_press=self.check_credentials_1)
        self.layout.add_widget(self.sign_button)
        
        self.login_button = Button(text="Go to login")
        self.login_button_button.bind(on_press=self.loginscreen)
        self.layout.add_widget(self.login_button)
        
        self.status_label=Label(text="")
        self.layout.add_widget(self.status_label)
        
    def check_credentials_1(self,instance):
        username=self.username_input.text
        password=self.password_input.text
        email=self.email_input.text
        
        
        if username and password and email:
            self.status_label.text="Signed up successful"
            self.status_label.color=(0,1,0,1)
        else:
            self.status_label.text="Invalid Credentials"
            self.status_label.color=(1,0,0,1)
            
           
if __name__=='__main__':
    SimpleApp().run()

