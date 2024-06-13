from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.text import LabelBase
from kivy.graphics import Color, Rectangle
from datetime import datetime, timedelta
import json
import os

LabelBase.register(name='Monospace', fn_regular='fonts/monospace.ttf')

class GoalsScreen(Screen):
    def __init__(self, **kwargs):
        super(GoalsScreen, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0.8, 0.9, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        title_label = Label(text="Metas Diarias", font_size=40, font_name='Monospace', color=(0, 0, 0, 1), size_hint=(1, 0.2))
        self.layout.add_widget(title_label)

        self.goal_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        self.goals = {
            "Abrir o aplicativo": {"completed": False, "collected": False, "reward": {"Energia": 10, "Felicidade": 10}},
            "Comer uma fruta": {"completed": False, "collected": False, "reward": {"Alimentacao saudavel": 5, "Energia": 5, "Felicidade": 3, "Resistencia": 3}},
            "Andar 2km": {"completed": False, "collected": False, "progress": 0, "target": 2000, "reward": {"Forca": 10, "Resistencia": 10, "Energia": -10}}
        }

        self.goal_widgets = {}

        goal_box = BoxLayout(orientation='vertical', spacing=20, size_hint=(None, None), size=(400, 300))

        for goal, details in self.goals.items():
            goal_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
            
            label = Label(text=goal, font_name='Monospace', size_hint_x=0.7, color=(0, 0, 0, 1))
            goal_layout.add_widget(label)

            if goal == "Andar 2km":
                progress_bar = ProgressBar(max=details["target"], value=details["progress"], size_hint_x=0.3)
                goal_layout.add_widget(progress_bar)
                self.goal_widgets[goal] = progress_bar
            else:
                icon = Image(source='imagens/erro.png', size_hint_x=0.1)
                goal_layout.add_widget(icon)
                self.goal_widgets[goal] = icon

            collect_button = Button(text="Coletar", size_hint_x=0.3, disabled=True, font_name='Monospace')
            collect_button.bind(on_press=self.collect_goal(goal))
            goal_layout.add_widget(collect_button)
            self.goal_widgets[f"{goal}_button"] = collect_button

            goal_box.add_widget(goal_layout)

        self.goal_layout.add_widget(goal_box)
        self.layout.add_widget(self.goal_layout)

        back_button = Button(text="Voltar", size_hint=(None, None), size=(100, 50), pos_hint={'center_x': 0.5}, font_name='Monospace')
        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(back_button)
        
        self.add_widget(self.layout)

        Clock.schedule_once(lambda dt: self.complete_goal("Abrir o aplicativo")(None, None), 0)

        Clock.schedule_interval(self.update_exercise_goal, 1)

        self.load_state()
        self.reset_goals_daily()

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def complete_goal(self, goal):
        def callback(instance, touch):
            if not self.goals[goal]["completed"]:
                self.goals[goal]["completed"] = True
                self.goal_widgets[goal].source = 'imagens/ok.png'
                self.goal_widgets[f"{goal}_button"].disabled = False
            print(f"Goal {goal} completed")
        return callback

    def collect_goal(self, goal):
        def callback(instance):
            if self.goals[goal]["completed"] and not self.goals[goal]["collected"]:
                self.goals[goal]["collected"] = True
                self.goal_widgets[f"{goal}_button"].disabled = True
                self.apply_reward(goal)
                self.save_state()
                print(f"Goal {goal} collected")
        return callback

    def apply_reward(self, goal):
        if self.manager:
            rewards = self.goals[goal]["reward"]
            game_screen = self.manager.get_screen('GameScreen')
            for status, value in rewards.items():
                game_screen.status_bars[status].value = min(100, game_screen.status_bars[status].value + value)

    def update_exercise_goal(self, dt):
        if self.manager:
            game_screen = self.manager.get_screen('GameScreen')
            exercise_progress = game_screen.get_exercise_progress()
            self.goals["Andar 2km"]["progress"] = exercise_progress
            self.goal_widgets["Andar 2km"].value = exercise_progress

            if exercise_progress >= self.goals["Andar 2km"]["target"]:
                self.complete_goal("Andar 2km")(None, None)

    def reset_goals_daily(self):
        current_date = datetime.now().strftime("%Y-%m-%d")
        try:
            with open("goal_reset_date.json", "r") as f:
                last_reset_date = json.load(f)["date"]
        except (FileNotFoundError, ValueError):
            last_reset_date = ""

        if last_reset_date != current_date:
            for goal in self.goals.keys():
                self.goals[goal]["completed"] = False
                self.goals[goal]["collected"] = False
                if "progress" in self.goals[goal]:
                    self.goals[goal]["progress"] = 0
                self.goal_widgets[goal].source = 'imagens/erro.png'
                self.goal_widgets[f"{goal}_button"].disabled = True

            with open("goal_reset_date.json", "w") as f:
                json.dump({"date": current_date}, f)
            print("Goals have been reset for the new day.")

    def go_back(self, instance):
        if self.manager:
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'GameScreen'

    def save_state(self):
        state = {"goals": self.goals}
        with open("goals_state.json", "w") as f:
            json.dump(state, f)

    def load_state(self):
        if os.path.exists("goals_state.json"):
            with open("goals_state.json", "r") as f:
                state = json.load(f)
                self.goals.update(state["goals"])
                for goal, details in self.goals.items():
                    if details["completed"]:
                        self.goal_widgets[goal].source = 'imagens/ok.png'
                        self.goal_widgets[f"{goal}_button"].disabled = details["collected"]
                    else:
                        self.goal_widgets[goal].source = 'imagens/erro.png'
                        self.goal_widgets[f"{goal}_button"].disabled = True
                    if goal == "Andar 2km":
                        self.goal_widgets[goal].value = details["progress"]
