import pyrebase
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.image import Image
from GameScreen import GameScreen

config = {
  "apiKey": "AIzaSyBu1roq0mP41BD-EZOzxkDhnxbKUGifnVI",
  "authDomain": "cadastro-c2f3a.firebaseapp.com",
  "databaseURL": "https://cadastro-c2f3a-default-rtdb.firebaseio.com/",
  "projectId": "cadastro-c2f3a",
  "storageBucket": "cadastro-c2f3a.appspot.com",
  "messagingSenderId": "708806537984",
  "appId": "1:708806537984:web:36bc0ef3f9af752f0779e5",
  "measurementId": "G-T1Z10LZPMT"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.add_widget(Image(source='dog.png'))  

class AppScreenManager(ScreenManager):
    pass

class LoginScreen(BoxLayout, Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = [50, 100]
        self.spacing = 20

        title_label = Label(text="Buddy Eat", font_size=60, color=(1, 1, 1, 1))
        self.add_widget(title_label)
        
        self.email_label = Label(text="Email:")
        self.add_widget(self.email_label)
        self.email = TextInput(multiline=False, size_hint_y=None, height=30)
        self.add_widget(self.email)
        
        self.password_label = Label(text="Senha:")
        self.add_widget(self.password_label)
        self.password = TextInput(multiline=False, size_hint_y=None, height=30, password=True)
        self.add_widget(self.password)

        self.login_button = Button(text="Login", background_color=(0, 1, 0, 1))
        self.login_button.bind(on_press=self.login)
        self.add_widget(self.login_button)

        self.register_button = Button(text="Registrar", background_color=(1, 0, 0, 1))
        self.register_button.bind(on_press=self.register)
        self.add_widget(self.register_button)

        self.reset_password_button = Button(text="Recuperar Senha", background_color=(0, 0, 1, 1))
        self.reset_password_button.bind(on_press=self.reset_password)
        self.add_widget(self.reset_password_button)
    
    def login(self, instance):
        email = self.email.text
        password = self.password.text

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            print("Login bem-sucedido!")
            self.parent.transition = SlideTransition(direction='left')
            self.parent.current = 'GameScreen'
        except Exception as e:
            print("Erro durante o login:", e)

    def register(self, instance):
        email = self.email.text
        password = self.password.text

        try:
            user = auth.create_user_with_email_and_password(email, password)
            print("Usuário registrado com sucesso!")
        except Exception as e:
            print("Erro durante o registro:", e)

    def reset_password(self, instance):
        email = self.email.text

        try:
            auth.send_password_reset_email(email)
            print("Email de recuperação de senha enviado com sucesso!")
        except Exception as e:
            print("Erro ao enviar email de recuperação de senha:", e)


class BuddyEatApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='LoginScreen'))
        sm.add_widget(GameScreen(name='GameScreen'))
        return sm


if __name__ == "__main__":
    BuddyEatApp().run()
