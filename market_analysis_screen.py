import openai

openai.api_key = ("openai"), ["api_key"]
openai.api_key = "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"

import json
import pandas as pd
import matplotlib.pyplot as plt
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.snackbar import Snackbar
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel

class MarketAnalysisScreen(Screen):
    def __init__(self, app=None, **kwargs):
        super(MarketAnalysisScreen, self).__init__(**kwargs)
        self.app = app

        self.market_text_input = MDTextField(hint_text="Enter a keyword related to the market", size_hint=(.8, None), height=50)
        self.analyze_button = MDRaisedButton(text="Analyze", size_hint=(.8, None), height=50)
        self.analyze_button.bind(on_release=self.analyze_market)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.market_text_input)
        layout.add_widget(self.analyze_button)
        self.add_widget(layout)

    def analyze_market(self, instance):
        keyword = self.market_text_input.text
        data = self.get_market_data(keyword)
        self.plot_market_data(data)

    def get_market_data(self, keyword):
        response = openai.Completion.create(
            engine="davinci",
            prompt=f"Market analysis for {keyword}:",
            temperature=0.5,
            max_tokens=1024,
            n=1,
            stop=None,
            timeout=10,
        )
        result = response.choices[0].text
        data = json.loads(result)
        return data

    def plot_market_data(self, data):
        df = pd.DataFrame(data)
        fig, ax = plt.subplots(figsize=(8, 4))
        df.plot(kind="line", x="date", y="value", ax=ax)
        ax.set_title(f"Market Analysis for {data['keyword']}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Value")
        plt.show()

class MyScreenManager(ScreenManager):
    pass

class TestApp(MDApp):
    def build(self):
        sm = MyScreenManager()
        sm.add_widget(MarketAnalysisScreen())
        sm.current = "MarketAnalysisScreen"
        return sm

if __name__ == "__main__":
    TestApp().run()
