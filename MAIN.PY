from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.utils import get_color_from_hex
import math


# ✅ Safe Calculator
def safe_calc(expr):
    expr = expr.replace('×', '*').replace('÷', '/').replace('^', '**')
    allowed = "0123456789+-*/.() "
    for c in expr:
        if c not in allowed:
            raise Exception("Invalid")
    return eval(expr)


# ✅ Rounded Button
class RoundedButton(Button):
    def __init__(self, bg_color="#1C1C1C", **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)

        with self.canvas.before:
            Color(*get_color_from_hex(bg_color))
            self.rect = RoundedRectangle(radius=[dp(20)])

        self.bind(pos=self.update_rect, size=self.update_rect)
        self.bind(on_press=self.animate_press)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def animate_press(self, *args):
        Animation(opacity=0.7, duration=0.05).start(self)
        Animation(opacity=1, duration=0.1).start(self)


class CalculatorApp(App):

    memory = 0
    history = []
    dark_mode = True

    def build(self):
        Window.clearcolor = (0, 0, 0, 1)

        main = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # ✅ History
        self.history_label = Label(
            text="",
            size_hint_y=None,
            halign="right",
            valign="top",
            color=(0.5, 0.5, 0.5, 1),
            font_size='14sp'
        )
        self.history_label.bind(texture_size=self.history_label.setter('size'))

        scroll = ScrollView(size_hint=(1, 0.2))
        scroll.add_widget(self.history_label)
        main.add_widget(scroll)

        # ✅ Display
        self.display = Label(
            text="0",
            font_size='48sp',
            halign='right',
            valign='middle',
            size_hint=(1, 0.2),
            color=(1, 1, 1, 1)
        )
        self.display.bind(size=lambda i, v: setattr(i, 'text_size', v))
        self.display.bind(on_touch_down=self.double_tap_theme)
        main.add_widget(self.display)

        # ✅ Buttons
        grid = GridLayout(cols=4, spacing=dp(8), size_hint=(1, 0.6))

        buttons = [
            'MC', 'MR', 'M+', 'M-',
            'C', '±', '🌙', '÷',
            '7', '8', '9', '×',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            '0', '.', '√', '=',
            'x²', '^', '[x]', 'sin',
            'cos', 'tan', 'log', 'ln'
        ]

        for text in buttons:
            if text in ['÷', '×', '-', '+', '=', '^']:
                color = '#9C27B0'
            elif text in ['C', '±', '√', 'x²', '[x]', 'sin', 'cos', 'tan', 'log', 'ln']:
                color = '#424242'
            elif text in ['MC', 'MR', 'M+', 'M-']:
                color = '#00695C'
            elif text == '🌙':
                color = '#455A64'
            else:
                color = '#1C1C1C'

            btn = RoundedButton(text=text, bg_color=color, font_size='18sp', color=(1, 1, 1, 1))
            btn.bind(on_press=self.on_press)
            grid.add_widget(btn)

        main.add_widget(grid)

        return main

    def adjust_font(self):
        length = len(self.display.text)
        if length > 20:
            self.display.font_size = '22sp'
        elif length > 15:
            self.display.font_size = '30sp'
        elif length > 10:
            self.display.font_size = '38sp'
        else:
            self.display.font_size = '48sp'

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            Window.clearcolor = (0, 0, 0, 1)
            self.display.color = (1, 1, 1, 1)
        else:
            Window.clearcolor = (1, 1, 1, 1)
            self.display.color = (0, 0, 0, 1)

    def double_tap_theme(self, instance, touch):
        if touch.is_double_tap:
            self.toggle_theme()

    def on_press(self, instance):
        text = instance.text
        current = self.display.text

        if text == 'C':
            self.display.text = "0"

        elif text == '[x]':
            self.display.text = current[:-1] if len(current) > 1 else "0"

        elif text == '±':
            if current.startswith('-'):
                self.display.text = current[1:]
            elif current != "0":
                self.display.text = '-' + current

        elif text == '√':
            try:
                val = float(current)
                self.display.text = str(round(math.sqrt(val), 10)) if val >= 0 else "Error"
            except:
                self.display.text = "Error"

        elif text == 'x²':
            try:
                self.display.text = str(round(float(current) ** 2, 10))
            except:
                self.display.text = "Error"

        elif text == '🌙':
            self.toggle_theme()

        elif text == '=':
            try:
                result = safe_calc(current)
                self.history.append(f"{current} = {result}")
                self.history_label.text = "\n".join(self.history[-10:])
                self.display.text = str(result)
            except:
                self.display.text = "Error"

        elif text in ['MC', 'MR', 'M+', 'M-']:
            try:
                value = float(current)
            except:
                value = 0

            if text == 'MC':
                self.memory = 0
            elif text == 'MR':
                self.display.text = str(self.memory)
            elif text == 'M+':
                self.memory += value
            elif text == 'M-':
                self.memory -= value

        elif text in ['sin', 'cos', 'tan', 'log', 'ln']:
            try:
                val = float(current)
                if text == 'sin':
                    self.display.text = str(round(math.sin(math.radians(val)), 10))
                elif text == 'cos':
                    self.display.text = str(round(math.cos(math.radians(val)), 10))
                elif text == 'tan':
                    self.display.text = str(round(math.tan(math.radians(val)), 10))
                elif text == 'log':
                    self.display.text = str(round(math.log10(val), 10)) if val > 0 else "Error"
                elif text == 'ln':
                    self.display.text = str(round(math.log(val), 10)) if val > 0 else "Error"
            except:
                self.display.text = "Error"

        elif text in ['+', '-', '×', '÷', '^']:
            if current and current[-1] in ['+', '-', '×', '÷', '^']:
                self.display.text = current[:-1] + text
            else:
                self.display.text += text

        else:
            if current == "0":
                self.display.text = text
            else:
                self.display.text += text

        self.adjust_font()


if __name__ == "__main__":
    CalculatorApp().run()
