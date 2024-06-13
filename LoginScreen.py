import pyrebase
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.core.text import LabelBase

LabelBase.register(name='Monospace', fn_regular='fonts/monospace.ttf')

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

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.rect = Rectangle(size=Window.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)
        
        title_label = Label(text="Buddy Eat", font_size=60, color=(0, 0, 0, 1))
        title_label.font_name = 'Monospace'
        self.layout.add_widget(title_label)
        
        content_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        
        login_layout = BoxLayout(orientation='vertical', size_hint=(0.8, None), spacing=10, padding=20)
        
        user_icon = Image(source='imagens/icone.png', size_hint=(None, None), size=(80, 80))
        login_layout.add_widget(user_icon)
        
        self.email_label = Label(text="Email:", font_size=24, color=(0, 0, 0, 1))
        self.email_label.font_name = 'Monospace'
        login_layout.add_widget(self.email_label)
        self.email = TextInput(multiline=False, size_hint_y=None, height=40, font_size=20)
        login_layout.add_widget(self.email)
        
        self.password_label = Label(text="Senha:", font_size=24, color=(0, 0, 0, 1))
        self.password_label.font_name = 'Monospace'
        login_layout.add_widget(self.password_label)
        self.password = TextInput(multiline=False, size_hint_y=None, height=40, password=True, font_size=20)
        login_layout.add_widget(self.password)
        
        self.login_button = Button(text="Login", background_color=(0, 0.5, 1, 1), font_size=24, size_hint_y=None, height=50)
        self.login_button.bind(on_press=self.login)
        login_layout.add_widget(self.login_button)
        
        self.register_button = Button(text="Registrar", background_color=(0, 1, 0, 1), font_size=24, size_hint_y=None, height=50)
        self.register_button.bind(on_press=self.register)
        login_layout.add_widget(self.register_button)
        
        self.reset_password_button = Button(text="Recuperar Senha", background_color=(1, 0, 0, 1), font_size=24, size_hint_y=None, height=50)
        self.reset_password_button.bind(on_press=self.reset_password)
        login_layout.add_widget(self.reset_password_button)
        
        content_layout.add_widget(login_layout)
        self.layout.add_widget(content_layout)
        self.add_widget(self.layout)
    
    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos
    
    def login(self, instance):
        email = self.email.text
        password = self.password.text
        
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            print("Login bem-sucedido!")
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'GameScreen'
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
