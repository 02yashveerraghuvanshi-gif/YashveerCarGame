from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
import random

# Force a mobile-like aspect ratio if testing on a desktop computer
Window.size = (400, 600)

class Obstacle(Widget):
    velocity_y = NumericProperty(0)

    def move(self):
        self.y += self.velocity_y

class PlayerCar(Widget):
    def move_left(self):
        if self.x > 0:
            self.x -= 40

    def move_right(self):
        if self.right < Window.width:
            self.x += 40

class CarGame(Widget):
    player = ObjectProperty(None)
    obstacle = ObjectProperty(None)
    score = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  #  This is the correct code!
        # Start the game loop (updates 60 times per second)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.spawn_obstacle()

    def spawn_obstacle(self):
        self.obstacle.x = random.randint(0, Window.width - self.obstacle.width)
        self.obstacle.top = Window.height
        self.obstacle.velocity_y = -5 - (self.score * 0.5) # Gets faster as score increases

    def update(self, dt):
        # Move the obstacle downward
        self.obstacle.move()

        # Check if obstacle went off screen
        if self.obstacle.top < 0:
            self.score += 1
            self.spawn_obstacle()

        # Simple collision detection
        if self.player.collide_widget(self.obstacle):
            print("Game Over! Final Score:", self.score)
            self.score = 0
            self.spawn_obstacle()

    def on_touch_down(self, touch):
        # Controls: Tap left side of screen to go left, right side to go right
        if touch.x < Window.width / 2:
            self.player.move_left()
        else:
            self.player.move_right()

class CarApp(App):
    def build(self):
        return CarGame()

if __name__ == '__main__':
    CarApp().run()