from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.graphics import Color, Rectangle
from google.cloud import vision
from google.oauth2 import service_account
import io

LabelBase.register(name='Monospace', fn_regular='fonts/monospace.ttf')

class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0.9, 0.9, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical')

        title_label = Label(text="Tire uma Foto", font_size=40, font_name='Monospace', color=(0, 0, 0, 1), size_hint=(1, 0.1))
        layout.add_widget(title_label)

        self.camera = Camera(play=True, resolution=(640, 480), size_hint=(1, 0.8))
        layout.add_widget(self.camera)

        button_layout = BoxLayout(size_hint=(1, 0.1), padding=(10, 10), spacing=10)

        capture_button = Button(text="Capturar Imagem", size_hint=(0.5, 1), font_name='Monospace', font_size=20)
        capture_button.bind(on_press=self.capture_image)
        button_layout.add_widget(capture_button)

        back_button = Button(text="Voltar", size_hint=(0.5, 1), background_color=(0.7, 0.7, 0.7, 1), color=(1, 1, 1, 1), font_name='Monospace', font_size=20)
        button_layout.add_widget(back_button)
        back_button.bind(on_press=self.go_back)

        layout.add_widget(button_layout)
        self.add_widget(layout)

        self.analysis_result = Label(text="", size_hint=(1, 0.1))
        layout.add_widget(self.analysis_result)

        self.client = vision.ImageAnnotatorClient(
            credentials=service_account.Credentials.from_service_account_file('projetointegrador-423913-9f6262a7f97b.json')
        )

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def capture_image(self, instance):
        self.camera.export_to_png("captured_image.png")
        self.identify_food()

    def identify_food(self):
        with io.open("captured_image.png", "rb") as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = self.client.label_detection(image=image)
        labels = response.label_annotations
        
        food_keywords = {
            'fruta': ['fruit', 'apple', 'banana', 'orange', 'berry', 'grape'],
            'legume': ['vegetable', 'carrot', 'broccoli', 'lettuce'],
            'carne': ['meat', 'beef', 'chicken', 'pork', 'steak'],
            'cereal': ['grain', 'bread', 'rice', 'pasta', 'oat'],
            'leguminosa': ['legume', 'bean', 'lentil', 'chickpea'],
            'leite': ['dairy', 'milk', 'cheese', 'yogurt'],
            'doce': ['sweets', 'snacks', 'candy', 'chocolate']
        }

        food_labels = []
        for label in labels:
            for group, keywords in food_keywords.items():
                if any(keyword in label.description.lower() for keyword in keywords):
                    food_labels.append(group)
                    break

        print('Food labels identified:', food_labels)
        if food_labels:
            game_screen = self.manager.get_screen('GameScreen')
            game_screen.update_status(food_labels)
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'GameScreen'
        else:
            self.analysis_result.text = "Nenhum alimento identificado."

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'GameScreen'
