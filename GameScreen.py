from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.graphics import Color, Rectangle
from datetime import datetime, timedelta
import json
import os

LabelBase.register(name='Monospace', fn_regular='fonts/monospace.ttf')

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        layout = FloatLayout()

        background = Image(source='imagens/FundoC.png', allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
        layout.add_widget(background)

        self.pet_image = Image(source='imagens/normal.png', size_hint=(None, None), size=(200, 200), pos_hint={'center_x': 0.4, 'center_y': 0.45})
        layout.add_widget(self.pet_image)

        status_block = BoxLayout(orientation='vertical', size_hint=(1, None), height=200, pos_hint={'center_x': 0.5, 'y': 0})
        with status_block.canvas.before:
            Color(0.2, 0.6, 0.8, 1)
            self.status_block_rect = Rectangle(size=status_block.size, pos=status_block.pos)
            status_block.bind(size=self._update_status_block_rect, pos=self._update_status_block_rect)

        self.status_bars = {
            'Alimentacao saudavel': ProgressBar(max=100, value=50, size_hint=(0.7, None), height=20),
            'Energia': ProgressBar(max=100, value=50, size_hint=(0.7, None), height=20),
            'Forca': ProgressBar(max=100, value=50, size_hint=(0.7, None), height=20),
            'Felicidade': ProgressBar(max=100, value=50, size_hint=(0.7, None), height=20),
            'Resistencia': ProgressBar(max=100, value=50, size_hint=(0.7, None), height=20)
        }

        self.value_labels = {}

        for label_text, bar in self.status_bars.items():
            bar_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            label = Label(text=label_text, size_hint=(0.3, None), height=40, font_name='Monospace')
            value_label = Label(text=f"{int(bar.value)}%", size_hint=(0.2, None), height=40, font_name='Monospace')
            self.value_labels[bar] = value_label
            bar.bind(value=self.update_value_label)
            bar_layout.add_widget(label)
            bar_layout.add_widget(bar)
            bar_layout.add_widget(value_label)
            status_block.add_widget(bar_layout)

        layout.add_widget(status_block)

        camera_button = Button(background_normal='imagens/camera.png', size_hint=(None, None), size=(80, 80), pos_hint={'right': 1, 'top': 1})
        camera_button.bind(on_press=self.open_camera)
        layout.add_widget(camera_button)

        goals_button = Button(background_normal='imagens/metas.png', size_hint=(None, None), size=(80, 80), pos_hint={'x': 0, 'top': 1})
        goals_button.bind(on_press=self.open_goals_screen)
        layout.add_widget(goals_button)

        self.add_widget(layout)

        Clock.schedule_interval(self.decrease_status, 60)
        self.load_state()

        Clock.schedule_interval(self.save_state, 300)

    def _update_status_block_rect(self, instance, value):
        self.status_block_rect.size = instance.size
        self.status_block_rect.pos = instance.pos

    def update_value_label(self, instance, value):
        self.value_labels[instance].text = f"{int(value)}%"

    def open_camera(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'CameraScreen'

    def open_goals_screen(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'GoalsScreen'

    def decrease_status(self, dt):
        print("Decreasing status bars...")
        for bar in self.status_bars.values():
            initial_value = bar.value
            bar.value = max(0, bar.value - 5)
            print(f"{bar}: {initial_value} -> {bar.value}")

        self.save_state()

    def update_status(self, food_labels):
        food_effects = {
            'fruta': {'Alimentacao saudavel': 10, 'Energia': 10, 'Felicidade': 5, 'Resistencia': 5},
            'legume': {'Alimentacao saudavel': 15, 'Resistencia': 5},
            'carne': {'Alimentacao saudavel': 5, 'Forca': 10, 'Resistencia': 5, 'Felicidade': 5},
            'cereal': {'Alimentacao saudavel': 5, 'Energia': 15, 'Felicidade': 10},
            'leguminosa': {'Alimentacao saudavel': 5, 'Forca': 10, 'Resistencia': 5},
            'leite': {'Alimentacao saudavel': 10, 'Forca': 10, 'Felicidade': 5},
            'doce': {'Alimentacao saudavel': -5, 'Forca': -5, 'Resistencia': -5, 'Energia': 10, 'Felicidade': 10}
        }

        print("Updating status with food labels:", food_labels)
        updated_labels = set()
        for food in food_labels:
            if food in food_effects and food not in updated_labels:
                effects = food_effects[food]
                for status, change in effects.items():
                    self.status_bars[status].value = max(0, min(100, self.status_bars[status].value + change))
                    print(f"Updated {status} by {change} points")
                updated_labels.add(food)

        if 'fruta' in updated_labels:
            goals_screen = self.manager.get_screen('GoalsScreen')
            goals_screen.complete_goal("Comer uma fruta")(None, None)

        self.save_state()

    def get_exercise_progress(self):
        return self.exercise_distance

    def update_exercise_distance(self, distance):
        self.exercise_distance += distance
        goals_screen = self.manager.get_screen('GoalsScreen') if self.manager else None
        if goals_screen:
            goals_screen.update_exercise_goal(0)
        self.save_state()

    def update_bars_from_exercise(self):
        print("Atualizando status após exercício...")
        self.status_bars['Energia'].value = min(100, self.status_bars['Energia'].value + 20)
        self.status_bars['Felicidade'].value = min(100, self.status_bars['Felicidade'].value + 10)
        self.status_bars['Resistencia'].value = min(100, self.status_bars['Resistencia'].value + 15)
        self.status_bars['Forca'].value = min(100, self.status_bars['Forca'].value + 10)

    def update_pet_image(self, *args):
        avg_status = sum(bar.value for bar in self.status_bars.values()) / len(self.status_bars)
        if avg_status < 30:
            self.pet_image.source = 'imagens/triste.png'
        elif 30 <= avg_status <= 70:
            self.pet_image.source = 'imagens/normal.png'
        else:
            self.pet_image.source = 'imagens/feliz.png'

    def save_state(self, dt=None):
        state = {
            "status_bars": {key: bar.value for key, bar in self.status_bars.items()},
            "exercise_distance": self.exercise_distance,
            "last_save_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open("game_state.json", "w") as f:
            json.dump(state, f)

    def load_state(self):
        if os.path.exists("game_state.json"):
            with open("game_state.json", "r") as f:
                state = json.load(f)
                if "status_bars" in state:
                    for key, value in state["status_bars"].items():
                        self.status_bars[key].value = value
                self.exercise_distance = state.get("exercise_distance", 0)
