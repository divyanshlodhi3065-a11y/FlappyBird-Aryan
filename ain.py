from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Ellipse, Triangle
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
import random


class FlappyBird(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # -------------------------
        # BIRD
        # -------------------------
        self.bird_x = 100
        self.bird_y = 350
        self.bird_w = 45
        self.bird_h = 35

        # Physics
        self.velocity = 0
        self.gravity = -900
        self.jump_power = 400

        # -------------------------
        # PIPES
        # -------------------------
        self.pipe_x = Window.width
        self.pipe_width = 75
        self.gap = 190
        self.pipe_bottom = 250

        # -------------------------
        # GAME
        # -------------------------
        self.score = 0
        self.game_over = False

        # -------------------------
        # SOUNDS
        # -------------------------
        self.jump_sound = SoundLoader.load("jump.mp3")
        self.score_sound = SoundLoader.load("score.mp3")
        self.gameover_sound = SoundLoader.load("gameover.mp3")

        # -------------------------
        # SCORE
        # -------------------------
        self.score_label = Label(
            text="Score: 0",
            font_size="28sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(200, 60),
            pos=(15, Window.height - 70)
        )

        self.add_widget(self.score_label)

        Clock.schedule_interval(self.update, 1 / 60)

        self.draw_game()

    # =========================
    # DRAW
    # =========================

    def draw_game(self):

        self.canvas.clear()

        with self.canvas:

            # SKY
            Color(0.45, 0.80, 1, 1)

            Rectangle(
                pos=(0, 0),
                size=Window.size
            )

            # CLOUD 1
            Color(1, 1, 1, 0.8)

            Ellipse(
                pos=(80, Window.height - 150),
                size=(100, 45)
            )

            Ellipse(
                pos=(140, Window.height - 145),
                size=(80, 40)
            )

            # CLOUD 2
            Ellipse(
                pos=(Window.width - 180, Window.height - 220),
                size=(110, 45)
            )

            # GROUND
            Color(0.35, 0.75, 0.25, 1)

            Rectangle(
                pos=(0, 0),
                size=(Window.width, 50)
            )

            # =====================
            # BIRD
            # =====================

            # Body
            Color(1, 0.85, 0, 1)

            Ellipse(
                pos=(self.bird_x, self.bird_y),
                size=(self.bird_w, self.bird_h)
            )

            # Wing
            Color(1, 0.60, 0.05, 1)

            Ellipse(
                pos=(
                    self.bird_x + 3,
                    self.bird_y + 5
                ),
                size=(27, 18)
            )

            # Eye white
            Color(1, 1, 1, 1)

            Ellipse(
                pos=(
                    self.bird_x + 29,
                    self.bird_y + 20
                ),
                size=(13, 13)
            )

            # Eye black
            Color(0, 0, 0, 1)

            Ellipse(
                pos=(
                    self.bird_x + 35,
                    self.bird_y + 25
                ),
                size=(6, 6)
            )

            # Beak
            Color(1, 0.30, 0.02, 1)

            Triangle(
                points=[
                    self.bird_x + 43,
                    self.bird_y + 15,

                    self.bird_x + 60,
                    self.bird_y + 22,

                    self.bird_x + 43,
                    self.bird_y + 28
                ]
            )

            # =====================
            # PIPES
            # =====================

            Color(0.10, 0.65, 0.18, 1)

            # Bottom pipe
            Rectangle(
                pos=(
                    self.pipe_x,
                    50
                ),
                size=(
                    self.pipe_width,
                    self.pipe_bottom - 50
                )
            )

            # Bottom pipe cap
            Rectangle(
                pos=(
                    self.pipe_x - 7,
                    self.pipe_bottom - 20
                ),
                size=(
                    self.pipe_width + 14,
                    20
                )
            )

            # Top pipe
            Rectangle(
                pos=(
                    self.pipe_x,
                    self.pipe_bottom + self.gap
                ),
                size=(
                    self.pipe_width,
                    Window.height -
                    self.pipe_bottom -
                    self.gap
                )
            )

            # Top pipe cap
            Rectangle(
                pos=(
                    self.pipe_x - 7,
                    self.pipe_bottom + self.gap
                ),
                size=(
                    self.pipe_width + 14,
                    20
                )
            )

        # =====================
        # GAME OVER TEXT
        # =====================

        if self.game_over:

            if not hasattr(self, "game_over_label"):

                self.game_over_label = Label(
                    text="GAME OVER\n\nTAP TO RESTART",
                    font_size="30sp",
                    bold=True,
                    halign="center",
                    color=(1, 0.1, 0.2, 1),
                    size_hint=(None, None),
                    size=(Window.width, 160),
                    pos=(
                        0,
                        Window.height / 2 - 80
                    )
                )

                self.add_widget(
                    self.game_over_label
                )

    # =========================
    # UPDATE GAME
    # =========================

    def update(self, dt):

        if self.game_over:
            return

        # Gravity
        self.velocity += self.gravity * dt
        self.bird_y += self.velocity * dt

        # Pipe movement
        self.pipe_x -= 220 * dt

        # =====================
        # NEW PIPE
        # =====================

        if self.pipe_x < -self.pipe_width:

            self.pipe_x = Window.width

            self.pipe_bottom = random.randint(
                120,
                max(121, int(Window.height - 320))
            )

            self.score += 1

            self.score_label.text = (
                "Score: " + str(self.score)
            )

            # SCORE SOUND
            self.play_sound(self.score_sound)

        # =====================
        # COLLISION
        # =====================

        bird_left = self.bird_x
        bird_right = self.bird_x + self.bird_w
        bird_bottom = self.bird_y
        bird_top = self.bird_y + self.bird_h

        pipe_left = self.pipe_x
        pipe_right = self.pipe_x + self.pipe_width

        hit_pipe_x = (
            bird_right > pipe_left
            and bird_left < pipe_right
        )

        hit_bottom = (
            bird_bottom < self.pipe_bottom
        )

        hit_top = (
            bird_top >
            self.pipe_bottom + self.gap
        )

        hit_ground = (
            self.bird_y <= 50
        )

        hit_ceiling = (
            self.bird_y + self.bird_h >= Window.height
        )

        if (
            (
                hit_pipe_x
                and
                (hit_bottom or hit_top)
            )
            or hit_ground
            or hit_ceiling
        ):

            self.game_over = True

            # GAME OVER SOUND
            self.play_sound(
                self.gameover_sound
            )

        self.draw_game()

    # =========================
    # TOUCH
    # =========================

    def on_touch_down(self, touch):

        # GAME OVER -> RESTART
        if self.game_over:

            self.game_over = False

            self.bird_y = 350
            self.velocity = 0

            self.pipe_x = Window.width
            self.pipe_bottom = 250

            self.score = 0

            self.score_label.text = "Score: 0"

            if hasattr(
                self,
                "game_over_label"
            ):

                self.remove_widget(
                    self.game_over_label
                )

                del self.game_over_label

            return True

        # TAP -> JUMP
        self.velocity = self.jump_power

        # JUMP SOUND
        self.play_sound(
            self.jump_sound
        )

        return True

    # =========================
    # SOUND
    # =========================

    def play_sound(self, sound):

        if sound is not None:

            try:
                sound.stop()
                sound.play()

            except Exception as e:
                print("Sound error:", e)


class FlappyBirdApp(App):

    def build(self):
        return FlappyBird()


if __name__ == "__main__":
    FlappyBirdApp().run()