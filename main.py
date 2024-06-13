from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from LoginScreen import LoginScreen
from GameScreen import GameScreen
from CameraScreen import CameraScreen
from ExerciseScreen import ExerciseScreen
from GoalsScreen import GoalsScreen

class BuddyEatApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='LoginScreen'))
        sm.add_widget(GameScreen(name='GameScreen'))
        sm.add_widget(CameraScreen(name='CameraScreen'))
        sm.add_widget(ExerciseScreen(name='ExerciseScreen'))
        sm.add_widget(GoalsScreen(name='GoalsScreen'))
        return sm

if __name__ == "__main__":
    BuddyEatApp().run()
