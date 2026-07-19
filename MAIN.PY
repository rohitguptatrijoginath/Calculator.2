from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.utils import get_color_from_hex
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock

import math


# ✅ SAFE CALC
def safe_calc(expr):
    expr = expr.replace('×', '*').replace('÷', '/').replace('^', '**')
    allowed = "0123456789+-*/.() "
    for c in expr:
        if c not in allowed:
            raise Exception("Invalid")
    return eval(expr)


# ✅ ROUNDED BUTTON
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


class AdvancedCalculatorX(App):

    memory = 0
    dark_mode = True

    def build(self):
        Window.clearcolor = (0, 0, 0, 1)
        self.store = JsonStore('history.json')

        main = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

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

        tabs = TabbedPanel(do_default_tab=False)

        basic_tab = TabbedPanelItem(text="Calculator")
        basic_tab.content = self.basic_layout()
        tabs.add_widget(basic_tab)

        sci_tab = TabbedPanelItem(text="Scientific")
        sci_tab.content = self.scientific_layout()
        tabs.add_widget(sci_tab)

        hist_tab = TabbedPanelItem(text="History")
        hist_tab.content = self.history_layout()
        tabs.add_widget(hist_tab)

        main.add_widget(tabs)

        return main

    # ✅ BASIC
    def basic_layout(self):
        grid = GridLayout(cols=4, spacing=dp(8))

        buttons = [
            'MC', 'MR', 'M+', 'M-',
            'C', '±', '🌙', '÷',
            '7', '8', '9', '×',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            '0', '.', '√', '=',
            'x²', '^', '[x]', '00'
        ]

        for text in buttons:
            btn = RoundedButton(text=text, bg_color='#1C1C1C')
            btn.bind(on_press=self.basic_press)
            grid.add_widget(btn)

        return grid

    # ✅ SCIENTIFIC
    def scientific_layout(self):
        grid = GridLayout(cols=4, spacing=dp(8))

        buttons = [
            'sin', 'cos', 'tan', 'π',
            'log', 'ln', 'e', '!',
            '(', ')', '^', 'DEL',
            '7', '8', '9', '÷',
            '4', '5', '6', '×',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]

        for text in buttons:
            btn = RoundedButton(text=text, bg_color='#1C1C1C')
            btn.bind(on_press=self.scientific_press)
            grid.add_widget(btn)

        return grid

    # ✅ HISTORY
    def history_layout(self):
        box = BoxLayout(orientation='vertical')
        self.history_label = Label(text="", size_hint_y=None)
        scroll = ScrollView()
        scroll.add_widget(self.history_label)
        box.add_widget(scroll)
        self.load_history()
        return box

    def save_history(self, expr, result):
        data = self.store.get('items')['list'] if self.store.exists('items') else []
        data.append(f"{expr} = {result}")
        self.store.put('items', list=data[-50:])

    def load_history(self):
        if self.store.exists('items'):
            items = self.store.get('items')['list']
            self.history_label.text = "\n".join(items[::-1])

    # ✅ BASIC LOGIC
    def basic_press(self, instance):
        text = instance.text
        current = self.display.text

        if text == 'C':
            self.display.text = "0"
        elif text == '[x]':
            self.display.text = current[:-1] if len(current) > 1 else "0"
        elif text == '±':
            self.display.text = current[1:] if current.startswith("-") else "-" + current
        elif text == '√':
            self.display.text = str(round(math.sqrt(float(current)), 10))
        elif text == 'x²':
            self.display.text = str(round(float(current) ** 2, 10))
        elif text == '=':
            try:
                result = safe_calc(current)
                self.display.text = str(result)
                self.save_history(current, result)
                self.load_history()
            except:
                self.display.text = "Error"
        elif text == '🌙':
            self.toggle_theme()
        else:
            if current == "0":
                self.display.text = text
            else:
                self.display.text += text

    # ✅ SCIENTIFIC LOGIC
    def scientific_press(self, instance):
        text = instance.text
        current = self.display.text

        try:
            if text == 'sin':
                self.display.text = str(math.sin(float(current)))
            elif text == 'cos':
                self.display.text = str(math.cos(float(current)))
            elif text == 'tan':
                self.display.text = str(math.tan(float(current)))
            elif text == 'log':
                self.display.text = str(math.log10(float(current)))
            elif text == 'ln':
                self.display.text = str(math.log(float(current)))
            elif text == 'π':
                self.display.text += str(math.pi)
            elif text == 'e':
                self.display.text += str(math.e)
            elif text == '!':
                self.display.text = str(math.factorial(int(float(current))))
            elif text == 'DEL':
                self.display.text = current[:-1] if len(current) > 1 else "0"
            elif text == '=':
                result = safe_calc(current)
                self.display.text = str(result)
                self.save_history(current, result)
                self.load_history()
            else:
                if current == "0":
                    self.display.text = text
                else:
                    self.display.text += text
        except:
            self.display.text = "Error"

    # ✅ THEME
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


if __name__ == "__main__":
    AdvancedCalculatorX().run()
