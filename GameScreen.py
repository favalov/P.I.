from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')
        
        #fundo
        "background = Image(source='fundo 2.jpg', allow_stretch=True, keep_ratio=False)"
        "layout.add_widget(background)"

        #dinossauro
        dinossauro_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        pet_image = Image(source='Dinossauro.png', size_hint=(None, None), size=(200, 200))
        dinossauro_layout.add_widget(pet_image)
        layout.add_widget(dinossauro_layout)

        #câmera
        camera_layout = AnchorLayout(anchor_x='center', anchor_y='bottom')
        camera_button = Button(background_normal='camera.png', background_down='camera.png', size_hint=(None, None), size=(100, 100))
        camera_layout.add_widget(camera_button)
        layout.add_widget(camera_layout)

        self.add_widget(layout)
