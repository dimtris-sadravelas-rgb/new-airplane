from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Triangle, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
import random


class Bullet:
    def __init__(self, canvas, x, y):
        self.w = Window.width * 0.015
        self.h = Window.height * 0.035
        self.x = x - self.w / 2
        self.y = y
        self.speed = Window.height * 0.018

        with canvas:
            Color(1, 0, 0, 1)
            self.shape = Rectangle(pos=(self.x, self.y), size=(self.w, self.h))

    def move(self):
        self.y += self.speed
        self.shape.pos = (self.x, self.y)

    def off_screen(self):
        return self.y > Window.height


class Obstacle:
    def __init__(self, canvas):
        self.size = Window.width * 0.09
        self.x = random.randint(0, int(Window.width - self.size))
        self.y = Window.height + self.size
        self.speed = Window.height * 0.006

        r, g, b = random.random(), random.random(), random.random()

        with canvas:
            Color(r, g, b, 1)
            self.shape = Rectangle(pos=(self.x, self.y), size=(self.size, self.size))

    def move(self):
        self.y -= self.speed
        self.shape.pos = (self.x, self.y)

    def off_screen(self):
        return self.y + self.size < 0


class AirplaneGame(Widget):
    def __init__(self, score_label, high_score_label, **kwargs):
        super().__init__(**kwargs)

        self.score_label = score_label
        self.high_score_label = high_score_label

        self.score = 0
        self.high_score = 0
        self.game_running = True
        self.paused = False

        self.bullets = []
        self.obstacles = []

        self.player_size = Window.width * 0.12
        self.player_x = Window.width / 2
        self.player_y = Window.height * 0.12

        with self.canvas:
            Color(0, 0, 0, 1)
            self.background = Rectangle(pos=(0, 0), size=Window.size)

            Color(0, 1, 1, 1)
            self.player = Triangle(points=self.get_player_points())

        Clock.schedule_interval(self.update, 1 / 60)
        Clock.schedule_interval(self.spawn_obstacle, 0.9)
        Clock.schedule_interval(self.auto_shoot, 0.35)

    def get_player_points(self):
        return [
            self.player_x, self.player_y + self.player_size,
            self.player_x - self.player_size / 2, self.player_y,
            self.player_x + self.player_size / 2, self.player_y
        ]

    def on_touch_down(self, touch):
        self.move_player_to_touch(touch)
        return True

    def on_touch_move(self, touch):
        self.move_player_to_touch(touch)
        return True

    def move_player_to_touch(self, touch):
        if not self.game_running or self.paused:
            return

        margin = self.player_size / 2

        self.player_x = max(margin, min(touch.x, Window.width - margin))
        self.player_y = max(0, min(touch.y, Window.height * 0.45))

        self.player.points = self.get_player_points()

    def auto_shoot(self, dt):
        if not self.game_running or self.paused:
            return

        bullet = Bullet(self.canvas, self.player_x, self.player_y + self.player_size)
        self.bullets.append(bullet)

    def spawn_obstacle(self, dt):
        if not self.game_running or self.paused:
            return

        obstacle = Obstacle(self.canvas)
        self.obstacles.append(obstacle)

    def update(self, dt):
        if not self.game_running or self.paused:
            return

        self.background.size = Window.size

        for bullet in self.bullets[:]:
            bullet.move()

            if bullet.off_screen():
                self.canvas.remove(bullet.shape)
                self.bullets.remove(bullet)

        for obstacle in self.obstacles[:]:
            obstacle.move()

            if self.collides_with_player(obstacle):
                self.game_over()
                return

            for bullet in self.bullets[:]:
                if self.collides_rect(
                    bullet.x, bullet.y, bullet.w, bullet.h,
                    obstacle.x, obstacle.y, obstacle.size, obstacle.size
                ):
                    self.canvas.remove(obstacle.shape)
                    self.canvas.remove(bullet.shape)

                    if obstacle in self.obstacles:
                        self.obstacles.remove(obstacle)

                    if bullet in self.bullets:
                        self.bullets.remove(bullet)

                    self.score += 1
                    self.score_label.text = f"Σκορ: {self.score}"

                    if self.score > self.high_score:
                        self.high_score = self.score
                        self.high_score_label.text = f"Max: {self.high_score}"

                    break

            if obstacle.off_screen() and obstacle in self.obstacles:
                self.canvas.remove(obstacle.shape)
                self.obstacles.remove(obstacle)

    def collides_rect(self, x1, y1, w1, h1, x2, y2, w2, h2):
        return not (
            x1 + w1 < x2 or
            x1 > x2 + w2 or
            y1 + h1 < y2 or
            y1 > y2 + h2
        )

    def collides_with_player(self, obstacle):
        return self.collides_rect(
            self.player_x - self.player_size / 2,
            self.player_y,
            self.player_size,
            self.player_size,
            obstacle.x,
            obstacle.y,
            obstacle.size,
            obstacle.size
        )

    def toggle_pause(self):
        self.paused = not self.paused

    def reset_game(self):
        for bullet in self.bullets:
            self.canvas.remove(bullet.shape)

        for obstacle in self.obstacles:
            self.canvas.remove(obstacle.shape)

        self.bullets.clear()
        self.obstacles.clear()

        self.score = 0
        self.score_label.text = "Σκορ: 0"

        self.game_running = True
        self.paused = False

        self.player_x = Window.width / 2
        self.player_y = Window.height * 0.12
        self.player.points = self.get_player_points()

    def game_over(self):
        self.game_running = False

        with self.canvas:
            Color(1, 1, 1, 1)
            self.game_over_text = Rectangle(
                pos=(Window.width / 2 - 120, Window.height / 2 - 30),
                size=(240, 60)
            )


class GameApp(App):
    def build(self):
        root = FloatLayout()

        score_label = Label(
            text="Σκορ: 0",
            size_hint=(0.4, 0.08),
            pos_hint={"x": 0.02, "top": 0.98},
            font_size="20sp"
        )

        high_score_label = Label(
            text="Max: 0",
            size_hint=(0.4, 0.08),
            pos_hint={"right": 0.98, "top": 0.98},
            font_size="20sp"
        )

        game = AirplaneGame(score_label, high_score_label)
        root.add_widget(game)

        root.add_widget(score_label)
        root.add_widget(high_score_label)

        pause_button = Button(
            text="ΠΑΥΣΗ",
            size_hint=(0.28, 0.08),
            pos_hint={"x": 0.05, "y": 0.01}
        )
        pause_button.bind(on_press=lambda x: game.toggle_pause())

        restart_button = Button(
            text="ΞΑΝΑ",
            size_hint=(0.28, 0.08),
            pos_hint={"right": 0.95, "y": 0.01}
        )
        restart_button.bind(on_press=lambda x: game.reset_game())

        root.add_widget(pause_button)
        root.add_widget(restart_button)

        return root


if __name__ == "__main__":
    GameApp().run()