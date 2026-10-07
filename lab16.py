
from kivy.app import App 
from kivy.uix.button import Button 
from kivy.uix.label import Label 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout


'''class SimpleApp(App):
    def build(self):
        layout=BoxLayout(orientation='vertical')
        
        self.label=Label(text="Hello, ICT Department")
        layout.add_widget(self.label)
        
        button=Button(text="Click Me!")
        button.bind(on_press=self.on_button_press)
        layout.add_widget(button)
        
        return layout
    def on_button_press(self,instance):
        self.label.text="Button Clicked"
        

if __name__=='__main__':
    SimpleApp().run()'''
    
'''class LoginApp(App):
    def build(self):
        layout=BoxLayout(orientation='vertical',padding=10,spacing=10)
        
        self.username_label=Label(text="Username:")
        layout.add_widget(self.username_label)
        
        self.username_input = TextInput(multiline=False)
        layout.add_widget(self.username_input)
        
        self.password_label=Label(text="Password:")
        layout.add_widget(self.password_label)
        
        self.password_input=TextInput(password=True,multiline=False)
        layout.add_widget(self.password_input)
        
        self.login_button=Button(text="Login")
        self.login_button.bind(on_press=self.check_credentials)
        layout.add_widget(self.login_button)
        
        self.status_label=Label(text="")
        layout.add_widget(self.status_label)
        
        return layout
    
    def check_credentials(self,instance):
        username=self.username_input.text
        password=self.password_input.text
        
        
        if username=="admin" and password=="password":
            self.status_label.text="Login successful"
            self.status_label.color=(0,1,0,1)
        else:
            self.status_label.text="Invalid Credentials"
            self.status_label.color=(1,0,0,1)
            
            
if __name__=='__main__':
    LoginApp().run()'''
    
#Q1
'''class incremCount(App):
    count=0
    def build(self):
        layout=BoxLayout(orientation='vertical')
        
        self.label=Label(text="0")
        layout.add_widget(self.label)
        
        button=Button(text="Click!")
        button.bind(on_press=self.on_button_press)
        layout.add_widget(button)
        return layout
    
    def on_button_press(self,instance):
         self.count+=1
         self.label.text=str(self.count)
         
if __name__=='__main__':
    incremCount().run()'''
    
#Q2
class User_details(App):
    def build(self):
        layout=BoxLayout(orientation='vertical',padding=10, spacing=10)
        
        self.username_label=Label(text="Username:")
        layout.add_widget(self.username_label)
        
        self.username_input=TextInput(multiline=False)
        layout.add_widget(self.username_input)
        
        self.occupation_label=Label(text="Occupation:")
        layout.add_widget(self.occupation_label)
        
        self.occupation_input=TextInput(multiline=False)
        layout.add_widget(self.occupation_input)
        
        self.age_label=Label(text="Age:")
        layout.add_widget(self.age_label)
        
        self.age_input=TextInput(multiline=False)
        layout.add_widget(self.age_input)
        
        self.btn=Button(text="Click!")
        self.btn.bind(on_press=self.check_details)
        layout.add_widget(self.btn)
        
        self.status_label=Label(text="")
        layout.add_widget(self.status_label)
        
        self.status1_label=Label(text="")
        layout.add_widget(self.status1_label)
        
        self.status2_label=Label(text="")
        layout.add_widget(self.status2_label)
        
        return layout 
    def check_details(self,instance):
        u_name=self.username_input.text
        occupation=self.occupation_input.text
        age=self.age_input.text
        
        self.status_label.text="Name:" + u_name
        self.status1_label.text="Occupation:" + occupation
        self.status2_label.text="Age:" + age
        
if __name__=='__main__':
    User_details().run()
    
'''import kivy
from kivy.app import App
from kivy.uix.button import Button, Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty


class Example(BoxLayout):
    n = 0

    def n_plus(self):
        self.n += 1


class ExampleApp(App):

    def build(self):
        return Example()

example = ExampleApp()
example.run()'''
        


'''# Defining the calculator layout and logic
class CalculatorGrid(GridLayout):
    def __init__(self, **kwargs):
        super(CalculatorGrid, self).__init__(**kwargs)
        self.cols = 4  # Grid layout with 4 columns

        # TextInput field to display the calculation results
        self.result = TextInput(font_size=32, readonly=True, halign="right", multiline=False)
        self.add_widget(self.result)

        # Buttons for numbers and operations
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '.', '0', '=', '+'
        ]

        # Adding buttons to the layout
        for button in buttons:
            self.add_widget(Button(text=button, font_size=24, on_press=self.on_button_press))

        # Clear button to reset the calculator
        self.add_widget(Button(text="C", font_size=24, on_press=self.clear_result))

    # Function to handle button press events
    def on_button_press(self, instance):
        current_text = self.result.text
        button_text = instance.text

        # If the equals sign is pressed, evaluate the expression
        if button_text == "=":
            try:
                self.result.text = str(eval(current_text))
            except Exception:
                self.result.text = "Error"
        else:
            # Otherwise, append the pressed button's text to the current expression
            if current_text == "Error":
                self.result.text = button_text  # Reset the result if there's an error
            else:
                self.result.text += button_text

    # Function to clear the result field
    def clear_result(self, instance):
        self.result.text = ""

# Main App class
class CalculatorApp(App):
    def build(self):
        return CalculatorGrid()

# Running the application
if __name__ == '__main__':
    CalculatorApp().run()'''

