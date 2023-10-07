import os
os.environ['KIVY_NO_FILELOG'] = '1'
os.environ['KIVY_NO_CONSOLELOG'] = '1'

import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.base import EventLoop
import subprocess
import json
import threading

Window.clearcolor = 0, 0, 0.2, 1

class Label2(Label):
    def on_size(self, *args):
        self.text_size = self.size

class SpeedtestApp(App):
    def build(self):
        self.title = 'SpeedTest App - by Pratham Jaiswal'
        self.icon = 'speedtest.png'
        main = GridLayout(cols=1, spacing=dp(10), padding=dp(10))
        speed = GridLayout(cols=2, spacing=dp(10), padding=dp(10))

        download = BoxLayout(orientation='vertical', spacing=dp(5))
        self.downSpeed = Label(text='N/A', color=(0, 1, 0, 1), font_size=dp(24))
        downLabel = Label(text='Download', color=(1, 1, 1, 1), font_size=dp(20))
        download.add_widget(self.downSpeed)
        download.add_widget(downLabel)

        upload = BoxLayout(orientation='vertical', spacing=dp(5))
        self.upSpeed = Label(text='N/A', color=(0, 1, 0, 1), font_size=dp(24))
        upLabel = Label(text='Upload', color=(1, 1, 1, 1), font_size=dp(20))
        upload.add_widget(self.upSpeed)
        upload.add_widget(upLabel)

        speed.add_widget(download)
        speed.add_widget(upload)

        ping = BoxLayout(orientation='horizontal', spacing=dp(5))
        self.pingLabel = Label(text='Ping: ', color=(1, 1, 1, 1), font_size=dp(18))
        self.pingVal = Label(text='N/A', color=(0, 1, 0, 1), font_size=dp(18))
        ping.add_widget(self.pingLabel)
        ping.add_widget(self.pingVal)

        self.startBtn = Button(text='Start', size_hint=(None, None), size=(dp(100), dp(50)))
        self.startBtn.bind(on_press=self.start_test)

        btnLayout = AnchorLayout(anchor_x='center', anchor_y='center')
        btnLayout.add_widget(self.startBtn)

        main.add_widget(speed)
        main.add_widget(ping)
        main.add_widget(btnLayout)

        return main

    def start_test(self, instance):
        self.downSpeed.text = "Testing..."
        self.upSpeed.text = "Testing..."
        self.pingVal.text = "Testing..."
        self.startBtn.disabled = True

        threading.Thread(target=self.run_speed_test).start()

    def run_speed_test(self):
        try:
            result = subprocess.check_output(["speedtest-cli", "--json"], universal_newlines=True, creationflags=subprocess.CREATE_NO_WINDOW)
            results = json.loads(result)

            downSpeed = round(results["download"] / 10**6, 2)
            self.downSpeed.text = f"{downSpeed} Mbps"

            upSpeed = round(results["upload"] / 10**6, 2)
            self.upSpeed.text = f"{upSpeed} Mbps"

            ping = results["ping"]
            self.pingVal.text = f"{ping} ms"
        except subprocess.CalledProcessError as e:
            Clock.schedule_once(lambda dt: self.show_error_popup("Something went wrong\nCheck your network connectiivity"))
        finally:
            self.startBtn.disabled = False

    def show_error_popup(self, error_message):
        self.downSpeed.text = "N/A"
        self.upSpeed.text = "N/A"
        self.pingVal.text = "N/A"

        error = BoxLayout(orientation='vertical')
        errorLabel = Label(text=error_message, halign='center', valign='middle')
        error.add_widget(errorLabel)

        errorMsg = Popup(title="Error", content=error, size_hint=(None, None), size=(400, 200))
        errorMsg.open()

def reset():
    if not EventLoop.event_listeners:
        from kivy.cache import Cache
        Window.Window = Window.core_select_lib('Window', Window.window_impl, True)
        Cache.print_usage()
        for cat in Cache._categories:
            Cache._objects[cat] = {}

if __name__ == '__main__':
    reset()
    SpeedtestApp().run()